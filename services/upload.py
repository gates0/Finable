import os
from fastapi import UploadFile, HTTPException
from datetime import datetime
from uuid import uuid4

UPLOAD_DIR = "uploads/campaigns"

os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_uploaded_file(file: UploadFile) -> str:
    try:
        ext = file.filename.split(".")[-1]
        unique_name = f"{uuid4().hex}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_name)

        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        # Return relative path
        return file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
