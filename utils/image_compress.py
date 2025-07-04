from PIL import Image

def compress_image(image_path, quality=80):
    try:
        img = Image.open(image_path)
        if img.format in ['JPEG', 'JPG', 'PNG']:
            img.save(image_path, quality=quality, optimize=True)
    except Exception:
        pass
