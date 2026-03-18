---
description: 解读学术论文的技能（通过PubMed在线检索或本地PDF文件）
name: paper_interpret
---

# 学术论文解读技能

## 技能描述

通过PubMed在线检索（DOI或标题）查找指定文章，或直接解读本地PDF文章，用严谨、科学的语言解读文章所有要点，并输出到markdown文件中。

## 使用方法

调用此技能时，请提供以下参数之一：

### 方式一：通过DOI查找
```
/paper-interpret --doi 10.1038/s42003-022-04242-7
```

### 方式二：通过标题查找
```
/paper-interpret --title "GIPR Is Predominantly Localized to Nonadipocyte Cell Types Within White Adipose Tissue"
```

### 方式三：通过PMID查找
```
/paper-interpret --pmid 35907261
```

### 方式四：通过本地PDF文件
```
/paper-interpret --file "path/to/article.pdf"
```
或
```
/paper-interpret --pdf "path/to/article.pdf"
```

## 执行流程

当用户通过 DOI、标题或 PMID 调用时：

1. **文献检索**
   - 使用 `mcp__pubmed-mcp-server__search_articles` API 根据DOI、标题或PMID查找文章
   - 获取文章的PMID

2. **内容获取与全文确认**
   - 使用 `mcp__pubmed-mcp-server__get_article_details` API 获取文章元数据和摘要
   - 如需获取全文，使用 `mcp__pubmed-mcp-server__get_full_text` API（需要PMCID）
   - 包含：标题、作者、期刊、摘要、全文（如可用）、MeSH主题词等
   - **关键步骤**：检查是否成功获取到文章全文
     - **如果通过 PubMed 成功获取全文**：
       - 直接进入步骤3进行解读
       - 如全文内容过长，采用**分段读取**的方式处理
       - **不再尝试任何其他 MCP 工具**（包括 Zotero、web reader、web search 等）
     - **如果通过 Zotero 成功获取全文**：
       - 调用 parse_paper_fulltext.py 脚本生成 txt 格式全文
       - 使用 sed 命令分段读取生成的 txt 文件
       - 进入步骤3进行解读
       - **不再尝试任何其他 MCP 工具**（包括 web reader、web search 等）
     - **如果只能获得摘要**，按以下优先顺序尝试：
       - **优先级1：从 Zotero 获取全文**
         - 使用 Zotero 语义搜索或基于 DOI/标题搜索文献
         - 如果找到匹配文献，使用 `mcp__zotero__zotero_get_item_fulltext` 获取全文内容
         - 调用 parse_paper_fulltext.py 生成 txt 格式全文
         - 使用 sed 命令分段读取
         - 进入步骤3进行解读
       - **优先级2：询问用户**
         - 如果只能获得摘要，执行以下询问流程：
           - 向用户说明：目前只能获取到文章摘要，无法获得全文
           - 提示用户：检查 Zotero 中是否有该文献的 PDF 附件
           - 询问用户：是否只基于摘要进行解读？
           - 提供以下选项供用户选择：
             - **选项1**：仅基于摘要进行解读（可能内容不够详细）
             - **选项2**：提供全文URL链接，由系统尝试获取全文后解读
             - **选项3**：用户自行下载PDF后，使用 `--file` 或 `--pdf` 参数重新提供本地文件
             - **选项4**：将PDF添加到 Zotero 后，系统重新从 Zotero 获取
           - **等待用户确认后再继续**

3. **全文处理（仅当通过 Zotero 获取到全文时）**
   - **Step 3.1：自动调用 parse_paper_fulltext.py**
     - 从 Zotero 获取的 JSON 格式中提取全文内容
     - 生成结构化的 txt 格式全文文件
     - 自动生成章节摘要文件（_summary.txt）

   - **Step 3.2：使用 sed 命令分段读取**
     - 根据章节边界分段处理
     - 示例 sed 命令：
       ```bash
       # 按章节分段（如 1. Introduction, 2. Methods 等）
       sed -n '/1\. Introduction/,/2\. Methods/p' fulltext_extracted.txt

       # 按段落分段
       sed -n '1,10p'    # 读取前10行
       sed -n '11,20p'   # 读取11-20行
       sed -n '21,30p'   # 读取21-30行
       ...

       # 按字符数分段（每10000字符一段）
       split -l 100 fulltext_extracted.txt section_

       # 使用 sed 按段落号提取
       sed -n '段落号,$p'  # 从指定段落开始到文件末尾
       ```
     - 确保章节结构的完整性
     - 避免段落被截断

4. **文章解读**
   - 用严谨、科学的语言解读文章所有要点
   - 包含以下结构：
     - 文献基本信息（标题、期刊、DOI、PMID等）
     - 研究背景与科学问题
     - 研究方法
     - 研究发现
     - 科学意义与临床价值
     - 展望与未来研究方向
     - 结论
     - MeSH主题词（如有）
     - 关键信息总结
   - 如果只基于摘要解读，在文末明确标注：**"注意：本文解读仅基于文章摘要，内容可能不够全面详细。建议查阅原文全文以获取完整信息。"**

5. **文件输出**
   - 将解读内容保存为markdown文件
   - 文件命名格式：`{关键词}_article_interpretation.md` 或 `{PMID}_article_interpretation.md`
   - 同时生成 txt 格式的全文文件（用于后续处理）
   - 生成章节摘要文件（_summary.txt）

当用户通过 `--file` 或 `--pdf` 参数提供本地 PDF 文件时：

1. **PDF内容提取**
   - 使用 `pdftotext` 命令行工具将 PDF 转换为纯文本
   - 命令示例：`pdftotext "path/to/article.pdf" -`
   - 或者先将 PDF 转换为临时文本文件：`pdftotext "path/to/article.pdf" "temp_article.txt"`
   - 读取转换后的文本内容

2. **文章信息识别**
   - 从 PDF 文本中提取文章基本信息
   - 包含：标题、作者、期刊、发表日期、DOI（如有）、PMID（如有）
   - 识别文章类型（原创研究、综述、meta分析等）

3. **文章解读**
   - 用严谨、科学的语言解读文章所有要点
   - 包含以下结构：
     - 文献基本信息（从PDF中提取）
     - 研究背景与科学问题
     - 研究方法
     - 研究发现
     - 科学意义与临床价值
     - 展望与未来研究方向
     - 结论
     - 关键信息总结
   - 如果 PDF 中包含 MeSH 主题词或关键词，也一并列出

4. **文件输出**
   - 将解读内容保存为markdown文件
   - 文件命名格式：`{文件名}_article_interpretation.md` 或基于标题关键词命名

## 使用的 MCP 工具

### PubMed MCP Server
| 工具名称 | 功能描述 |
|----------|----------|
| `mcp__pubmed-mcp-server__search_articles` | 在 PubMed 上搜索文章，支持通过 DOI、标题、PMID 等方式查询 |
| `mcp__pubmed-mcp-server__get_article_details` | 获取文章的详细元数据和摘要 |
| `mcp__pubmed-mcp-server__get_full_text` | 从 PubMed Central (PMC) 获取全文（需要PMCID） |
| `mcp__pubmed-mcp-server__get_abstract` | 根据 PMID 获取文章摘要 |
| `mcp__pubmed-mcp-server__convert_identifiers` | 在 PMID、DOI 和 PMC ID 之间转换 |

### Zotero MCP Server
| 工具名称 | 功能描述 |
|----------|----------|
| `mcp__zotero__zotero_search` | 在 Zotero 中进行语义搜索 |
| `mcp__zotero__zotero_search_items` | 在 Zotero 中搜索文献 |
| `mcp__zotero__zotero_get_item_fulltext` | 获取 Zotero 中文献的全文内容 |

## 输出格式要求

- 使用中文进行解读
- 采用markdown格式
- 结构清晰，层次分明
- 语言严谨科学
- 包含完整的文献引用信息

## 注意事项

### 使用PubMed在线检索时：
- **全文获取优先原则（按顺序）**：
  1. **优先使用 get_article_details 获取摘要和元数据**，然后使用 get_full_text 获取全文（如果有PMCID）
  2. **其次从 Zotero 获取全文**：使用 Zotero 语义搜索或基于 DOI/标题搜索，获取本地 Zotero 库中的 PDF 附件
  3. **最后询问用户**：如果只能获取到摘要，必须先询问用户选择
- **重要：一旦获取到全文后，不再尝试其他 MCP**
  - 如果通过 PubMed 成功获取到全文，直接进行解读，**不再尝试任何其他 MCP 工具**（包括 web reader、web search 等）
  - 如果通过 Zotero 成功获取到全文，直接进行解读，**不再尝试任何其他 MCP 工具**（包括 web reader、web search 等）
  - 如全文内容过长，采用**分段读取**的方式处理，确保完整解读所有内容
- **全文格式说明**：
  - 通过 `mcp__pubmed-mcp-server__get_full_text` 获取的全文一般为 **JSON 格式**，可直接解析提取文本内容
  - 通过 `mcp__zotero__zotero_get_item_fulltext` 获取的全文一般为 **JSON 格式**，可直接解析提取文本内容
  - 全文内容编码一般为 **UTF-8**，解析时需注意编码问题，避免中文乱码
  - **分段读取策略**：文献全文一般行数很少但每行内容很多，应优先按照**字符长度**分段读取（如每 5000-10000 字符一段），而非按行分割
  - 直接解析 JSON 中的全文字段进行解读，无需尝试其他格式转换工具
- **仅摘要情况处理**：如果只能获取到摘要，必须先询问用户选择：
  - 仅基于摘要解读（内容可能不够详细）
  - 提供全文URL链接
  - 下载PDF后使用本地文件模式
  - 将PDF添加到 Zotero 后重新获取
- 提供基于摘要的解读时，必须在文末明确标注：**"注意：本文解读仅基于文章摘要，内容可能不够全面详细。建议查阅原文全文以获取完整信息。"**
- 保持客观中立的学术态度
- 如遇到搜索不到文章的情况，请提供更准确的DOI、标题或PMID
- **Zotero 使用说明**：
  - 确保已正确配置 Zotero MCP 服务器
  - 确保 Zotero 中已添加相关文献及其 PDF 附件
  - 文献的 DOI 或标题信息应准确，以便搜索匹配

### 使用本地PDF文件时：
- 确保已安装 `pdftotext` 工具（来自 Poppler 或 Xpdf 套件）
  - Windows: 可通过 Chocolatey 安装 `choco install poppler`
  - macOS: `brew install poppler`
  - Linux: `sudo apt-get install poppler-utils`
- 提供的PDF文件路径必须是有效的绝对路径或相对路径
- PDF文件应包含完整的文章内容（标题、作者、正文、参考文献等）
- 对于扫描版PDF，文字识别效果可能不佳，建议使用可复制的PDF
- 如PDF转换失败，请检查：
  1. pdftotext 是否正确安装
  2. PDF文件是否损坏
  3. PDF文件是否有密码保护

## 高级功能：全文提取脚本（parse_paper_fulltext.py）

本技能集成了一个专门的解析脚本，用于处理从 Zotero 获取的 JSON 格式全文：

### 功能特点：
1. **自动识别章节结构**：提取文章标题和各主要章节
2. **生成txt全文文件**：保存为结构化的txt格式
3. **生成章节摘要**：自动创建章节结构摘要
4. **编码处理**：正确处理中文和特殊字符

### 使用方法：

#### 方法一：作为独立脚本运行
```bash
# 基本用法
python parse_paper_fulltext.py zotero_fulltext.json

# 指定输出文件
python parse_paper_fulltext.py zotero_fulltext.json my_article_fulltext.txt
```

#### 方法二：集成到论文解读流程
当系统从 Zotero 获取到全文后，将自动：
1. 提取JSON格式内容
2. 调用 parse_paper_fulltext.py 生成txt格式全文
3. 保存章节摘要文件（_summary.txt）
4. 使用全文内容进行解读

### 输出文件：
- `{title}_fulltext.txt` - 结构化的全文内容
- `{title}_summary.txt` - 章节结构摘要（包含字数统计和内容预览）

### 章节提取范围：
- 文章标题
- 摘要（Abstract）
- 数字编号章节（1. Introduction, 2. Methods 等）
- Markdown章节（### Introduction, ## Methods 等）

## 技能优化说明

本技能已进行以下优化：

1. **全文提取优先级**：
   - 首先尝试从 PubMed 获取全文
   - 其次从 Zotero 获取全文
   - 获取成功后自动调用脚本进行格式化处理

2. **智能分段处理**：
   - 当全文过长时（超过 100,000 字符）
   - 自动分段读取内容
   - 保持章节结构的完整性

3. **输出格式优化**：
   - 生成 markdown 格式的解读文件
   - 同时生成 txt 格式的全文文件（可选）
   - 提供章节摘要便于快速浏览

4. **智能分段处理**：
   - 当从 Zotero 获取全文后，自动调用 parse_paper_fulltext.py 生成 txt 格式全文
   - 使用 sed 命令分段读取生成的 txt 文件，便于处理长篇文献
   - 保持章节结构的完整性，支持按章节分段处理
