
from fastapi import HTTPException, status
import magic

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/gif", "video/mp4", "video/quicktime", "video/x-msvideo"}

async def check_files(files):
    validated_files = []
    for file in files:
        if file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"Unsupported media type for '{file.filename}': '{file.content_type}'."
            )
        
        total_size = 0
        chunks = []
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            total_size += len(chunk)
            if total_size > MAX_UPLOAD_SIZE:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"File '{file.filename}' exceeds the 10 MB size limit."
                )
            chunks.append(chunk)

        file_bytes = b"".join(chunks)

        actual_mime = magic.from_buffer(file_bytes[:2048], mime=True)
        if actual_mime not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"File '{file.filename}' content identified as '{actual_mime}', which is not allowed."
            )
        
        validated_files.append({
            "filename": file.filename,
            "bytes": file_bytes
        })
    
    return validated_files