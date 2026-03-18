#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动执行全文提取脚本
功能：
当从 Zotero 获取到 JSON 格式的全文后，自动调用 parse_paper_fulltext.py
进行处理并生成 txt 格式的全文文件
"""

import os
import sys
import subprocess
import re
import json

def find_latest_zotero_file():
    """查找最新的 Zotero 全文文件"""

    # 常见的工作区目录路径
    worktree_dirs = [
        "C:/Users/liush/.claude/projects/D--Data-CIMR-Grants-20260112------2026-claude-output",
        "C:/Users/liush/.claude/projects/C--Users-liush",
        "C:/Users/liush/.claude/projects"
    ]

    latest_file = None
    latest_time = 0

    for worktree_dir in worktree_dirs:
        if os.path.exists(worktree_dir):
            # 搜索包含 "mcp-zotero-zotero_get_item_fulltext" 的文件
            for root, dirs, files in os.walk(worktree_dir):
                for file in files:
                    if "mcp-zotero-zotero_get_item_fulltext" in file and file.endswith(".txt"):
                        file_path = os.path.join(root, file)
                        # 检查文件修改时间
                        mod_time = os.path.getmtime(file_path)
                        if mod_time > latest_time:
                            latest_time = mod_time
                            latest_file = file_path

    return latest_file

def auto_extract_fulltext():
    """自动执行全文提取"""

    print("=" * 60)
    print("开始自动提取全文...")

    # 1. 查找最新的 Zotero 全文文件
    zotero_file = find_latest_zotero_file()

    if not zotero_file:
        print("错误：未找到 Zotero 全文文件")
        return False

    print(f"找到 Zotero 全文文件：{zotero_file}")

    # 2. 确定输出文件路径
    output_dir = os.path.dirname(os.path.abspath(__file__))  # 技能目录
    output_file = os.path.join(output_dir, "fulltext_extracted.txt")

    # 3. 调用 parse_paper_fulltext.py
    try:
        # 构建命令
        cmd = [
            sys.executable,
            "parse_paper_fulltext.py",
            zotero_file,
            output_file
        ]

        # 执行命令
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

        if result.returncode == 0:
            print("\n" + "=" * 60)
            print(result.stdout)

            # 4. 检查生成的文件
            if os.path.exists(output_file):
                print(f"\n全文文件已生成：{output_file}")

                # 读取文件前几行作为预览
                with open(output_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()[:5]
                    print("\n文件预览：")
                    for line in lines:
                        print(line.rstrip())

                return True
            else:
                print("错误：未生成输出文件")
                return False
        else:
            print(f"错误：执行失败，返回码：{result.returncode}")
            print("错误信息：")
            print(result.stderr)
            return False

    except Exception as e:
        print(f"执行过程中发生错误：{e}")
        return False

def generate_fulltext_summary(fulltext_file):
    """生成全文摘要"""

    if not os.path.exists(fulltext_file):
        return

    summary_file = fulltext_file.replace('.txt', '_summary.txt')

    try:
        with open(fulltext_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 统计基本信息
        lines = content.split('\n')
        total_lines = len(lines)
        total_chars = len(content)

        # 提取标题
        title = "未知"
        for line in lines[:20]:
            if line.startswith('文章标题:'):
                title = line.split(':', 1)[1].strip()
                break

        # 生成摘要
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"全文摘要\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"文章标题: {title}\n")
            f.write(f"总行数: {total_lines}\n")
            f.write(f"总字符数: {total_chars}\n")
            f.write("\n章节结构:\n")
            f.write("-" * 20 + "\n")

            # 提取章节
            chapter_pattern = r'^([^-]+)\n-+$'
            for i, line in enumerate(lines):
                if re.match(chapter_pattern, line):
                    chapter_title = re.match(r'^([^-]+)', line).group(1)
                    # 查找下一章节或文件结束
                    next_chapter = None
                    for j in range(i+1, min(i+20, len(lines))):
                        if re.match(chapter_pattern, lines[j]):
                            next_chapter = j
                            break

                    if next_chapter:
                        chapter_content = ''.join(lines[i+1:next_chapter])
                        word_count = len(chapter_content.split())
                    else:
                        chapter_content = ''.join(lines[i+1:])
                        word_count = len(chapter_content.split())

                    f.write(f"{chapter_title}: 约 {word_count} 字\n")

        print(f"摘要文件已生成：{summary_file}")

    except Exception as e:
        print(f"生成摘要时发生错误：{e}")

def main():
    """主函数"""

    # 检查是否在技能目录中
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    parse_script = os.path.join(skill_dir, "parse_paper_fulltext.py")

    if not os.path.exists(parse_script):
        print(f"错误：找不到 parse_paper_fulltext.py 脚本")
        print(f"期望路径：{parse_script}")
        return

    # 自动执行全文提取
    success = auto_extract_fulltext()

    if success:
        print("\n" + "=" * 60)
        print("全文提取完成！")
        print("现在可以使用提取的全文进行论文解读...")
    else:
        print("\n" + "=" * 60)
        print("全文提取失败！")

if __name__ == "__main__":
    main()
