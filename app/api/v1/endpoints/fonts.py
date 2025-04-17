from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form
from app.services.font_manager import FontManager
from app.core.config import settings
import logging
from pathlib import Path
import os

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/list")
async def list_fonts():
    """List all available fonts"""
    try:
        font_files = [f.stem for f in settings.FONTS_DIR.glob("*.ttf")]
        return {"fonts": font_files}
    except Exception as e:
        logger.error(f"Error listing fonts: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload")
async def upload_font(
    font_file: UploadFile = File(...),
    font_name: str = Form(...),
    font_manager: FontManager = Depends()
):
    """Upload a new font file"""
    try:
        # Validate font name
        if not font_name.endswith(".ttf"):
            font_name += ".ttf"
        
        # Save the font file
        font_path = settings.FONTS_DIR / font_name
        with open(font_path, "wb") as f:
            content = await font_file.read()
            f.write(content)
        
        # Clear font cache to ensure new font is loaded
        font_manager.clear_cache()
        
        return {"status": "success", "message": f"Font {font_name} uploaded successfully"}
    except Exception as e:
        logger.error(f"Error uploading font: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{font_name}")
async def delete_font(
    font_name: str,
    font_manager: FontManager = Depends()
):
    """Delete a font file"""
    try:
        if not font_name.endswith(".ttf"):
            font_name += ".ttf"
        
        font_path = settings.FONTS_DIR / font_name
        if not font_path.exists():
            raise HTTPException(status_code=404, detail="Font not found")
        
        os.remove(font_path)
        font_manager.clear_cache()
        
        return {"status": "success", "message": f"Font {font_name} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting font: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 