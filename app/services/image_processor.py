from app.models.request import GenerateRequest
from app.services.font_manager import FontManager
from app.services.svg_processor import SVGProcessor
from app.core.config import settings
import aiohttp
import uuid
import os
from PIL import Image, ImageDraw
from io import BytesIO
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ImageProcessor:
    def __init__(self):
        self.font_manager = FontManager()
        self.svg_processor = SVGProcessor()
        # Ensure output directory exists
        settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    async def process_image(self, request: GenerateRequest) -> str:
        try:
            # Download and process the base image
            async with aiohttp.ClientSession() as session:
                async with session.get(str(request.image_url)) as response:
                    if response.status != 200:
                        raise ValueError(f"Failed to download image: {response.status}")
                    
                    image_data = await response.read()
                    base_img = Image.open(BytesIO(image_data)).convert("RGBA")

            # Process background removal if requested
            if request.remove_background:
                base_img = self._remove_background(base_img)

            # Process text items
            draw = ImageDraw.Draw(base_img)
            for item in request.items:
                await self._process_text_item(draw, item, request.font_family)

            # Process SVG items
            if request.svg:
                for svg_item in request.svg:
                    await self._process_svg_item(base_img, svg_item)

            # Process watermark removal if requested
            if request.remove_watermark:
                base_img = self._remove_watermark(base_img)

            # Save the processed image
            filename = f"{uuid.uuid4().hex}.{request.output_format}"
            output_path = settings.OUTPUT_DIR / filename

            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            if request.output_format.lower() in ["jpg", "jpeg"]:
                base_img.convert("RGB").save(output_path, format="JPEG")
            elif request.output_format.lower() == "pdf":
                base_img.convert("RGB").save(output_path, format="PDF")
            else:
                base_img.save(output_path, format=request.output_format.upper())

            return filename

        except Exception as e:
            logger.error(f"Error in process_image: {str(e)}")
            raise

    def _remove_background(self, image: Image.Image) -> Image.Image:
        data = image.getdata()
        new_data = []
        for item in data:
            if item[0] > 200 and item[1] > 200 and item[2] > 200:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        image.putdata(new_data)
        return image

    def _remove_watermark(self, image: Image.Image) -> Image.Image:
        # Implement watermark removal logic
        return image

    async def _process_text_item(
        self,
        draw: ImageDraw.Draw,
        item: dict,
        font_family: str
    ):
        font = await self.font_manager.get_font(
            font_family,
            item.font_weight,
            item.font_style,
            item.variant,
            item.font_size
        )
        
        if item.max_width:
            lines = self._wrap_text(item.text, font, item.max_width)
            y_position = item.position[1]
            bbox = font.getbbox("A")
            line_height = bbox[3] - bbox[1]
            
            for line in lines:
                bbox = font.getbbox(line)
                text_width = bbox[2] - bbox[0]
                x_position = item.position[0] - (text_width // 2)
                draw.text((x_position, y_position), line, font=font, fill=item.color)
                y_position += line_height + 5
        else:
            bbox = font.getbbox(item.text)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x_position = item.position[0] - (text_width // 2)
            y_position = item.position[1] - (text_height // 2)
            draw.text((x_position, y_position), item.text, font=font, fill=item.color)

    async def _process_svg_item(self, base_img: Image.Image, svg_item: dict):
        await self.svg_processor.process_svg(base_img, svg_item)

    def _wrap_text(self, text: str, font, max_width: int) -> list:
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            width = font.getlength(test_line)
            
            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines 