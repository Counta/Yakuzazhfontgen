# Yakuzazhfontgen
a series of python that generates yakuza fonts for kiwami engine

两个Python小程序，生成极引擎可用的繁体中文字体文件

如果你用我库里的繁转简字体工具，就能给自己生成简体字体

## 所需文件

你需要一个Big5到Unicode的码表，它的名字应该是 `b2u.txt`

你需要你用于生成字体的文件，你得在代码里改改字体

## How to Use
使用[Partool](https://github.com/Kaplas80/ParManager)之类的工具解包font.par，然后解包出字体的dds。进行替换后再打包

生成dds使用微软的[DirectXTex](https://github.com/microsoft/DirectXTex/wiki/texconv)工具，字体应使用DXT5压缩，单层mipmap

或者解包后按照目录替换文件，打包成Shin Ryu Mod Manager可用的Mod zip包

enjoy
