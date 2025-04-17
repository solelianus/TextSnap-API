from fastapi import APIRouter, HTTPException, Depends
from app.core.config import settings
import logging
import shutil
from pathlib import Path

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/status")
async def get_status():
    """Get system status and statistics"""
    try:
        # Get directory sizes
        output_size = sum(f.stat().st_size for f in settings.OUTPUT_DIR.glob("**/*") if f.is_file())
        cache_size = sum(f.stat().st_size for f in settings.CACHE_DIR.glob("**/*") if f.is_file())
        fonts_size = sum(f.stat().st_size for f in settings.FONTS_DIR.glob("**/*") if f.is_file())
        
        # Count files
        output_files = len(list(settings.OUTPUT_DIR.glob("**/*")))
        cache_files = len(list(settings.CACHE_DIR.glob("**/*")))
        font_files = len(list(settings.FONTS_DIR.glob("**/*")))
        
        return {
            "status": "running",
            "directories": {
                "output": {
                    "size": output_size,
                    "files": output_files
                },
                "cache": {
                    "size": cache_size,
                    "files": cache_files
                },
                "fonts": {
                    "size": fonts_size,
                    "files": font_files
                }
            }
        }
    except Exception as e:
        logger.error(f"Error getting status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cleanup")
async def cleanup_system():
    """Clean up temporary files and cache"""
    try:
        # Clean output directory
        for file in settings.OUTPUT_DIR.glob("*"):
            if file.is_file():
                file.unlink()
        
        # Clean cache directory
        for file in settings.CACHE_DIR.glob("*"):
            if file.is_file():
                file.unlink()
        
        # Clean fonts directory (except .ttf files)
        for file in settings.FONTS_DIR.glob("*"):
            if file.is_file() and not file.suffix.lower() == '.ttf':
                file.unlink()
        
        return {"status": "success", "message": "System cleaned up successfully"}
    except Exception as e:
        logger.error(f"Error cleaning up system: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset")
async def reset_system():
    """Reset the system (delete all generated files and cache)"""
    try:
        # Remove and recreate output directory
        if settings.OUTPUT_DIR.exists():
            shutil.rmtree(settings.OUTPUT_DIR)
        settings.OUTPUT_DIR.mkdir(parents=True)
        
        # Remove and recreate cache directory
        if settings.CACHE_DIR.exists():
            shutil.rmtree(settings.CACHE_DIR)
        settings.CACHE_DIR.mkdir(parents=True)
        
        # For fonts directory, remove everything except .ttf files
        if settings.FONTS_DIR.exists():
            # First, move all .ttf files to a temporary directory
            temp_dir = settings.FONTS_DIR.parent / "temp_fonts"
            temp_dir.mkdir(exist_ok=True)
            
            for file in settings.FONTS_DIR.glob("*.ttf"):
                shutil.move(str(file), str(temp_dir / file.name))
            
            # Remove the entire fonts directory
            shutil.rmtree(settings.FONTS_DIR)
            
            # Recreate fonts directory
            settings.FONTS_DIR.mkdir(parents=True)
            
            # Move .ttf files back
            for file in temp_dir.glob("*.ttf"):
                shutil.move(str(file), str(settings.FONTS_DIR / file.name))
            
            # Remove temporary directory
            shutil.rmtree(temp_dir)
        
        return {"status": "success", "message": "System reset successfully"}
    except Exception as e:
        logger.error(f"Error resetting system: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 