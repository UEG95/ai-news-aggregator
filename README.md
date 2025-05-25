# AI新闻聚合器

[![Python Application](https://github.com/你的用户名/ai-news-aggregator/actions/workflows/python-app.yml/badge.svg)](https://github.com/你的用户名/ai-news-aggregator/actions/workflows/python-app.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

一个使用Python开发的AI新闻聚合器，支持多个新闻源的实时新闻获取和过滤。

## 功能特点

- 多新闻源支持（新浪科技、36氪）
- 现代化GUI界面（使用arc主题）
- 实时新闻搜索过滤
- 可点击的新闻链接
- 代理设置支持
- 新闻来源和时间显示

## 界面预览

![主界面预览](screenshots/main.png)

*注意：请运行程序并截图，将截图保存到 screenshots 目录下的 main.png*

主要特点：
- 窗口大小：1200x800
- 使用微软雅黑字体
- 整洁的布局设计
- 现代化arc主题

## 安装要求

- Python 3.6+
- 依赖包：
  ```
  requests>=2.31.0
  beautifulsoup4>=4.12.0
  lxml>=4.9.0
  ttkthemes>=3.2.2
  ```

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/你的用户名/ai-news-aggregator.git
cd ai-news-aggregator
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

运行程序：
```bash
python news_aggregator.py
```

### 基本操作

1. 切换新闻源：使用顶部下拉菜单选择不同的新闻源
2. 刷新新闻：点击"刷新新闻"按钮
3. 搜索过滤：在搜索框中输入关键词进行实时过滤
4. 查看新闻：点击新闻链接在浏览器中打开
5. 代理设置：点击"设置代理"按钮配置代理服务器

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