import os
from PIL import Image, ImageDraw, ImageFont

def load_big5_map(map_file="b2u.txt"):
    """加载 Big5 编码到 Unicode 字符的映射表"""
    big5_map = {}
    with open(map_file, "r", encoding="utf-8") as f:
        for line in f.readlines()[1:]:  # 跳过第一行
            parts = line.strip().split()
            if len(parts) == 2:
                big5_code, unicode_code = parts
                big5_code = big5_code[2:]  # 移除前缀 "0x"
                try:
                    char = chr(int(unicode_code, 16))
                    big5_map[big5_code] = char
                except ValueError:
                    continue
    return big5_map

def render_char(font, char, size=32, y_offset=12):
    """渲染单个字符为透明背景的图像，并上移指定的像素偏移量"""
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # 获取文本边界框并计算位置
    bbox = draw.textbbox((0, 0), char, font=font)
    width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((size - width) // 2, (size - height) // 2 - y_offset), char, font=font, fill=(255, 255, 255, 255))

    return image

def is_valid_big5(code):
    """检查 Big5 编码是否有效，跳过 ??00 到 ??3F、??80 到 ??9F，以及 A3C0 到 A3DF 和 A3F0 到 A3FF 区间"""
    lower_byte = int(code[2:], 16)
    high_byte = code[:2].upper()

    # 跳过 ??00 到 ??3F 和 ??80 到 ??9F
    if 0x00 <= lower_byte <= 0x3F or 0x80 <= lower_byte <= 0x9F:
        return False

    # 跳过 A3C0 到 A3DF 和 A3F0 到 A3FF，但保留 A3E?
    if high_byte == "A3" and (0xC0 <= lower_byte <= 0xDF or 0xF0 <= lower_byte <= 0xFF):
        return False

    return True

def generate_characters(start_code, font_path, map_file, output_size=(512, 512), cell_size=32):
    """生成 PNG 图像文件，按照 Big5 编码顺序绘制字符"""
    font = ImageFont.truetype(font_path, size=cell_size)
    big5_map = load_big5_map(map_file)

    # 初始化画布
    image = Image.new("RGBA", output_size, (0, 0, 0, 0))

    current_x, current_y = 0, 0
    start_value = int(start_code, 16)
    end_value = 0xFFFF  # 最大可能值为 0xFFFF，支持连续绘制

    for value in range(start_value, end_value):
        code = f"{value:04X}"

        # 跳过无效 Big5 编码
        if not is_valid_big5(code):
            continue

        if code in big5_map:
            char = big5_map[code]
            char_image = render_char(font, char, size=cell_size)
            image.paste(char_image, (current_x, current_y))

        current_x += cell_size
        if current_x >= output_size[0]:
            current_x = 0
            current_y += cell_size
            if current_y >= output_size[1]:
                break

    return image

def process_input_files(input_folder="input"):
    """检查 input 文件夹，自动提取编码并生成图片"""
    # 获取 input 文件夹中的所有文件
    files = os.listdir(input_folder)
    # 遍历文件，提取编码并生成对应图片
    for file in files:
        if file.startswith("hd_c_zenkaku") and len(file) == 20:  # 假设文件名格式为 hd_c_zenkakuXXXX
            start_code = file[11:15]  # 提取文件名中的 4 位编码
            print(f"处理文件：{file}，提取编码：{start_code}")
            
            # 调用生成图片的函数
            map_file = "b2u.txt" # 需要一个Big5到Unicode的对照表
            font_path = "fontw3.ttf" # 如果你要拿我的项目改字体，记得改改字体文件
            output_filename = f"{start_code}.png"

            print(f"开始生成图片：{output_filename}")
            image = generate_characters(start_code, font_path, map_file)
            image.save(output_filename, "PNG")
            print(f"生成完成：{output_filename}")

def main():
    # 自动处理 input 文件夹中的文件
    process_input_files()

if __name__ == "__main__":
    main()
