# About

Program that loops over all images in a given folder

If an image is larger than 2 MB or any side is > 2000 px, it:

- Resizes it proportionally (keeps aspect ratio)
- Image goes down to ~1.9MB as a baseline
- Ensures no side exceeds 2000 px

# How to run

1. Install Pillow if you don’t have it yet. Provides file format support, including image processing.
    pip install pillow

2. Run the file 🚀
    python resize_images.py