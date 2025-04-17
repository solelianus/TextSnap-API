import logging
from PIL import Image
import io
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from app.models.request import SVGItem

logger = logging.getLogger(__name__)

class SVGProcessor:
    def __init__(self):
        pass

    async def process_svg(self, base_img: Image.Image, svg_item: SVGItem) -> None:
        """
        Process and overlay an SVG onto the base image.
        
        Args:
            base_img: The base PIL Image to overlay the SVG onto
            svg_item: The SVGItem containing SVG data and positioning information
        """
        try:
            # Convert SVG to PNG using svglib
            drawing = svg2rlg(io.BytesIO(svg_item.svg_data.encode('utf-8')))
            
            # Set output dimensions if specified
            if svg_item.width and svg_item.height:
                drawing.width = svg_item.width
                drawing.height = svg_item.height
            
            # Render to PNG
            png_data = io.BytesIO()
            renderPM.drawToFile(drawing, png_data, fmt="PNG")
            png_data.seek(0)
            
            # Convert PNG data to PIL Image
            svg_img = Image.open(png_data)
            
            # Convert to RGBA if not already
            if svg_img.mode != 'RGBA':
                svg_img = svg_img.convert('RGBA')
            
            # Create a transparent layer the size of the base image
            overlay = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
            
            # Paste the SVG image at the specified position
            overlay.paste(svg_img, svg_item.position, svg_img)
            
            # Composite the overlay onto the base image
            base_img.alpha_composite(overlay)
            
        except Exception as e:
            logger.error(f"Error processing SVG: {str(e)}")
            raise 