import os
import sys
from PIL import Image

def convert_images(folder_path, source_ext, target_ext):
    """
    Convert all images in a folder from one format to another using Pillow.

    Parameters:
        folder_path (str): Path to the directory containing images.
        source_ext (str): Source file extension (e.g. "jpg").
        target_ext (str): Target file extension (e.g. "png").
    """

    # Normalize extensions (remove leading dots if present)
    source_ext = source_ext.lower().lstrip(".")
    target_ext = target_ext.lower().lstrip(".")

    # Iterate through all files in the directory
    for filename in os.listdir(folder_path):
        if filename.lower().endswith("." + source_ext):
            source_file = os.path.join(folder_path, filename)

            # Build output filename
            base_name = os.path.splitext(filename)[0]
            target_file = os.path.join(folder_path, base_name + "." + target_ext)

            try:
                # Open and convert the image
                with Image.open(source_file) as img:
                    img.convert("RGB").save(target_file)
                print(f"Converted: {source_file} -> {target_file}")
            except Exception as e:
                print(f"Error converting {source_file}: {e}")


if __name__ == "__main__":
    # Expecting 3 arguments: folder, source type, target type
    if len(sys.argv) != 4:
        print("Usage: python convert.py <folder_path> <source_ext> <target_ext>")
        sys.exit(1)

    folder = sys.argv[1]
    source = sys.argv[2]
    target = sys.argv[3]

    convert_images(folder, source, target)

# python S01-L050-pillow-tool-convert.py ./dogs jpg png
