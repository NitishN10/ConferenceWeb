import os
import secrets
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_paper_file(file_storage, upload_folder: str, paper_id: str):
    """
    Safely processes an uploaded paper manuscript.
    Attempts to save to local disk if writable (e.g. in local development),
    while also returning the raw file bytes for persistent database storage
    so that deployed serverless environments (like Vercel) do not depend on
    a writable filesystem.
    Returns: (saved_relative_or_full_path, original_filename, file_size, file_bytes)
    """
    orig_name = secure_filename(file_storage.filename)
    if not orig_name:
        orig_name = "paper_submission.pdf"
        
    ext = orig_name.rsplit('.', 1)[1].lower() if '.' in orig_name else 'pdf'
    safe_filename = f"{paper_id}_{secrets.token_hex(4)}.{ext}"
    full_path = os.path.join(upload_folder, safe_filename)
    
    # Read the file content into memory
    file_bytes = file_storage.read()
    file_size = len(file_bytes)
    
    # Attempt to save to disk if filesystem is writable (e.g., local development)
    try:
        os.makedirs(upload_folder, exist_ok=True)
        with open(full_path, 'wb') as f:
            f.write(file_bytes)
    except OSError:
        # Read-only filesystem on serverless environments like Vercel; database stores the file
        pass
    
    return full_path, orig_name, file_size, file_bytes
