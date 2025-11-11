import os
import subprocess

def convert_png_to_dds(input_folder, output_folder, texconv_path="texconv.exe"):
    """
    使用巨硬的texconv工具把文件夹下的png全部转成dds.

    :param input_folder: Path to the folder containing PNG files.
    :param output_folder: Path to the folder where DDS files will be saved.
    :param texconv_path: Path to the texconv executable.
    """
    if not os.path.exists(texconv_path):
        raise FileNotFoundError(f"texconv tool not found at {texconv_path}")

    if not os.path.exists(input_folder):
        raise FileNotFoundError(f"Input folder not found: {input_folder}")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith(".png"):
            input_file = os.path.join(input_folder, file_name)
            output_file = os.path.join(output_folder, os.path.splitext(file_name)[0] + ".dds")

            # Build texconv command
            command = [
                texconv_path,
                "-f", "DXT5",  # 字体用DXT5压缩
                "-m", "1",     # 一层mipmap
                "-w", "512",   # 宽512
                "-h", "512",   # 高512
                "-o", output_folder,  # 输出文件夹
                input_file     # 输入的文件
            ]

            try:
                print(f"Converting {input_file} to {output_file}...")
                subprocess.run(command, check=True)
                print(f"Conversion complete: {output_file}")
            except subprocess.CalledProcessError as e:
                print(f"Error converting {input_file}: {e}")

# 示例
input_folder = "./png_files"  # 换成你自己的目录
output_folder = "./dds_files"  # 换成你想要的目录
convert_png_to_dds(input_folder, output_folder)
