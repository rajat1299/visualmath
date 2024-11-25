from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.db_models import Animation
from app.models.animation import AnimationRequest
from app.services.file_service import FileService
from app.services.cache_service import CacheService
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class AnimationService:
    def __init__(self):
        self.file_service = FileService()
        self.cache_service = CacheService()

    async def create_animation(self, db: Session, request: AnimationRequest, manim_code: str, user_id: int = None):
        """Create animation with caching."""
        try:
            # Generate cache key
            cache_key = self.cache_service.get_animation_key(request.description)

            # Try to get from cache or create new
            async def create_new_animation():
                # Create animation record
                db_animation = Animation(
                    description=request.description,
                    manim_code=manim_code,
                    user_id=user_id
                )
                db.add(db_animation)
                db.commit()
                db.refresh(db_animation)

                return {
                    "id": db_animation.id,
                    "description": db_animation.description,
                    "manim_code": db_animation.manim_code,
                    "animation_url": db_animation.animation_url,
                    "user_id": db_animation.user_id
                }

            animation_data = await self.cache_service.get_or_set(
                cache_key,
                create_new_animation,
                expire=settings.CACHE_TTL
            )

            return Animation(**animation_data)

        except Exception as e:
            logger.error(f"Error creating animation: {str(e)}")
            db.rollback()
            raise

    async def get_animation(self, db: Session, animation_id: int):
        """Get animation with caching."""
        cache_key = f"animation_id:{animation_id}"
        
        async def get_from_db():
            animation = db.query(Animation).filter(Animation.id == animation_id).first()
            if animation:
                return {
                    "id": animation.id,
                    "description": animation.description,
                    "manim_code": animation.manim_code,
                    "animation_url": animation.animation_url,
                    "user_id": animation.user_id
                }
            return None

        animation_data = await self.cache_service.get_or_set(
            cache_key,
            get_from_db,
            expire=settings.CACHE_TTL
        )
        
        return Animation(**animation_data) if animation_data else None

    async def cleanup_old_files(self):
        """Clean up old animation files."""
        await self.file_service.cleanup_old_files()

    async def get_recent_animations(self, db: Session, limit: int = 10):
        """Get recent animations with caching."""
        cache_key = f"recent_animations:{limit}"
        
        async def fetch_from_db():
            return (
                db.query(Animation)
                .order_by(desc(Animation.created_at))
                .limit(limit)
                .all()
            )
        
        return await self.cache_service.get_or_set(
            cache_key,
            fetch_from_db,
            expire=300  # Cache for 5 minutes
        )

    async def get_animation_stats(self, db: Session):
        """Get animation statistics."""
        cache_key = "animation_stats"
        
        async def compute_stats():
            total_count = db.query(Animation).count()
            quality_distribution = (
                db.query(Animation.quality, func.count(Animation.id))
                .group_by(Animation.quality)
                .all()
            )
            return {
                "total_count": total_count,
                "quality_distribution": dict(quality_distribution)
            }
        
        return await self.cache_service.get_or_set(
            cache_key,
            compute_stats,
            expire=3600  # Cache for 1 hour
        )
  