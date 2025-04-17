import requests
import os
import uuid
from PIL import Image
from io import BytesIO

# Configuration
BASE_URL = "http://localhost:8000"
TEST_IMAGE_URL = "https://images.unsplash.com/photo-1598048150218-53ab5609ef31?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
TEST_SVG_URL = "https://www.svgrepo.com/download/535115/alien.svg"
OUTPUT_DIR = "test_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def print_test_header(test_name):
    print(f"\n{'='*50}")
    print(f"Running Test: {test_name}")
    print(f"{'='*50}")

def download_and_verify_image(download_url, test_name):
    try:
        full_url = f"{BASE_URL}{download_url.replace('/download', '/files')}"
        image_response = requests.get(full_url)
        if image_response.status_code != 200:
            print(f"Failed to download image: {image_response.status_code}")
            return None

        filename = f"{test_name.replace(' ', '_')}_{uuid.uuid4().hex[:6]}.png"
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, "wb") as f:
            f.write(image_response.content)

        try:
            with Image.open(filepath) as img:
                print(f"✅ Success! Saved result to: {filepath}")
                print(f"Image size: {img.size}, format: {img.format}")
                return filepath
        except Exception as e:
            print(f"⚠️ Image file may be invalid: {str(e)}")
            return None

    except Exception as e:
        print(f"❌ Error during download/verification: {str(e)}")
        return None

def get_available_fonts():
    try:
        response = requests.get(f"{BASE_URL}/list-fonts")
        response.raise_for_status()
        fonts = response.json().get("fonts", {})
        if not fonts:
            raise Exception("Font list is empty.")
        return fonts
    except Exception as e:
        print(f"❌ Failed to fetch fonts: {str(e)}")
        return {}

def get_first_valid_font(fonts, preferred_family=None):
    if preferred_family and preferred_family in fonts:
        family = preferred_family
    else:
        family = list(fonts.keys())[0]  # fallback

    font_options = fonts[family]
    first = font_options[0]
    return {
        "family": family,
        "weight": first["weight"],
        "style": first["style"],
        "variant": first["variant"]
    }

def test_basic_text_rendering(font_data):
    print_test_header("Basic Text Rendering")

    payload = {
        "image_url": TEST_IMAGE_URL,
        "font_family": font_data["family"],
        "output_format": "png",
        "items": [
            {
                "text": "این یک متن تست فارسی است",
                "position": [100, 100],
                "font_size": 36,
                "font_weight": font_data["weight"],
                "font_style": font_data["style"],
                "variant": font_data["variant"],
                "color": "#FFFFFF"
            }
        ]
    }

    try:
        response = requests.post(f"{BASE_URL}/generate", json=payload)
        if response.status_code != 200:
            print(f"❌ API request failed: {response.status_code}")
            try:
                print(response.json())
            except:
                print("Failed to decode error response.")
            return None

        result = response.json()
        return download_and_verify_image(result["download_url"], "basic_text")

    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return None

def test_svg_overlay(font_data):
    print_test_header("SVG Overlay Test")

    payload = {
        "image_url": TEST_IMAGE_URL,
        "font_family": font_data["family"],
        "output_format": "png",
        "items": [
            {
                "text": "متن همراه با SVG",
                "position": [100, 100],
                "font_size": 32,
                "font_weight": font_data["weight"],
                "font_style": font_data["style"],
                "variant": font_data["variant"],
                "color": "#000000"
            }
        ],
        "svg": [
            {
                "url": TEST_SVG_URL,
                "position": [200, 200],
                "size": [100, 100]
            }
        ]
    }

    try:
        response = requests.post(f"{BASE_URL}/generate", json=payload)
        if response.status_code != 200:
            print(f"❌ API request failed: {response.status_code}")
            try:
                print(response.json())
            except:
                print("Failed to decode error response.")
            return None

        result = response.json()
        return download_and_verify_image(result["download_url"], "svg_overlay")

    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return None

def test_output_formats(font_data):
    print_test_header("Output Formats Test")

    formats = ["png", "jpg", "webp"]
    results = []

    for fmt in formats:
        print(f"\n--- Testing format: {fmt.upper()} ---")
        payload = {
            "image_url": TEST_IMAGE_URL,
            "font_family": font_data["family"],
            "output_format": fmt,
            "items": [
                {
                    "text": f"فرمت خروجی: {fmt}",
                    "position": [100, 100],
                    "font_size": 32,
                    "font_weight": font_data["weight"],
                    "font_style": font_data["style"],
                    "variant": font_data["variant"],
                    "color": "#000000"
                }
            ]
        }

        try:
            response = requests.post(f"{BASE_URL}/generate", json=payload)
            if response.status_code != 200:
                print(f"❌ Failed for format {fmt}: {response.status_code}")
                try:
                    print(response.json())
                except:
                    print("Failed to decode error response.")
                continue

            result = response.json()
            result_path = download_and_verify_image(result["download_url"], f"format_{fmt}")
            if result_path:
                results.append(result_path)

        except Exception as e:
            print(f"❌ Error testing format {fmt}: {str(e)}")

    return results

def run_all_tests():
    print("\n🚀 Starting API Tests...")
    fonts = get_available_fonts()
    if not fonts:
        print("❌ No fonts available to test.")
        return

    font_data = get_first_valid_font(fonts, preferred_family="dana")

    test_basic_text_rendering(font_data)
    test_svg_overlay(font_data)
    test_output_formats(font_data)

    print("\n✅ All tests completed!")

if __name__ == "__main__":
    run_all_tests()
