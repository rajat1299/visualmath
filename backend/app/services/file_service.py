import os
import aiofiles
from datetime import datetime, timedelta
from app.core.config import settings
import logging
import magic  # for file type validation

logger = logging.getLogger(__name__)

class FileService:
    def __init__(self):
        self.storage_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../storage'))
        self.temp_path = os.path.join(self.storage_path, "temp")
        self.animations_path = os.path.join(self.storage_path, "animations")
        
        # Ensure directories exist
        os.makedirs(self.storage_path, exist_ok=True)
        os.makedirs(self.temp_path, exist_ok=True)
        os.makedirs(self.animations_path, exist_ok=True)
        
        logger.info(f"Storage directories initialized at: {self.storage_path}")

    def validate_file(self, file_path: str) -> bool:
        """Validate file type and size."""
        try:
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size > settings.MAX_UPLOAD_SIZE:
                raise ValueError(f"File size exceeds limit: {file_size} > {settings.MAX_UPLOAD_SIZE}")
            
            # Check file type using python-magic
            mime = magic.Magic(mime=True)
            file_type = mime.from_file(file_path)
            if not file_type.startswith('video/'):
                raise ValueError(f"Invalid file type: {file_type}")
            
            return True
            
        except Exception as e:
            logger.error(f"File validation failed: {str(e)}")
            return False

    async def save_animation(self, animation_id: int, video_data: bytes) -> str:
        """Save animation video and return its URL."""
        filename = f"animation_{animation_id}.mp4"
        filepath = os.path.join(self.animations_path, filename)
        
        # Save file
        async with aiofiles.open(filepath, 'wb') as f:
            await f.write(video_data)
        
        # Validate saved file
        if not self.validate_file(filepath):
            os.remove(filepath)
            raise ValueError("Invalid file generated")
        
        logger.info(f"Animation saved to: {filepath}")
        return f"/storage/animations/{filename}"

    async def cleanup_old_files(self, max_age_days: int = None):
        """Remove files older than max_age_days."""
        max_age = max_age_days or settings.MAX_FILE_AGE_DAYS
        now = datetime.now()
        
        for directory in [self.temp_path, self.animations_path]:
            if os.path.exists(directory):
                for filename in os.listdir(directory):
                    filepath = os.path.join(directory, filename)
                    file_modified = datetime.fromtimestamp(os.path.getmtime(filepath))
                    if now - file_modified > timedelta(days=max_age):
                        try:
                            os.remove(filepath)
                            logger.info(f"Cleaned up old file: {filepath}")
                        except Exception as e:
                            logger.error(f"Failed to remove file {filepath}: {str(e)}")