import os
import sys
from PIL import Image

def create_thumbnails(folder_path, source_ext, target_ext, scale=1.0):
    """
    Create thumbnails for all images in a folder using Pillow.

    Parameters:
        folder_path (str): Path to the directory containing images.
        source_ext (str): Source file extension (e.g. "jpg").
        target_ext (str): Target file extension (e.g. "png").
        scale (float): Scale factor for the thumbnail size (default 1.0).
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
            target_file = os.path.join(folder_path, f"mini_{base_name}.{target_ext}")

            try:
                with Image.open(source_file) as img:
                    # Calculate thumbnail size
                    width, height = img.size
                    new_size = (int(width * scale), int(height * scale))

                    # Create thumbnail
                    thumbnail = img.copy()
                    thumbnail.thumbnail(new_size)

                    # Save thumbnail
                    thumbnail.save(target_file)
                print(f"Thumbnail created: {target_file}")

            except Exception as e:
                print(f"Error processing {source_file}: {e}")


if __name__ == "__main__":
    # Expecting 4 or 5 arguments: folder, source type, target type, optional scale
    if len(sys.argv) not in (4, 5):
        print("Usage: python thumbnails.py <folder_path> <source_ext> <target_ext> [scale]")
        sys.exit(1)

    folder = sys.argv[1]
    source = sys.argv[2]
    target = sys.argv[3]
    scale = float(sys.argv[4]) if len(sys.argv) == 5 else 1.0

    create_thumbnails(folder, source, target, scale)

# python .\S01-L060-pillow-tool-resize.py ./dogs jpg jpg 0.1