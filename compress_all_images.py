import os
from utils.image_compress import compress_image

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')

# 支持的图片扩展名
IMAGE_EXTS = ['.jpg', '.jpeg', '.png']

def compress_all_images(root=MEDIA_ROOT, quality=80):
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            ext = os.path.splitext(filename)[-1].lower()
            if ext in IMAGE_EXTS:
                img_path = os.path.join(dirpath, filename)
                compress_image(img_path, quality=quality)

if __name__ == '__main__':
    compress_all_images()
    print('所有图片已批量压缩完成！') 