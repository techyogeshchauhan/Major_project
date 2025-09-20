# utils/helpers.py
import os

ALLOWED_EXTENSIONS = {
    'images': {'png', 'jpg', 'jpeg', 'gif'},
    'videos': {'mp4', 'mov', 'avi'},
    'pdfs': {'pdf'}
}

def allowed_file(filename, filetype='images'):
    """
    Check if the uploaded file has an allowed extension.
    filetype can be 'images', 'videos', or 'pdfs'
    """
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS.get(filetype, set())

def save_uploaded_file(file, upload_folder, subfolder):
    """
    Save uploaded file to the proper folder
    """
    if file and allowed_file(file.filename, subfolder):
        os.makedirs(os.path.join(upload_folder, subfolder), exist_ok=True)
        filepath = os.path.join(upload_folder, subfolder, file.filename)
        file.save(filepath)
        return filepath
    return None
