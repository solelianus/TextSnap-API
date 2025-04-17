from fastapi import APIRouter, HTTPException, Depends
from app.models.request import GenerateRequest
from app.services.image_processor import ImageProcessor
from app.core.config import settings
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=dict)
async def generate_image(
    request: GenerateRequest,
    image_processor: ImageProcessor = Depends()
):
    try:
        # Validate image URL
        image_url_str = str(request.image_url)
        if not image_url_str.startswith(("http://", "https://")):
            raise HTTPException(
                status_code=400,
                detail="Invalid image URL. Must start with http:// or https://"
            )

        # Process the image
        result = await image_processor.process_image(request)
        
        return {
            "status": "success",
            "download_url": f"{settings.API_V1_STR}/files/{result}"
        }

    except HTTPException as e:
        logger.error(f"HTTP error in generate_image: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Error in generate_image: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        ) 