# 🖼️ Cover Preview Generator

一键为图片添加半透明水印，生成 50% 分辨率的 JPG 预告图。  
🍎 专为 macOS 设计（兼容 M1/M2），纯本地处理。

## ✨ 功能
- 🖌️ 半透明文字水印，支持中英文
- 📐 分辨率减半，适合预告图
- ⚡ 仅需 Pillow，无网络依赖

## 📦 安装
```bash
pip install Pillow
```
🚀 使用
bash
python watermark_preview.py 图片.jpg
# 自定义
python watermark_preview.py 图片.png -o 预告.jpg --text "抢先看" --font /System/Library/Fonts/PingFang.ttc
📄 许可
MIT License
