# AI新闻聚合器

[![Python Application](https://github.com/你的用户名/ai-news-aggregator/actions/workflows/python-app.yml/badge.svg)](https://github.com/你的用户名/ai-news-aggregator/actions/workflows/python-app.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

一个基于Python的AI新闻聚合器，支持多个新闻源的AI相关新闻获取和展示。

## 功能特点

- 多新闻源支持：
  - 必应新闻
  - Google新闻
  - 新浪科技
  - 36氪
  - 量子位
- 美观的图形用户界面
- 支持代理设置
- 新闻预览和详细阅读
- 自动刷新功能
- 详细的错误日志记录

## 界面预览

![主界面预览](screenshots/main.png)

*注意：请运行程序并截图，将截图保存到 screenshots 目录下的 main.png*

主要特点：
- 窗口大小：1200x800
- 使用微软雅黑字体
- 整洁的布局设计
- 现代化arc主题

## 安装要求

- Python 3.7+
- tkinter (通常随Python一起安装)
- 其他依赖项见 `requirements.txt`

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/[你的用户名]/ai-news-aggregator.git
cd ai-news-aggregator
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

1. 运行主程序：
```bash
python ai_news_app.py
```

2. 在界面中选择需要的新闻源
3. 点击"刷新"按钮获取最新新闻
4. 点击新闻标题查看详细内容

## 代理设置

如果需要访问Google新闻，可以在设置中配置代理：

1. 点击"设置"按钮
2. 输入代理服务器地址和端口
3. 点击"保存"确认设置

## 故障排除

如果遇到问题：

1. 检查 `news_aggregator.log` 文件中的错误信息
2. 确保所有依赖都已正确安装
3. 检查网络连接是否正常
4. 如果使用代理，确保代理设置正确

## 开发

### 运行测试

```bash
python -m unittest test_news_aggregator.py
```

### 代码质量

本项目使用 flake8 进行代码质量检查：

```bash
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

## 贡献

欢迎提交 Pull Requests 来改进这个项目。对于重大更改，请先开一个 issue 讨论您想要改变的内容。

## 版权信息

© 2024 UEG95，保留所有权利

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情 