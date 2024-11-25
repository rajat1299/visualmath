from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.gpt_service import gpt_service
from app.services.manim_service import manim_service
from app.services.animation_service import AnimationService
from app.models.animation import (
    AnimationRequest, 
    AnimationResponse, 
    AnimationError,
    AnimationHistoryResponse
)
import time
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/animations", tags=["animations"])

# Create a singleton instance
animation_service = AnimationService()

@router.post("", response_model=AnimationResponse)
async def create_animation(
    request: AnimationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    start_time = time.time()
    try:
        # Validate input
        if not request.description.strip():
            raise HTTPException(
                status_code=400,
                detail="Description cannot be empty"
            )

        # Convert natural language to Manim code
        manim_code = await gpt_service.generate_manim_code(request.description)
        
        # Store in database
        db_animation = await animation_service.create_animation(
            db=db,
            request=request,
            manim_code=manim_code
        )
        
        # Generate animation using the instance
        animation_url = await manim_service.create_animation(
            manim_code=manim_code,
            animation_id=db_animation.id,
            quality=request.quality
        )
        
        # Update animation URL in database
        db_animation.animation_url = animation_url
        db_animation.quality = request.quality
        db.commit()
        
        # Add cleanup task to background tasks
        background_tasks.add_task(
            animation_service.cleanup_old_files
        )
        
        processing_time = time.time() - start_time
        return AnimationResponse(
            status="success",
            animation_url=animation_url,
            processing_time=processing_time,
            quality=request.quality
        )

    except Exception as e:
        logger.error(f"Animation creation failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/history", response_model=List[AnimationHistoryResponse])
async def get_animation_history(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get recent animation history."""
    try:
        animations = await animation_service.get_recent_animations(db, limit)
        return [
            AnimationHistoryResponse(
                id=anim.id,
                description=anim.description,
                url=anim.animation_url,
                created_at=anim.created_at,
                quality=anim.quality
            )
            for anim in animations
        ]
    except Exception as e:
        logger.error(f"Failed to get animation history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch animation history"
        ) 

@router.get("/stats", response_model=dict)
async def get_animation_stats(
    db: Session = Depends(get_db)
):
    """Get animation statistics."""
    try:
        stats = await animation_service.get_animation_stats(db)
        return stats
    except Exception as e:
        logger.error(f"Failed to get animation stats: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch animation statistics"
        )

@router.delete("/history/{animation_id}")
async def delete_animation(
    animation_id: int,
    db: Session = Depends(get_db)
):
    """Delete an animation from history."""
    try:
        await animation_service.delete_animation(db, animation_id)
        return {"status": "success", "message": "Animation deleted"}
    except Exception as e:
        logger.error(f"Failed to delete animation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to delete animation"
        ) 