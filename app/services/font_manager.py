import os
from pathlib import Path
from PIL import ImageFont
import logging
from app.core.config import settings
import platform

logger = logging.getLogger(__name__)

class FontManager:
    def __init__(self):
        self.font_cache = {}
        self._ensure_fonts_directory()
        self._init_system_fonts()

    def _ensure_fonts_directory(self):
        """Ensure the fonts directory exists"""
        os.makedirs(settings.FONTS_DIR, exist_ok=True)

    def _init_system_fonts(self):
        """Initialize system font paths based on platform"""
        if platform.system() == "Windows":
            self.system_fonts_dir = Path(os.environ.get("WINDIR", "C:\\Windows")) / "Fonts"
        elif platform.system() == "Darwin":  # macOS
            self.system_fonts_dir = Path("/System/Library/Fonts")
        else:  # Linux and others
            self.system_fonts_dir = Path("/usr/share/fonts")
        
        # Additional font directories for Linux
        if platform.system() == "Linux":
            self.system_fonts_dirs = [
                self.system_fonts_dir,
                Path("/usr/local/share/fonts"),
                Path.home() / ".local/share/fonts"
            ]
        else:
            self.system_fonts_dirs = [self.system_fonts_dir]

    def _find_font_in_dirs(self, font_name: str, dirs: list[Path]) -> Path | None:
        """Search for a font in the given directories"""
        for dir_path in dirs:
            if not dir_path.exists():
                continue
                
            # Try exact match first
            font_path = dir_path / f"{font_name}.ttf"
            if font_path.exists():
                return font_path
                
            # Try case-insensitive search
            for file in dir_path.glob("*.ttf"):
                if file.stem.lower() == font_name.lower():
                    return file
                    
        return None

    async def get_font(
        self,
        font_family: str,
        font_weight: str = "normal",
        font_style: str = "normal",
        variant: str = "normal",
        font_size: int = 12
    ) -> ImageFont.FreeTypeFont:
        """
        Get a font with the specified properties.
        If the font is not found, falls back to a default system font.
        """
        cache_key = f"{font_family}_{font_weight}_{font_style}_{variant}_{font_size}"
        
        if cache_key in self.font_cache:
            return self.font_cache[cache_key]

        try:
            # Try to load the font from the fonts directory
            font_path = settings.FONTS_DIR / f"{font_family}.ttf"
            if not font_path.exists():
                # Try system fonts
                font_path = self._find_font_in_dirs(font_family, self.system_fonts_dirs)
            
            if font_path and font_path.exists():
                font = ImageFont.truetype(str(font_path), font_size)
            else:
                # Fall back to default system font
                font = ImageFont.load_default()
                logger.warning(f"Font {font_family} not found, using default font")

            self.font_cache[cache_key] = font
            return font

        except Exception as e:
            logger.error(f"Error loading font: {str(e)}")
            # Fall back to default font on error
            return ImageFont.load_default()

    def clear_cache(self):
        """Clear the font cache"""
        self.font_cache.clear() 