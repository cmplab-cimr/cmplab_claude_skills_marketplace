# 论文解读技能（paper_interpret）

## 概述

本技能通过 PubMed 在线检索（DOI或标题）查找指定文章，或直接解读本地PDF文章，用严谨、科学的语言解读文章所有要点，并输出到markdown文件中。

## 功能特点

1. **多来源检索**：支持 DOI、标题、PMID 和本地PDF文件
2. **智能全文处理**：自动处理从 Zotero 获取的 JSON 格式全文
3. **章节识别**：自动提取文章章节结构
4. **双语输出**：中文解读，markdown格式
5. **全文保存**：同时生成txt格式全文文件

## 安装要求

### 必需的 Python 包
- Python 3.6+
- 无额外依赖（仅使用标准库）

### 系统工具
- `pdftotext`（处理PDF文件时需要）
  - Windows: `choco install poppler`
  - macOS: `brew install poppler`
  - Linux: `sudo apt-get install poppler-utils`

## 核心脚本

### 1. parse_paper_fulltext.py
主要脚本，用于解析从 Zotero 获取的 JSON 格式全文。

**使用方法：**
```bash
# 基本用法
python parse_paper_fulltext.py zotero_fulltext.json

# 指定输出文件
python parse_paper_fulltext.py zotero_fulltext.json my_article_fulltext.txt
```

**输出文件：**
- `{title}_fulltext.txt` - 结构化的全文内容
- `{title}_summary.txt` - 章节结构摘要

### 2. auto_extract_fulltext.py
自动化脚本，用于在从 Zotero 获取全文后自动调用 parse_paper_fulltext.py。

**使用方法：**
```bash
python auto_extract_fulltext.py
```

**功能：**
- 自动查找最新的 Zotero 全文文件
- 自动调用解析脚本
- 生成格式化的全文文件

### 3. 章节提取功能

自动识别以下章节结构：
- 文章标题
- 摘要（Abstract）
- 数字编号章节（1. Introduction, 2. Methods 等）
- Markdown章节（### Introduction, ## Methods 等）

## 使用示例

### 示例1：通过DOI解读论文
```
/paper-interpret --doi 10.1007/s11154-025-09954-9
```

### 示例2：通过本地PDF文件解读
```
/paper-interpret --file "path/to/article.pdf"
```

### 示例3：手动使用全文提取脚本
```bash
# 1. 从 Zotero 获取全文（在论文解读过程中自动完成）
# 2. 使用解析脚本处理JSON文件
python parse_paper_fulltext.py zotero_fulltext.json

# 3. 查看生成的文件
cat fulltext_extracted.txt
cat fulltext_extracted_summary.txt
```

## 文件结构

```
paper_interpret/
├── SKILL.md                 # 技能说明文档
├── parse_paper_fulltext.py  # 全文解析脚本
├── auto_extract_fulltext.py # 自动提取脚本
└── README.md               # 本说明文件
```

## 输出文件格式

### 1. Markdown 解读文件
包含完整的论文解读：
- 文献基本信息
- 研究背景与科学问题
- 研究方法
- 研究发现
- 科学意义与临床价值
- 展望与未来研究方向
- 结论
- MeSH主题词
- 关键信息总结

### 2. TXT 全文文件
结构化的原文内容：
- 自动识别章节
- 保留原文格式
- UTF-8编码

### 3. 章节摘要文件
- 每章字数统计
- 内容预览
- 章节结构概览

## 故障排除

### 常见问题

1. **找不到 Zotero 全文文件**
   - 确保已正确配置 Zotero MCP 服务器
   - 检查工作区目录结构

2. **JSON 解析失败**
   - 检查 JSON 文件是否损坏
   - 确保 UTF-8 编码

3. **章节提取不完整**
   - 检查章节格式是否符合预期
   - 手动调整章节匹配规则

### 调试模式

在脚本中添加调试信息：
```python
# 在 parse_paper_fulltext.py 中
print(f"Debug: 正在处理文件 {zotero_json_file}")
print(f"Debug: 提取的章节 {len(chapters)}")
```

## 更新日志

### v1.1 (2026-03-04)
- 新增 parse_paper_fulltext.py 脚本
- 新增 auto_extract_fulltext.py 自动化脚本
- 支持章节自动识别和提取
- 生成结构化的全文文件

### v1.0
- 基础论文解读功能
- 支持 PubMed 和 Zotero 检索
- Markdown 格式输出

## 贡献

欢迎提交问题和建议！

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开一个 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。
