import os
import uuid
import logging
from pathlib import Path
from typing import List, Optional
from io import BytesIO
import sqlite3
from functools import lru_cache

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont
import requests
import cairosvg

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configuration
FONTS_DIR = "fonts"
OUTPUT_DIR = "output"
CACHE_DIR = "font_cache"
DB_FILE = "fonts.db"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

# Font database setup
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create the table only if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fonts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            family TEXT NOT NULL,
            weight INTEGER NOT NULL,
            style TEXT NOT NULL,
            variant TEXT NOT NULL DEFAULT 'regular',
            format TEXT NOT NULL,
            path TEXT NOT NULL,
            UNIQUE(family, weight, style, variant, format)
        )
    ''')
    conn.commit()
    conn.close()

def index_fonts():
    """Index all available font files in the database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Clear existing data
    cursor.execute("DELETE FROM fonts")
    conn.commit()

    extensions = ('.ttf', '.woff', '.woff2', '.otf')

    for root, _, files in os.walk(FONTS_DIR):
        for file in files:
            if file.lower().endswith(extensions):
                path = os.path.join(root, file)
                try:
                    stem = Path(file).stem.lower()
                    parts = stem.split('-')

                    family = Path(root).relative_to(FONTS_DIR).parts[0]

                    weight = 400
                    style = 'normal'
                    variant = 'regular'

                    for part in parts:
                        if part.isdigit():
                            weight = int(part)
                        elif part in ('bold', 'light', 'medium', 'black', 'heavy', 'regular'):
                            weight = {
                                'bold': 700,
                                'light': 300,
                                'medium': 500,
                                'black': 900,
                                'heavy': 900,
                                'regular': 400
                            }.get(part, weight)
                        elif part in ('italic', 'oblique'):
                            style = part
                        elif 'fanum' in part:
                            variant = 'fanum'
                        elif 'noen' in part:
                            variant = 'noen'

                    cursor.execute(
                        """INSERT OR IGNORE INTO fonts 
                        (family, weight, style, variant, format, path) 
                        VALUES (?, ?, ?, ?, ?, ?)""",
                        (family.lower(), weight, style, variant, Path(path).suffix[1:].lower(), path)
                    )
                except Exception as e:
                    logger.error(f"Error indexing font {path}: {e}")
                    continue

    conn.commit()
    conn.close()

# Initialize database and index fonts at startup
init_db()
index_fonts()

# Models
class TextItem(BaseModel):
    text: str
    position: List[int]
    font_size: int
    font_weight: Optional[str] = "400"
    color: str
    font_style: Optional[str] = "normal"
    variant: Optional[str] = "regular"

class SvgItem(BaseModel):
    url: str
    position: List[int]
    size: Optional[List[int]] = None

class GenerateRequest(BaseModel):
    image_url: str
    font_family: str
    output_format: str
    items: List[TextItem]
    svg: Optional[List[SvgItem]] = None

# Font utilities
@lru_cache(maxsize=100)
def get_cached_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except Exception as e:
        logger.error(f"Failed to load font {path}: {e}")
        raise

def convert_webfont_to_ttf(source_path: str) -> str:
    cache_path = os.path.join(CACHE_DIR, f"{Path(source_path).stem}.ttf")

    if os.path.exists(cache_path):
        return cache_path

    try:
        if source_path.endswith('.woff2'):
            cairosvg.woff2_to_ttf(url=source_path, write_to=cache_path)
        elif source_path.endswith('.woff'):
            cairosvg.woff_to_ttf(url=source_path, write_to=cache_path)
        else:
            raise ValueError("Unsupported web font format")
        return cache_path
    except Exception as e:
        logger.error(f"Failed to convert web font {source_path}: {e}")
        raise

def find_best_font(family: str, weight: str = "400", style: str = "normal", variant: str = "regular") -> Optional[str]:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            SELECT path, format FROM fonts 
            WHERE family = ? AND weight = ? AND style = ? AND variant = ?
            ORDER BY format = 'ttf' DESC, format = 'otf' DESC
            LIMIT 1
        ''', (family.lower(), int(weight), style.lower(), variant.lower()))
        result = cursor.fetchone()

        if not result:
            cursor.execute('''
                SELECT path, format FROM fonts 
                WHERE family = ? AND weight = ? AND variant = ?
                ORDER BY style = ? DESC, format = 'ttf' DESC, format = 'otf' DESC
                LIMIT 1
            ''', (family.lower(), int(weight), variant.lower(), style.lower()))
            result = cursor.fetchone()

        if not result:
            cursor.execute('''
                SELECT path, format FROM fonts 
                WHERE family = ? AND weight = ?
                ORDER BY variant = ? DESC, style = ? DESC, format = 'ttf' DESC, format = 'otf' DESC
                LIMIT 1
            ''', (family.lower(), int(weight), variant.lower(), style.lower()))
            result = cursor.fetchone()

        if not result:
            cursor.execute('''
                SELECT path, format FROM fonts 
                WHERE family = ?
                ORDER BY abs(CAST(weight AS INTEGER) - ?), variant = ? DESC, style = ? DESC,
                format = 'ttf' DESC, format = 'otf' DESC
                LIMIT 1
            ''', (family.lower(), int(weight), variant.lower(), style.lower()))
            result = cursor.fetchone()

        if result:
            path, fmt = result
            if fmt in ('woff', 'woff2'):
                return convert_webfont_to_ttf(path)
            return path

        return None
    finally:
        conn.close()

# API Endpoints
@app.post("/generate")
async def generate_image(req: GenerateRequest):
    try:
        try:
            bg_resp = requests.get(req.image_url)
            bg_resp.raise_for_status()
            base_img = Image.open(BytesIO(bg_resp.content)).convert("RGBA")
        except Exception as e:
            logger.error(f"Failed to load background image: {e}")
            raise HTTPException(status_code=400, detail="Background image not found or invalid URL.")

        draw = ImageDraw.Draw(base_img)

        for item in req.items:
            try:
                font_path = find_best_font(
                    req.font_family,
                    item.font_weight or "400",
                    item.font_style or "normal",
                    item.variant or "regular"
                )
                if font_path:
                    font = get_cached_font(font_path, item.font_size)
                else:
                    logger.warning(f"No font found for family {req.font_family}, using default")
                    font = ImageFont.load_default()

                draw.text(tuple(item.position), item.text, font=font, fill=item.color)
            except Exception as e:
                logger.error(f"Failed to process text item: {e}")
                continue

        if req.svg:
            for svg_item in req.svg:
                try:
                    svg_response = requests.get(svg_item.url)
                    svg_response.raise_for_status()
                    svg_bytes = BytesIO(svg_response.content)
                    png_bytes = BytesIO()
                    cairosvg.svg2png(file_obj=svg_bytes, write_to=png_bytes)
                    png_bytes.seek(0)
                    svg_img = Image.open(png_bytes).convert("RGBA")
                    if svg_item.size:
                        svg_img = svg_img.resize(tuple(svg_item.size))
                    base_img.paste(svg_img, tuple(svg_item.position), svg_img)
                except Exception as e:
                    logger.error(f"Failed to process SVG item: {e}")
                    continue

        ext_map = {"png": "PNG", "jpg": "JPEG", "webp": "WEBP", "pdf": "PDF"}
        output_format = req.output_format.lower()
        if output_format not in ext_map:
            raise HTTPException(status_code=400, detail="Unsupported output format.")
        out_ext = ext_map[output_format]

        filename = f"{uuid.uuid4().hex}.{output_format}"
        output_path = os.path.join(OUTPUT_DIR, filename)

        try:
            if out_ext == "PDF":
                base_img.convert("RGB").save(output_path, format="PDF")
            elif out_ext == "JPEG":
                base_img.convert("RGB").save(output_path, format="JPEG")
            else:
                base_img.save(output_path, format=out_ext)
        except Exception as e:
            logger.error(f"Failed to save output image: {e}")
            raise HTTPException(status_code=500, detail="Failed to save output image")

        return {
            "status": "success",
            "download_url": f"/download/{filename}"
        }

    except Exception as e:
        logger.error(f"Error in generate_image: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/download/{filename}")
async def download_file(filename: str):
    path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(path):
        logger.warning(f"File not found: {filename}")
        raise HTTPException(status_code=404, detail="File not found.")
    return {
        "message": "To download the file, call this URL directly:",
        "url": f"/files/{filename}"
    }

@app.post("/admin/reindex-fonts")
async def reindex_fonts():
    try:
        index_fonts()
        return {"status": "success", "message": "Fonts reindexed successfully"}
    except Exception as e:
        logger.error(f"Failed to reindex fonts: {e}")
        raise HTTPException(status_code=500, detail="Failed to reindex fonts")

from fastapi.responses import JSONResponse

@app.get("/list-fonts")
async def list_fonts():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT family, weight, style, variant, format FROM fonts
            ORDER BY family, weight, style, variant
        ''')
        rows = cursor.fetchall()

        # Group fonts by family
        fonts: Dict[str, List[Dict]] = {}
        for family, weight, style, variant, fmt in rows:
            key = family.lower()
            if key not in fonts:
                fonts[key] = []
            fonts[key].append({
                "weight": weight,
                "style": style,
                "variant": variant,
                "format": fmt
            })

        return JSONResponse({"status": "success", "fonts": fonts})

    except Exception as e:
        logger.error(f"Failed to list fonts: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch font list")

    finally:
        conn.close()


app.mount("/files", StaticFiles(directory=OUTPUT_DIR), name="files")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
