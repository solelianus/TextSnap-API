from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Literal

class TextItem(BaseModel):
    text: str
    position: tuple[int, int]
    font_family: str
    font_size: int
    font_weight: str = "normal"
    font_style: str = "normal"
    variant: str = "normal"
    color: str = "#000000"
    max_width: Optional[int] = None

class SVGItem(BaseModel):
    svg_data: str
    position: tuple[int, int]
    width: Optional[int] = None
    height: Optional[int] = None

class GenerateRequest(BaseModel):
    image_url: HttpUrl
    output_format: Literal["png", "jpg", "jpeg", "webp", "pdf"]
    items: List[TextItem]
    font_family: str
    remove_background: bool = False
    remove_watermark: bool = False
    svg: Optional[List[SVGItem]] = None 