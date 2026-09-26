import os
import sys
import random
from PIL import Image

def load_images(folder_path):
    """Load all images from the given folder."""
    images = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            try:
                img = Image.open(os.path.join(folder_path, filename))
                images.append(img)
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return images


def layout_grid(images, canvas_size):
    """Arrange images in a simple grid layout."""
    canvas_w, canvas_h = canvas_size
    count = len(images)
    cols = int(count ** 0.5)
    rows = (count + cols - 1) // cols

    cell_w = canvas_w // cols
    cell_h = canvas_h // rows

    positions = []
    index = 0

    for r in range(rows):
        for c in range(cols):
            if index >= count:
                break

            x = c * cell_w
            y = r * cell_h
            positions.append((index, (x, y, cell_w, cell_h)))
            index += 1

            # x = int(c * cell_w + random.uniform(-0.25 * cell_w, 0.25 * cell_w))
            # y = int(r * cell_h + random.uniform(-0.25 * cell_h, 0.25 * cell_h))
            # cell_w_rand = int(cell_w + random.uniform(-0.25 * cell_w, 0.25 * cell_w))
            # cell_h_rand = int(cell_h + random.uniform(-0.25 * cell_h, 0.25 * cell_h))
            # positions.append((index, (x, y, cell_w_rand, cell_h_rand)))
            # index += 1
    return positions


def layout_horizontal(images, canvas_size):
    """Arrange images horizontally across the canvas."""
    canvas_w, canvas_h = canvas_size
    count = len(images)
    cell_w = canvas_w // count
    cell_h = canvas_h

    positions = []
    for i in range(count):
        x = i * cell_w
        y = 0
        positions.append((i, (x, y, cell_w, cell_h)))

    return positions


def layout_vertical(images, canvas_size):
    """Arrange images vertically across the canvas."""
    canvas_w, canvas_h = canvas_size
    count = len(images)
    cell_w = canvas_w
    cell_h = canvas_h // count

    positions = []
    for i in range(count):
        x = 0
        y = i * cell_h
        positions.append((i, (x, y, cell_w, cell_h)))

    return positions


def create_collage(folder_path, canvas_width, canvas_height, mode="grid"):
    """Create a collage from images in the folder using the selected layout mode."""
    images = load_images(folder_path)
    if not images:
        print("No images found in the folder.")
        return

    random.shuffle(images)
    canvas = Image.new("RGB", (canvas_width, canvas_height), (255, 255, 255))

    if mode == "grid":
        positions = layout_grid(images, (canvas_width, canvas_height))
    elif mode == "horizontal":
        positions = layout_horizontal(images, (canvas_width, canvas_height))
    elif mode == "vertical":
        positions = layout_vertical(images, (canvas_width, canvas_height))
    else:
        print("Unknown layout mode. Use: grid, horizontal, vertical.")
        return

    for index, (x, y, w, h) in positions:
        img = images[index].copy()
        img.thumbnail((w, h))
        canvas.paste(img, (x, y))

    output_path = os.path.join(folder_path, "collage_output.jpg")
    canvas.save(output_path)
    print(f"Collage saved as: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) not in (4, 5):
        print("Usage: python collage.py <folder_path> <canvas_width> <canvas_height> [mode]")
        print("Modes: grid (default), horizontal, vertical")
        sys.exit(1)

    folder = sys.argv[1]
    width = int(sys.argv[2])
    height = int(sys.argv[3])
    mode = sys.argv[4] if len(sys.argv) == 5 else "grid"

    create_collage(folder, width, height, mode)


# python c:\code\S01-L070-pillow-tool-collage.py .\dogs 100 1000 vertical
# python c:\code\S01-L070-pillow-tool-collage.py .\dogs 1200 80 horizontal 
# python c:\code\S01-L070-pillow-tool-collage.py .\dogs 1400 1080  grid 