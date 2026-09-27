# MotionSites Design

一个可安装、可调用、可验证的 Codex 前端设计 Skill。它把“参考一个好看的动态网站”转成完整工作流：理解产品约束、检索设计方向、建立视觉系统、实现响应式页面、完成可访问性与浏览器验收。

它不复制第三方网站，也不替换业务逻辑。默认自带 8 套原创离线设计方向，安装后无需联网即可使用。

## 能解决什么

- 重设计已有后台、AI Chat、SaaS、数据看板和工作台，同时保留路由、权限、接口、字段和交互功能。
- 从一句需求开始设计新的落地页、产品页、电商页、作品集或工具界面。
- 从设计目录选择明确方向，减少“AI 自己瞎编”和千篇一律的模板感。
- 把设计质量落实到代码、响应式、键盘操作、减少动态效果和浏览器检查，而不只输出描述。

## 核心特点

- **安装即用：** `$motionsites-design` 可显式调用，也允许 Codex 在相关任务中自动选择。
- **离线优先：** 8 套原创 starter patterns 随 Skill 提供。
- **可选目录同步：** 只同步公开元数据和索引，不批量下载提示词、图片或视频。
- **版权边界清晰：** 外部条目只用于发现方向，不克隆页面、不绕过付费或权限。
- **可验证交付：** 内置功能、响应式、可访问性、运行时和交接检查清单。
- **零 pip 依赖：** 命令行工具使用 Python 标准库；若本机 Python 证书链不可用，会安全回退到系统 `curl`。

## 5 分钟安装

要求：Python 3.10+，以及支持 Skills 的 Codex。

```bash
git clone https://github.com/yanghongliang1010-stack/motionsites-design.git
cd motionsites-design
python3 scripts/install_skill.py
```

重启 Codex 后直接输入：

```text
$motionsites-design 帮我重新设计当前后台页面，保留所有业务功能，先选择设计方向再实现并验证。
```

更新版本：

```bash
git pull
python3 scripts/install_skill.py --force
```

卸载只需移除 `~/.codex/skills/motionsites-design`。如果你使用完整插件方式安装，请通过 Codex 的插件管理界面或相应插件命令卸载。

> GitHub 仓库发布前，也可从本地源码目录运行同一个安装命令。

## 使用示例

### 重设计现有产品

```text
$motionsites-design 重构这个 AI 问答工作台。不要改变业务逻辑、接口和权限；保留导航、会话历史、消息、快捷问题和输入工具。目标是企业级、紧凑、清晰，完成桌面和移动端验证。
```

### 从需求创建页面

```text
$motionsites-design 为 B2B 数据分析产品设计一个 1440px 首页。受众是运营负责人，需要突出异常发现、行动建议和可信证据，并实现响应式页面。
```

### 只做审查

```text
$motionsites-design 审查当前页面的信息层级、密度、响应式和动态效果。先给基于截图的证据，不要直接修改代码。
```

更多提示词和完整流程见 [使用手册](docs/USAGE.md)。

## 目录工具

```bash
# 检查安装和离线目录
python3 scripts/motionsites_catalog.py doctor

# 搜索原创方向
python3 scripts/motionsites_catalog.py search "enterprise AI workspace"

# 查看完整方向
python3 scripts/motionsites_catalog.py show ai-operations-cockpit

# 可选：同步公开元数据和文本索引，不下载正文或媒体
python3 scripts/motionsites_catalog.py sync

# 明确需要时才取一个公开索引对应的提示词正文
python3 scripts/motionsites_catalog.py prompt <id> --allow-remote
```

远程同步不是 Skill 正常工作的前提。网络不可用时，Codex 会继续使用原创离线方向。

## 项目结构

```text
motionsites-design/
├── .codex-plugin/plugin.json
├── skills/motionsites-design/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── assets/starter-patterns.json
│   └── references/
├── scripts/
│   ├── install_skill.py
│   └── motionsites_catalog.py
├── tests/
└── docs/
```

## 验证

```bash
python3 -m unittest discover -s tests -v
python3 scripts/motionsites_catalog.py doctor --json
python3 scripts/motionsites_catalog.py search "enterprise AI workspace" --json
```

GitHub Actions 会在 push 和 pull request 时执行同一组离线测试。

## 开源与第三方内容

本项目原创代码、Skill 指令和 starter patterns 使用 [MIT License](LICENSE)。可选 `sync` 数据来自公开的 [MotionSites 开源镜像](https://github.com/zhaosenlin12-creator/MotionSites)，但其中单条提示词和媒体可能保留原作者权利；它们不会被打包进本项目。详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

本项目与 MotionSites 无隶属或官方合作关系。

## 参与贡献

欢迎提交原创设计方向、验证规则、文档和安全改进。请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。不要提交付费内容、复制页面、第三方媒体或密钥。

English documentation: [README.en.md](README.en.md)
