import os
import sys
from PIL import Image, ImageEnhance

def load_images(folder_path):
    """Load all images from the given folder."""
    images = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            images.append(filename)
    return images


def apply_opacity(image, opacity):
    """Apply opacity to a watermark image."""
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    alpha = image.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity / 255.0)
    image.putalpha(alpha)
    return image


def calculate_position(base_size, wm_size, mode):
    """Calculate watermark placement based on the selected mode."""
    base_w, base_h = base_size
    wm_w, wm_h = wm_size

    if mode == "top-left":
        return (10, 10)
    elif mode == "top-right":
        return (base_w - wm_w - 10, 10)
    elif mode == "bottom-left":
        return (10, base_h - wm_h - 10)
    elif mode == "bottom-right":
        return (base_w - wm_w - 10, base_h - wm_h - 10)
    elif mode == "center":
        return ((base_w - wm_w) // 2, (base_h - wm_h) // 2)
    else:
        return (10, 10)  # default fallback


def add_watermark(folder_path, watermark_path, position_mode, scale, opacity):
    """Apply watermark to all images in the folder."""
    image_files = load_images(folder_path)
    if not image_files:
        print("No images found in the folder.")
        return
    
    # Load watermark
    watermark = Image.open(watermark_path).convert("RGBA")
    watermark = apply_opacity(watermark, opacity)

    for filename in image_files:
        input_path = os.path.join(folder_path, filename)
        output_path = os.path.join(folder_path, f"wm_{filename}")

        try:
            with Image.open(input_path) as base:
                base = base.convert("RGBA")

                # Scale watermark
                wm_w = int(base.width * scale)
                wm_ratio = wm_w / watermark.width
                wm_h = int(watermark.height * wm_ratio)
                wm_resized = watermark.resize((wm_w, wm_h), Image.LANCZOS)

                # Calculate position
                pos = calculate_position(base.size, wm_resized.size, position_mode)

                # Apply watermark
                base.paste(wm_resized, pos, wm_resized)

                # Save output
                base.convert("RGB").save(output_path)
                print(f"Watermark applied: {output_path}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python watermark.py <folder_path> <watermark_path> <position> <scale> <opacity>")
        print("Positions: top-left, top-right, bottom-left, bottom-right, center")
        sys.exit(1)

    folder = sys.argv[1]
    watermark = sys.argv[2]
    position = sys.argv[3]
    scale = float(sys.argv[4])
    opacity = int(sys.argv[5])

    add_watermark(folder, watermark, position, scale, opacity)

# python S01-L080-pillow-tool-watermark.py ./dogs ./dogs_wm/logo.png bottom-right 0.25 180