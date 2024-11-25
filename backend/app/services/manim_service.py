from app.services.manim_executor import ManimExecutor
from app.services.file_service import FileService
from app.services.video_processor import video_processor
import logging

logger = logging.getLogger(__name__)

class ManimService:
    def __init__(self):
        self.executor = ManimExecutor()
        self.file_service = FileService()

    async def create_animation(self, manim_code: str, animation_id: int, quality: str = None) -> str:
        """Create animation from Manim code and return the URL."""
        try:
            # Execute Manim code
            video_file = await self.executor.execute_manim_code(manim_code)
            
            # Optimize video
            optimized_video = await video_processor.optimize_video(video_file, quality)
            
            # Get video info for logging
            video_info = await video_processor.get_video_info(optimized_video)
            logger.info(f"Video info: {video_info}")
            
            # Read optimized video file
            with open(optimized_video, "rb") as f:
                video_data = f.read()
            
            # Save to permanent storage
            animation_url = await self.file_service.save_animation(
                animation_id=animation_id,
                video_data=video_data
            )
            
            return animation_url

        except Exception as e:
            logger.error(f"Animation creation failed: {str(e)}")
            raise

# Create singleton instance
manim_service = ManimService()