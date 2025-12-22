import os
from pathlib import Path
from PIL import Image

# -----------------------------
# CONFIGURATION
# -----------------------------
IMAGE_FOLDER = r""  # <-- FILL THIS IN

MAX_FILE_SIZE_BYTES = int(1.9 * 1024 * 1024)  # ~1.9 MB
MAX_DIMENSION = 2000
VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"}
# -----------------------------


def validate_folder(path_str: str) -> Path:
    if not path_str or path_str.strip() == "":
        raise ValueError(
            "ERROR: IMAGE_FOLDER is empty. Please fill in a valid path.")

    folder = Path(path_str)

    if not folder.exists():
        raise FileNotFoundError(
            f"ERROR: IMAGE_FOLDER does not exist: {folder}")

    if not folder.is_dir():
        raise NotADirectoryError(
            f"ERROR: IMAGE_FOLDER is not a directory: {folder}")

    return folder


def should_process_image(path: Path) -> bool:
    return path.suffix.lower() in VALID_EXTENSIONS and path.is_file()


def resize_down_to_target(img: Image.Image, target_size_bytes: int, ext: str) -> Image.Image:
    """
    Iteratively reduces image size until file is <= target_size_bytes.
    Uses decreasing scale factors but preserves aspect ratio.
    """
    scale_factor = 0.9  # Start by shrinking 10%
    current = img

    while True:
        temp_path = Path("_temp_resize_output" + ext)
        save_kwargs = {}

        if ext in {".jpg", ".jpeg"}:
            save_kwargs.update({"quality": 85, "optimize": True})
        elif ext == ".png":
            save_kwargs.update({"optimize": True})

        current.save(temp_path, **save_kwargs)
        current_size = temp_path.stat().st_size

        if current_size <= target_size_bytes:
            temp_path.unlink(missing_ok=True)
            return current

        # Shrink again
        w, h = current.size
        new_w = int(w * scale_factor)
        new_h = int(h * scale_factor)

        # Safety prevent over-shrinking to zero
        if new_w < 50 or new_h < 50:
            temp_path.unlink(missing_ok=True)
            return current

        current = current.resize((new_w, new_h), Image.LANCZOS)

        temp_path.unlink(missing_ok=True)


def resize_image_if_needed(img_path: Path, output_dir: Path) -> None:
    file_size = img_path.stat().st_size

    with Image.open(img_path) as img:
        width, height = img.size
        ext = img_path.suffix.lower()

        too_large_in_pixels = width > MAX_DIMENSION or height > MAX_DIMENSION
        too_large_in_bytes = file_size > MAX_FILE_SIZE_BYTES

        if not (too_large_in_pixels or too_large_in_bytes):
            print(f"SKIP: {img_path.name} (OK)")
            return

        # -----------------------
        # Step 1: Enforce max dimensions
        # -----------------------
        scale_factor = min(MAX_DIMENSION / width, MAX_DIMENSION / height, 1.0)

        if scale_factor < 1.0:
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            print(
                f"DIMENSION RESIZE: {img_path.name} "
                f"{width}x{height} -> {new_width}x{new_height}"
            )
            img = img.resize((new_width, new_height), Image.LANCZOS)

        # -----------------------
        # Step 2: Shrink to target file size (~1.9 MB)
        # -----------------------
        print(
            f"SIZE CHECK: {img_path.name} ({file_size/1024:.1f} KB) -> target 1900 KB")

        img = resize_down_to_target(img, MAX_FILE_SIZE_BYTES, ext)

        # -----------------------
        # Save output
        # -----------------------
        output_dir.mkdir(parents=True, exist_ok=True)
        out_path = output_dir / img_path.name

        save_kwargs = {}
        if ext in {".jpg", ".jpeg"}:
            save_kwargs.update({"quality": 85, "optimize": True})
        elif ext == ".png":
            save_kwargs.update({"optimize": True})

        img.save(out_path, **save_kwargs)

        new_size = out_path.stat().st_size
        print(f" -> FINAL: {out_path.name} = {new_size/1024:.1f} KB")


def process_folder(folder: Path) -> None:
    output_dir = folder / "resized"

    for entry in folder.iterdir():
        if should_process_image(entry):
            resize_image_if_needed(entry, output_dir)


def main():
    folder = validate_folder(IMAGE_FOLDER)
    process_folder(folder)


if __name__ == "__main__":
    main()
