from flask import Blueprint, request, jsonify, session, current_app
from services.ai_service import ai_service
from models.chat_history import ChatHistory
from utils.auth_decorators import login_required
from utils.helpers import allowed_file, save_uploaded_file
import os
import uuid

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/summarize/text', methods=['POST'])
@login_required
async def summarize_text():
    """Summarize text content"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        length = data.get('length', 'medium')
        
        if not text:
            return jsonify({'success': False, 'error': 'Text content is required'}), 400
        
        if len(text) < 50:
            return jsonify({'success': False, 'error': 'Text must be at least 50 characters long'}), 400
        
        # Call AI service
        result = await ai_service.summarize_text(text, length)
        
        if result['success']:
            # Save to chat history
            chat = ChatHistory(
                user_id=session['user_id'],
                type='text_summarization',
                input_data={'text': text[:500], 'length': length},  # Truncate for storage
                output_data={'summary': result['summary']},
                metadata={'original_length': result['original_length'], 'summary_length': result['summary_length']}
            )
            chat.save()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@chatbot_bp.route('/summarize/video', methods=['POST'])
@login_required
async def summarize_video():
    """Summarize video content"""
    try:
        if 'video' not in request.files:
            return jsonify({'success': False, 'error': 'No video file provided'}), 400
        
        video_file = request.files['video']
        length = request.form.get('length', 'medium')
        
        if video_file.filename == '':
            return jsonify({'success': False, 'error': 'No video file selected'}), 400
        
        if not allowed_file(video_file.filename, ['mp4', 'avi', 'mov', 'mkv']):
            return jsonify({'success': False, 'error': 'Invalid video format. Supported: MP4, AVI, MOV, MKV'}), 400
        
        # Save uploaded file
        filename = f"{uuid.uuid4().hex}_{video_file.filename}"
        video_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'videos', filename)
        video_file.save(video_path)
        
        try:
            # Process video
            result = await ai_service.summarize_video(video_path, length)
            
            if result['success']:
                # Save to chat history
                chat = ChatHistory(
                    user_id=session['user_id'],
                    type='video_summarization',
                    input_data={'filename': video_file.filename, 'length': length},
                    output_data={'summary': result['summary']},
                    metadata={
                        'transcription_length': len(result.get('transcription', '')),
                        'video_duration': result.get('video_duration', 0)
                    }
                )
                chat.save()
            
            return jsonify(result)
            
        finally:
            # Clean up uploaded file
            if os.path.exists(video_path):
                os.remove(video_path)
                
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@chatbot_bp.route('/pdf/upload', methods=['POST'])
@login_required
async def upload_pdf():
    """Upload and process PDF for Q&A"""
    try:
        if 'pdf' not in request.files:
            return jsonify({'success': False, 'error': 'No PDF file provided'}), 400
        
        pdf_file = request.files['pdf']
        
        if pdf_file.filename == '':
            return jsonify({'success': False, 'error': 'No PDF file selected'}), 400
        
        if not allowed_file(pdf_file.filename, ['pdf']):
            return jsonify({'success': False, 'error': 'Invalid file format. Only PDF files are allowed'}), 400
        
        # Save uploaded file
        filename = f"{uuid.uuid4().hex}_{pdf_file.filename}"
        pdf_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'pdfs', filename)
        pdf_file.save(pdf_path)
        
        # Extract text from PDF
        result = await ai_service.extract_pdf_text(pdf_path)
        
        if result['success']:
            # Store PDF session data
            session[f'pdf_{filename}'] = {
                'path': pdf_path,
                'text': result['text'],
                'pages': result['pages'],
                'original_filename': pdf_file.filename
            }
            
            return jsonify({
                'success': True,
                'pdf_id': filename,
                'pages': result['pages'],
                'filename': pdf_file.filename,
                'text_preview': result['text'][:500] + '...' if len(result['text']) > 500 else result['text']
            })
        else:
            # Clean up file if processing failed
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@chatbot_bp.route('/pdf/question', methods=['POST'])
@login_required
async def pdf_question():
    """Ask question about uploaded PDF"""
    try:
        data = request.get_json()
        pdf_id = data.get('pdf_id')
        question = data.get('question', '').strip()
        
        if not pdf_id or not question:
            return jsonify({'success': False, 'error': 'PDF ID and question are required'}), 400
        
        # Get PDF data from session
        pdf_key = f'pdf_{pdf_id}'
        if pdf_key not in session:
            return jsonify({'success': False, 'error': 'PDF not found. Please upload again.'}), 404
        
        pdf_data = session[pdf_key]
        
        # Get answer from AI
        result = await ai_service.pdf_question_answer(pdf_data['text'], question)
        
        if result['success']:
            # Save to chat history
            chat = ChatHistory(
                user_id=session['user_id'],
                type='pdf_qa',
                input_data={'question': question, 'pdf_filename': pdf_data['original_filename']},
                output_data={'answer': result['answer']},
                metadata={'pdf_pages': pdf_data['pages']}
            )
            chat.save()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@chatbot_bp.route('/question', methods=['POST'])
@login_required
async def general_question():
    """General Q&A"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        context = data.get('context', '')
        
        if not question:
            return jsonify({'success': False, 'error': 'Question is required'}), 400
        
        # Get answer from AI
        result = await ai_service.general_qa(question, context)
        
        if result['success']:
            # Save to chat history
            chat = ChatHistory(
                user_id=session['user_id'],
                type='general_qa',
                input_data={'question': question, 'context': context[:200] if context else ''},
                output_data={'answer': result['answer']}
            )
            chat.save()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@chatbot_bp.route('/history', methods=['GET'])
@login_required
def get_chat_history():
    """Get user's chat history"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        chat_type = request.args.get('type', 'all')
        
        history = ChatHistory.get_user_history(
            user_id=session['user_id'],
            chat_type=chat_type if chat_type != 'all' else None,
            page=page,
            limit=limit
        )
        
        return jsonify({
            'success': True,
            'history': history['chats'],
            'pagination': {
                'page': page,
                'limit': limit,
                'total': history['total'],
                'pages': (history['total'] + limit - 1) // limit
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@chatbot_bp.route('/history/<chat_id>', methods=['DELETE'])
@login_required
def delete_chat(chat_id):
    """Delete specific chat from history"""
    try:
        success = ChatHistory.delete_chat(chat_id, session['user_id'])
        
        if success:
            return jsonify({'success': True, 'message': 'Chat deleted successfully'})
        else:
            return jsonify({'success': False, 'error': 'Chat not found or unauthorized'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500