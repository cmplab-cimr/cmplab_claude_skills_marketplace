# CMP Lab Skills Marketplace

Claude Code 技能市场 - CMP Lab 专用的技能集合。

## 快速开始

### 步骤 1：安装官方技能 marketplace（推荐）

首先安装 Anthropic 官方的技能 marketplace 和 skill，获取更多强大的技能支持：

```bash
# 添加官方 marketplace
/plugin marketplace add anthropics/skills
```

然后安装官方技能包：

```bash
# 安装文档处理技能（PDF、Word、Excel、PPT等）
/plugin install document-skills@anthropic-agent-skills

# 安装示例技能（设计、开发、企业等场景）
/plugin install example-skills@anthropic-agent-skills
```

安装后即可使用官方技能，例如：
- "Use the PDF skill to extract text from `document.pdf`"
- "Create a Word document with..."
- "Use skill-creator to create a new skill"

### 步骤 2：克隆本仓库

```bash
git clone git@github.com:cmplab-cimr/cmplab_claude_skills_marketplace.git
```

## 可用技能

| 技能名称 | 描述 | 使用方式 |
|---------|------|---------|
| paper_interpret | 学术论文解读技能 | `/paper-interpret` |
| pubmed-topic-search | PubMed主题文献搜索 | `/pubmed-topic-search` |
| notion-save-to-project | 将对话输出保存到 Notion 课题项目 | `/notion-save-to-project` |

## 安装方法

### 方式一：复制到本地skills目录

将所需技能目录复制到 Claude Code 的 skills 目录：

```bash
# 进入仓库目录
cd cmplab_claude_skills_marketplace

# 复制单个技能
cp -r skills/paper_interpret ~/.claude/skills/

# 或复制所有技能
cp -r skills/* ~/.claude/skills/
```

### 方式二：配置为marketplace

在 `~/.claude/settings.json` 中添加：

```json
{
  "marketplaces": [
    {
      "name": "cmplab-skills",
      "path": "/path/to/cmplab_claude_skills_marketplace"
    }
  ]
}
```

## 技能详细说明

### paper_interpret - 学术论文解读

通过PubMed在线检索（DOI或标题）查找指定文章，或直接解读本地PDF文章，用严谨、科学的语言解读文章所有要点。

**使用示例：**
```
/paper-interpret --doi 10.1038/s42003-022-04242-7
/paper-interpret --title "GIPR Is Predominantly Localized..."
/paper-interpret --pmid 35907261
/paper-interpret --file "path/to/article.pdf"
```

### pubmed-topic-search - PubMed主题文献搜索

用户指定一个中文主题，自动翻译成英语后，在PubMed上搜索相关文章，并以中英文双语格式输出。

**使用示例：**
```
/pubmed-topic-search GIPR在人体不同组织和器官中的表达
/pubmed-topic-search 胰高血糖素受体
```

### notion-save-to-project - Notion 课题项目保存

将 Claude 对话中的完整输出保存到用户的 Notion 课题项目数据库中。自动探测课题项目的 database 结构，根据内容类型智能匹配最合适的 database，并自动填充属性（标题、标签、日期、状态等）。核心原则：绝不精简、截断任何内容。

**使用示例：**
```
/notion-save-to-project
保存到 Notion
把这个存到课题项目
```

也可通过自然语言触发：
- "保存到 Notion"、"存到课题项目"
- "记录下来"、"帮我记到 Notion"
- "把这个存一下"

## 依赖要求

### MCP 服务器

- `pubmed-mcp-server` - PubMed 文献检索
- `zotero` - 本地文献管理（可选）
- `notion` - Notion 工作空间管理（用于 notion-save-to-project 技能）

## 目录结构

```
cmplab_claude_skills_marketplace/
├── README.md                           # 本说明文件
├── skills/
│   ├── paper_interpret/                # 论文解读技能
│   │   ├── SKILL.md                    # 技能定义
│   │   ├── README.md                   # 详细说明
│   │   ├── parse_paper_fulltext.py     # 全文解析脚本
│   │   └── auto_extract_fulltext.py    # 自动提取脚本
│   └── pubmed-topic-search/            # PubMed主题搜索技能
│       └── SKILL.md                    # 技能定义
│   └── notion-save-to-project/         # Notion课题项目保存技能
│       └── SKILL.md                    # 技能定义
└── LICENSE                             # 许可证
```

## 创建新技能

### 推荐方式：使用 skill-creator

**推荐使用官方的 `skill-creator` skill 来创建新技能**，它可以：

- 生成符合规范的 SKILL.md 文件
- 优化技能描述以获得更好的触发准确性
- 提供技能开发的最佳实践

```bash
# 在项目目录下调用
/skill-creator
```

按照提示操作，将生成的技能文件放入 `skills/` 目录即可。

### 手动创建技能

如果需要手动创建，请遵循以下规范：

1. **创建目录结构**
   ```bash
   mkdir skills/your-skill-name
   ```

2. **创建 SKILL.md 文件**（必需）
   ```markdown
   ---
   description: 技能的简短描述（用于触发匹配）
   name: skill_name
   ---

   # 技能标题

   ## 技能描述
   详细描述技能的功能和使用场景...

   ## 使用方法
   ...

   ## 使用的 MCP 工具
   ...
   ```

3. **命名规范**
   - 目录名：小写字母 + 连字符，如 `my-skill`
   - 技能名（name）：小写字母 + 下划线，如 `my_skill`
   - 调用方式：`/my-skill`（使用连字符）

4. **可选文件**
   - `README.md` - 详细说明文档
   - `scripts/` - 辅助脚本目录

## 贡献

欢迎提交新的技能或改进现有技能！

1. Fork 本仓库
2. 使用 `/skill-creator` 创建新技能（推荐）
3. 将技能放入 `skills/` 目录
4. 提交 Pull Request

## 许可证

[木兰宽松许可证 第2版 (Mulan PSL v2)](./LICENSE)
