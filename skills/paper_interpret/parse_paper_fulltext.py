#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
论文全文解析脚本
功能：
1. 从Zotero获取的JSON格式全文中提取文本内容
2. 保存为txt格式的全文文件
3. 支持分段解析和章节提取
"""

import json
import re
import sys
import io

def extract_fulltext(zotero_json_file, output_path):
    """
    从Zotero获取的JSON文件中提取全文内容

    参数:
    zotero_json_file: Zotero返回的JSON文件路径
    output_path: 输出的txt文件路径

    返回:
    bool: 是否成功提取
    """

    # 设置输出编码为UTF-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # 读取Zotero全文文件
    try:
        with open(zotero_json_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"错误：无法读取文件 {zotero_json_file}: {e}")
        return False

    # 提取JSON部分（以{"result": 开头的部分）
    json_match = re.search(r'^\s*({.*?})\s*$', content, re.DOTALL)
    if json_match:
        try:
            json_data = json.loads(json_match.group(1))
            result = json_data.get('result', '')

            # 提取文章标题
            title_match = re.search(r'^# (.+)$', result, re.MULTILINE)
            if title_match:
                title = title_match.group(1)
                # 创建章节结构
                chapters = extract_chapters(result, title)

                # 写入txt文件
                with open(output_path, 'w', encoding='utf-8') as f:
                    # 写入基本信息
                    f.write(f"文章标题: {title}\n")
                    f.write("=" * 80 + "\n\n")

                    # 写入章节内容
                    for chapter_title, chapter_content in chapters.items():
                        f.write(f"{chapter_title}\n")
                        f.write("-" * len(chapter_title) + "\n")
                        f.write(chapter_content.strip() + "\n\n")

                print(f"全文已成功提取并保存到: {output_path}")

                # 生成章节摘要
                generate_chapter_summary(chapters, output_path.replace('.txt', '_summary.txt'))

                return True

        except json.JSONDecodeError as e:
            print(f"错误：JSON解析失败: {e}")
            return False
        except Exception as e:
            print(f"错误：处理文件时发生错误: {e}")
            return False
    else:
        print("错误：未找到JSON格式内容")
        return False

def extract_chapters(fulltext, title):
    """提取文章的章节结构"""

    chapters = {}

    # 提取标题
    chapters["文章标题"] = title

    # 提取各主要章节
    # 查找数字编号的标题（如 1 Introduction, 2 Background 等）
    chapter_pattern = r'\n(\d+\.\s+[^\n]+)|\n(#[^#][^\n]+)'
    chapter_matches = re.findall(chapter_pattern, fulltext, re.MULTILINE)

    for match in chapter_matches:
        if match[0]:  # 数字章节（1. 格式）
            chapter_title = match[0].strip()
        else:  # ## 标题格式
            chapter_title = match[1].strip()

        # 获取章节内容（从标题开始到下一个标题之前）
        start_pos = fulltext.find(chapter_title)
        if start_pos != -1:
            # 查找下一个章节标题的位置
            next_match = None
            for other_match in chapter_matches:
                if other_match[0] and other_match[0] != chapter_title:
                    next_pos = fulltext.find(other_match[0])
                    if next_pos > start_pos:
                        next_match = next_pos
                        break
                elif other_match[1] and other_match[1] != chapter_title:
                    next_pos = fulltext.find(other_match[1])
                    if next_pos > start_pos:
                        next_match = next_pos
                        break

            # 提取章节内容
            if next_match:
                chapter_content = fulltext[start_pos + len(chapter_title):next_match].strip()
            else:
                chapter_content = fulltext[start_pos + len(chapter_title):].strip()

            chapters[chapter_title] = chapter_content

    # 查找摘要部分
    abstract_match = re.search(r'^\s*Abstract\s+(Abstract)(.*?)(?=1\s+\w+)', fulltext, re.DOTALL | re.IGNORECASE)
    if abstract_match:
        chapters["摘要"] = abstract_match.group(2).strip()
    else:
        # 备用摘要查找
        abstract_match2 = re.search(r'^\s*Abstract\s+\n+(.*?)(?=\n\n)', fulltext, re.DOTALL | re.IGNORECASE)
        if abstract_match2:
            chapters["摘要"] = abstract_match2.group(1).strip()

    return chapters

def generate_chapter_summary(chapters, summary_path):
    """生成章节摘要"""

    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("文章章节结构摘要\n")
        f.write("=" * 40 + "\n\n")

        for chapter_title, chapter_content in chapters.items():
            if chapter_title != "文章标题":
                # 计算章节字数
                word_count = len(chapter_content)

                # 提取每段第一句话作为内容预览
                first_paragraph = chapter_content.split('\n')[0] if '\n' in chapter_content else chapter_content[:100]

                f.write(f"{chapter_title}\n")
                f.write(f"字数: {word_count}\n")
                f.write(f"内容预览: {first_paragraph[:100]}...\n\n")

    print(f"章节摘要已保存到: {summary_path}")

def main():
    """主函数，通过命令行参数调用"""

    # 获取命令行参数
    if len(sys.argv) < 2:
        print("用法: python parse_paper_fulltext.py <zotero_json_file> [output_txt_file]")
        return

    zotero_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "fulltext_extracted.txt"

    # 执行提取
    success = extract_fulltext(zotero_file, output_file)

    if success:
        print("\n全文提取完成！")
    else:
        print("\n全文提取失败！")

if __name__ == "__main__":
    main()
