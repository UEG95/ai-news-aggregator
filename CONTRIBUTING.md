# 贡献指南

感谢您对AI新闻聚合器项目的关注！我们欢迎各种形式的贡献，包括但不限于：

- 报告问题
- 提交功能请求
- 编写文档
- 提交代码改进

## 如何贡献

1. Fork 这个仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的改动 (`git commit -m '添加一些特性'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 开发环境设置

1. 克隆仓库：
```bash
git clone https://github.com/UEG95/ai-news-aggregator.git
cd ai-news-aggregator
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 代码风格指南

- 遵循 PEP 8 规范
- 使用有意义的变量和函数名
- 添加适当的注释
- 保持代码简洁明了

## 提交 Pull Request 前的检查清单

- [ ] 代码符合项目的代码风格指南
- [ ] 添加/更新了相关的测试
- [ ] 更新了相关的文档
- [ ] 所有测试都通过了
- [ ] 本地运行 flake8 检查没有错误

## 问题报告指南

创建 issue 时，请包含以下信息：

1. 问题描述
2. 复现步骤
3. 预期行为
4. 实际行为
5. 截图（如果适用）
6. 系统环境信息
   - 操作系统
   - Python 版本
   - 相关依赖包版本

## 分支命名约定

- `feature/*`: 新功能
- `bugfix/*`: 错误修复
- `docs/*`: 文档更新
- `test/*`: 测试相关
- `refactor/*`: 代码重构

## 提交信息规范

使用清晰的提交信息，格式如下：

```
类型: 简短的描述

详细的说明（如果需要）
```

类型可以是：
- `feat`: 新功能
- `fix`: 错误修复
- `docs`: 文档更改
- `style`: 代码格式化
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

## 许可证

通过提交 pull request，您同意您的贡献将在 MIT 许可证下发布。 