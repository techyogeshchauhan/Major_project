import google.generativeai as genai
from config.ai_config import get_gemini_config
import PyPDF2
import io
import os
from moviepy.editor import VideoFileClip
import speech_recognition as sr
from pydub import AudioSegment
import tempfile

class AIService:
    def __init__(self):
        self.config = get_gemini_config()
        genai.configure(api_key=self.config['api_key'])
        self.model = genai.GenerativeModel(self.config['model_name'])
    
    async def summarize_text(self, text, summary_length='medium'):
        """Summarize text content"""
        try:
            length_prompts = {
                'short': 'in 2-3 sentences',
                'medium': 'in a paragraph (4-6 sentences)',
                'long': 'in detailed bullet points'
            }
            
            prompt = f"""
            Please summarize the following text {length_prompts.get(summary_length, 'concisely')}. 
            Focus on the key points and main ideas:
            
            {text}
            
            Summary:
            """
            
            response = self.model.generate_content(prompt)
            return {
                'success': True,
                'summary': response.text,
                'original_length': len(text),
                'summary_length': len(response.text)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def extract_pdf_text(self, pdf_file_path):
        """Extract text from PDF file"""
        try:
            text = ""
            with open(pdf_file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return {
                'success': True,
                'text': text,
                'pages': len(pdf_reader.pages)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def pdf_question_answer(self, pdf_text, question):
        """Answer questions based on PDF content"""
        try:
            prompt = f"""
            Based on the following document content, please answer the question accurately and concisely:
            
            Document Content:
            {pdf_text[:4000]}  # Limit context to avoid token limits
            
            Question: {question}
            
            Answer:
            """
            
            response = self.model.generate_content(prompt)
            return {
                'success': True,
                'answer': response.text,
                'question': question
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def extract_video_audio(self, video_path):
        """Extract audio from video for transcription"""
        try:
            # Create temporary audio file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
                temp_audio_path = temp_audio.name
            
            # Extract audio from video
            video = VideoFileClip(video_path)
            audio = video.audio
            audio.write_audiofile(temp_audio_path, verbose=False, logger=None)
            
            # Clean up video objects
            audio.close()
            video.close()
            
            return {
                'success': True,
                'audio_path': temp_audio_path,
                'duration': video.duration
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def transcribe_audio(self, audio_path):
        """Transcribe audio to text using speech recognition"""
        try:
            recognizer = sr.Recognizer()
            
            # Convert to wav if needed
            audio = AudioSegment.from_file(audio_path)
            wav_path = audio_path.replace('.mp3', '.wav').replace('.mp4', '.wav')
            audio.export(wav_path, format="wav")
            
            # Transcribe audio
            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
            
            # Clean up temporary files
            if os.path.exists(wav_path):
                os.remove(wav_path)
            
            return {
                'success': True,
                'transcription': text
            }
        except sr.UnknownValueError:
            return {
                'success': False,
                'error': 'Could not understand audio'
            }
        except sr.RequestError as e:
            return {
                'success': False,
                'error': f'Speech recognition service error: {e}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def summarize_video(self, video_path, summary_length='medium'):
        """Extract audio from video, transcribe, and summarize"""
        try:
            # Extract audio from video
            audio_result = await self.extract_video_audio(video_path)
            if not audio_result['success']:
                return audio_result
            
            # Transcribe audio
            transcription_result = await self.transcribe_audio(audio_result['audio_path'])
            if not transcription_result['success']:
                return transcription_result
            
            # Clean up temporary audio file
            if os.path.exists(audio_result['audio_path']):
                os.remove(audio_result['audio_path'])
            
            # Summarize transcription
            summary_result = await self.summarize_text(
                transcription_result['transcription'], 
                summary_length
            )
            
            if summary_result['success']:
                summary_result['transcription'] = transcription_result['transcription']
                summary_result['video_duration'] = audio_result['duration']
            
            return summary_result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def general_qa(self, question, context=None):
        """General question answering"""
        try:
            if context:
                prompt = f"""
                Context: {context}
                
                Question: {question}
                
                Please provide a helpful and accurate answer based on the context provided:
                """
            else:
                prompt = f"""
                Question: {question}
                
                Please provide a helpful, accurate, and educational answer:
                """
            
            response = self.model.generate_content(prompt)
            return {
                'success': True,
                'answer': response.text,
                'question': question
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Global instance
ai_service = AIService()