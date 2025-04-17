from setuptools import setup, find_packages

setup(
    name="textsnap",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.109.2",
        "uvicorn==0.27.1",
        "pydantic==2.6.1",
        "pydantic-settings==2.1.0",
        "pillow==10.2.0",
        "aiohttp==3.9.3",
        "python-multipart==0.0.9",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "python-dotenv==1.0.1",
        "svglib==1.5.1",
        "reportlab==4.0.9",
    ],
    extras_require={
        "test": [
            "pytest==8.0.0",
            "pytest-asyncio==0.23.5",
            "httpx==0.26.0",
        ],
    },
    python_requires=">=3.10",
) 