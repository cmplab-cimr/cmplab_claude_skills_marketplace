---
description: 在PubMed上搜索指定主题的文献并以中英文双语格式输出
name: pubmed-topic-search
---

# PubMed主题文献搜索技能

## 技能描述

用户指定一个中文主题，自动翻译成英语后，在PubMed上搜索相关文章（优先检索近期文章），并尝试获取全文内容以提供更详细的要点总结，最终以中英文双语格式输出文献信息到markdown文件。

## 使用方法

### 基本用法
```
/pubmed-topic-search [中文主题]
```

### 示例
```
/pubmed-topic-search GIPR在人体不同组织和器官中的表达
/pubmed-topic-search 胰高血糖素受体
/pubmed-topic-search 阿尔茨海默病治疗靶点
```

## 执行流程

1. **主题翻译**
   - 接收用户输入的中文主题
   - 准确翻译成英文搜索词

2. **PubMed文献检索**
   - 使用 `mcp__pubmed-mcp-server__search_articles` API 根据英文主题搜索相关文章
   - 优先检索近期文章（可设置时间过滤）
   - 优先输出权威期刊文章
   - 获取文章的PMID列表

3. **文献信息获取**
   - 使用 `mcp__pubmed-mcp-server__get_article_details` API 获取每篇文章的详细元数据和摘要
   - 包括：标题、期刊、发表日期、PMID、DOI、MeSH主题词、摘要等

4. **全文获取（关键步骤）**
   - 对于每篇文章，按以下优先顺序尝试获取全文：
     - **步骤1**：使用 `mcp__pubmed-mcp-server__convert_identifiers` 将 PMID 转换为 PMCID
     - **步骤2**：如果成功获取 PMCID，使用 `mcp__pubmed-mcp-server__get_full_text` API 获取 PMC 全文
     - **步骤3**：如果 PMC 全文不可用，尝试从 Zotero 获取全文：
       - 使用 `mcp__zotero__zotero_semantic_search` 或 `mcp__zotero__zotero_search_items` 基于 DOI/标题搜索
       - 如果找到匹配文献，使用 `mcp__zotero__zotero_get_item_fulltext` 获取全文内容
     - **步骤4**：如果以上方法都无法获取全文，则仅使用摘要进行总结

5. **中文要点总结**
   - **如果成功获取全文**：基于全文内容进行详细总结，包括研究背景、方法、主要发现、意义和结论
   - **如果仅获取摘要**：基于摘要进行简明总结，并在文末标注"仅基于摘要"
   - 每篇文章总结3-5个关键要点

6. **文件输出**
   - 将所有文章信息整理成markdown格式
   - 按发表日期降序排列（最新的在前）
   - 标注每篇文章是否基于全文总结
   - 保存到当前工作目录

## 使用的 MCP 工具

### PubMed MCP Server
| 工具名称 | 功能描述 |
|----------|----------|
| `mcp__pubmed-mcp-server__search_articles` | 在 PubMed 上搜索文章，支持关键词、时间范围等过滤 |
| `mcp__pubmed-mcp-server__get_article_details` | 获取文章的详细元数据和摘要 |
| `mcp__pubmed-mcp-server__get_full_text` | 从 PubMed Central (PMC) 获取全文（需要PMCID） |
| `mcp__pubmed-mcp-server__convert_identifiers` | 在 PMID、DOI 和 PMC ID 之间转换 |
| `mcp__pubmed-mcp-server__get_abstract` | 根据 PMID 获取文章摘要 |

### Zotero MCP Server
| 工具名称 | 功能描述 |
|----------|----------|
| `mcp__zotero__zotero_semantic_search` | 在 Zotero 中进行语义搜索 |
| `mcp__zotero__zotero_search_items` | 在 Zotero 中搜索文献 |
| `mcp__zotero__zotero_get_item_fulltext` | 获取 Zotero 中文献的全文内容 |

## 输出格式要求

### 单篇文章格式（有全文）

```markdown
### [序号]. [英文标题] *[全文总结]*

**标题**: [中文标题]
**期刊**: [Journal Name]
**发表日期**: [YYYY-MM-DD]
**PMID**: [PMID]
**DOI**: [DOI]
**全文来源**: PMC/Zotero

**关键要点**（中文，基于全文）：
- 要点1
- 要点2
- 要点3
- 要点4
- 要点5
```

### 单篇文章格式（仅摘要）

```markdown
### [序号]. [英文标题] *[仅摘要]*

**标题**: [中文标题]
**期刊**: [Journal Name]
**发表日期**: [YYYY-MM-DD]
**PMID**: [PMID]
**DOI**: [DOI]

**关键要点**（中文，仅基于摘要）：
- 要点1
- 要点2
- 要点3

> 注意：本文总结仅基于摘要，内容可能不够全面。
```

### 总体文件结构

```markdown
# [中文主题] - PubMed文献搜索结果

## 搜索摘要

**搜索主题（中文）**: [主题]
**搜索关键词（英文）**: [English keywords]
**搜索数据库**: PubMed
**检索时间**: [YYYY-MM-DD]
**文章数量**: [N]篇
**全文获取**: [M]篇成功获取全文，[N-M]篇仅基于摘要

---

## 文献列表

[文章1]
[文章2]
...

---

## 参考文献

1. [参考文献1]
2. [参考文献2]
...
```

## 输出要求

| 项目 | 要求 |
|------|------|
| 标题 | 英文 |
| 期刊 | 英文 |
| 发表日期 | YYYY-MM-DD格式 |
| PMID | 完整数字 |
| DOI | 完整格式 |
| 全文来源 | PMC 或 Zotero（如有） |
| 关键要点 | 中文，基于全文时5条，仅摘要时3条 |

## 搜索参数设置

### 默认设置
- 最大文章数: 20-30篇
- 排序方式: 按发表日期降序（最新的在前）
- 时间范围: 无限制（或近5年）

### 可自定义参数
```
/pubmed-topic-search [主题] --max 50        # 最多50篇
/pubmed-topic-search [主题] --recent 3    # 近3年
/pubmed-topic-search [主题] --sort relevance # 按相关性排序
/pubmed-topic-search [主题] --fulltext-only # 仅返回有全文的文章
```

## 注意事项

1. **翻译准确性**: 确保中文主题准确翻译为英文搜索词，必要时提供多个搜索词变体

2. **全文获取优先级**:
   - 优先从 PMC 获取全文（开放获取）
   - 其次从本地 Zotero 库获取
   - 最后仅使用摘要

3. **中文总结质量**:
   - **基于全文**：详细总结研究背景、方法、结果、讨论和结论
   - **仅基于摘要**：简明扼要，突出重点，并明确标注
   - 避免过度解读，忠实于原文内容

4. **信息完整性**:
   - 确保PMID、DOI等标识符准确
   - 期刊名称使用标准缩写或全称
   - 日期格式统一

5. **文件命名**:
   - 格式: `[主题关键词]_literature_search.md`
   - 使用英文关键词作为文件名
   - 避免特殊字符

6. **Zotero 使用说明**:
   - 确保已正确配置 Zotero MCP 服务器
   - 确保 Zotero 中已添加相关文献及其 PDF 附件
   - 文献的 DOI 或标题信息应准确，以便搜索匹配

## 示例输出

```markdown
# GIPR在人体不同组织和器官中的表达 - PubMed文献搜索结果

## 搜索摘要

**搜索主题（中文）**: GIPR在人体不同组织和器官中的表达
**搜索关键词（英文）**: GIPR expression human tissues organs localization
**搜索数据库**: PubMed
**检索时间**: 2026-02-27
**文章数量**: 15篇
**全文获取**: 8篇成功获取全文，7篇仅基于摘要

---

### 1. Human epicardial adipose tissue expresses glucose-dependent insulinotropic polypeptide, glucagon, and glucagon-like peptide-1 receptors as potential targets of pleiotropic therapies *[全文总结]*

**期刊**: European journal of preventive cardiology
**发表日期**: 2023-06-01
**PMID**: 36799940
**DOI**: 10.1093/eurjpc/zwad050
**全文来源**: PMC

**关键要点**（中文，基于全文）：
- **研究背景**：GIPR是肠促胰岛素受体家族成员，在代谢调节中起重要作用，但其在心外膜脂肪组织中的表达和功能尚不明确
- **研究方法**：收集33例接受开胸手术患者的心外膜脂肪组织样本，采用微阵列分析、免疫组化和单细胞RNA测序技术
- **主要发现1**：GIPR和GCGR mRNA在心外膜脂肪组织中均有表达，且表达水平与代谢指标相关
- **主要发现2**：免疫组化分析发现GIPR主要表达于巨噬细胞，部分成熟脂肪细胞、内皮细胞和周细胞也有表达
- **临床意义**：提示GIPR是心血管治疗药物（如GLP-1/GIP双激动剂）的潜在靶点，为心血管代谢疾病的联合治疗提供新思路

---

### 2. Another article title *[仅摘要]*

**期刊**: Some Journal
**发表日期**: 2023-05-15
**PMID**: 12345678
**DOI**: 10.1234/example

**关键要点**（中文，仅基于摘要）：
- 要点1
- 要点2
- 要点3

> 注意：本文总结仅基于摘要，内容可能不够全面。
```
