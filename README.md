# Flit Watermark Tool (FWT)

轻量级跨平台图片水印编辑器，支持交互式文字水印的拖拽、旋转、缩放及样式调节，提供实时预览与中英文界面。

## 功能

- 交互式编辑：在预览画布上直接拖动、旋转和缩放水印文字。
- 参数调节：修改文字内容、字体、字号、不透明度、旋转角度和颜色。
- 输出缩放：生成图片时可选择 100%、50%、20% 的缩放比例。
- 实时预览：调整参数立即反映在画布上。
- 系统字体：自动列出当前系统可用字体，支持多语言文字显示。
- 多语言：启动时根据系统语言自动选择中文或英文，菜单可随时切换。
- 快捷操作：一键保存为 JPEG，复制到剪贴板，打开输出目录。

## 依赖与运行

需要 Python 3.8+，安装依赖：


pip install PyQt5 Pillow

进入项目根目录，执行：


python main.py


Linux 用户可能需要通过包管理器安装 PyQt5（例如 `apt install python3-pyqt5`）。

## 语言切换

程序启动时自动检测系统语言，中文用户会看到中文界面，其他环境默认英文。运行过程中可通过菜单 `Language` -> `中文` / `English` 切换，所有界面文字即时更新。

## 文件结构

- `main.py`          主程序入口
- `core/`            水印核心逻辑、字体管理、数据模型
- `ui/`              图形界面组件（调整面板、交互预览、底部状态栏）
- `localization/`    多语言字符串定义
- `run_gui.sh`       可选的自动虚拟环境启动脚本

## 许可证

MIT License

## 开发计划

当前版本处于活跃开发阶段，部分功能尚未稳定，可编译尝试已有交互与生成功能。

接下来的工作：

1. 修复拖拽缩放，支持在编辑框内按住旋转
2. 恢复多文件格式输出功能
3. 增加模版功能
4. 恢复间距与行数调节
5. 翻新 UI 界面
6. 翻新教程文档
7. 发布多平台 Release

## 功能与核心实现

| 功能 | 函数/类 | 文件 |
|------|---------|------|
| 水印参数封装 | `WatermarkParams` | `core/watermark_core.py` |
| 图片水印渲染 | `apply_watermark` | `core/watermark_core.py` |
| 系统字体扫描 | `scan_fonts` | `core/font_manager.py` |
| 字体文件加载 | `load_font` | `core/font_manager.py` |
| 主文字数据模型 | `WatermarkElement` | `core/watermark_element.py` |
| 调整面板控件与参数读写 | `AdjustmentPanel` | `ui/adjustment_panel.py` |
| 交互式预览画布 | `InteractivePreviewWidget` | `ui/interactive_preview.py` |
| 画布可编辑文本项 | `WatermarkSimpleItem` | `ui/interactive_preview.py` |
| 预览面板容器 | `PreviewPanel` | `ui/preview_panel.py` |
| 底部信息栏 | `FooterBar` | `ui/footer_bar.py` |
| 多语言管理（设置与翻译） | `set_language`, `tr` | `localization/__init__.py` |
| 应用主窗口 | `MainWindow` | `main.py` |

## 待完善跨平台事项

- Windows/Linux 系统字体路径适配（当前仅扫描 macOS 常用目录，其他平台默认列表为空）。
- 虚拟环境启动脚本 `run_gui.sh` 仅适用于 macOS/Linux，Windows 环境下需额外编写 `.bat` 脚本或手动运行。
- 多格式输出及部分高级编辑功能尚在开发中，跨平台行为尚未验证。
