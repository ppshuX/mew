from PIL import Image
import os

# 目标目录
avatar_dir = 'media/avatars'
# 支持的图片格式
exts = ('.jpg', '.jpeg', '.png')
# 压缩参数
max_size = 256  # 最大宽高像素
quality = 80    # JPEG压缩质量

for filename in os.listdir(avatar_dir):
    if filename.lower().endswith(exts):
        path = os.path.join(avatar_dir, filename)
        try:
            img = Image.open(path)
            # 等比例缩放
            if max(img.size) > max_size:
                ratio = max_size / max(img.size)
                new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            # 转为RGB（防止PNG透明背景报错）
            img = img.convert('RGB')
            # 统一保存为JPEG，覆盖原文件
            img.save(path, format='JPEG', quality=quality)
        except Exception as e:
            pass

print("全部处理完成！") 