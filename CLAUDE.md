# CMP Lab Skills Marketplace

Claude Code 技能市场 - CMP Lab 专用的技能集合仓库。

## 项目说明

本仓库用于管理和分发 CMP Lab 开发的 Claude Code 技能（skills）。

## 技能结构

每个技能位于 `skills/` 目录下，必须包含 `SKILL.md` 文件：

```
skills/
├── skill-name/
│   ├── SKILL.md          # 必需 - 技能定义文件
│   ├── README.md         # 可选 - 详细说明文档
│   └── scripts/          # 可选 - 辅助脚本
```

## 创建新技能

**重要：创建新技能时，请使用官方的 `skill-creator` skill**

```
/skill-creator
```

该 skill 会帮助您：
- 生成符合规范的 SKILL.md 文件
- 优化技能描述以获得更好的触发准确性
- 提供技能开发的最佳实践

### 手动创建技能（仅在必要时）

1. 在 `skills/` 目录下创建新文件夹
2. 创建 `SKILL.md` 文件，包含以下 frontmatter：
   ```markdown
   ---
   description: 技能的简短描述（用于触发匹配）
   name: skill-name
   ---

   # 技能标题

   ## 技能描述
   ...
   ```

## 技能规范

### SKILL.md 要求
- 必须包含 frontmatter（description 和 name）
- description 应清晰描述技能功能，便于触发匹配
- 使用中文编写内容
- 明确说明使用的 MCP 工具

### 命名规范
- 文件夹名：使用小写字母和连字符，如 `paper-interprept`
- 技能名（name）：使用下划线，如 `paper_interprept`
- 调用方式：`/skill-name`（使用连字符）

## 依赖要求

本仓库中的技能可能依赖以下 MCP 服务器：
- `pubmed-mcp-server` - PubMed 文献检索
- `zotero` - 本地文献管理

## 许可证

本项目采用木兰宽松许可证第2版 (Mulan PSL v2)。
