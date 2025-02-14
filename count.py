import os
import re


def count_words_in_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        # 匹配中文字符、ASCII字母数字字符以及空格分隔的单词
        words = re.findall(r"[\u4e00-\u9fff]|[a-zA-Z0-9]+", content)
        return len(words)


def count_words_in_directory(directory_path):
    total_word_count = 0
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file == "book.md":
                file_path = os.path.join(root, file)
                total_word_count += count_words_in_file(file_path)
    return total_word_count


folder_path = "/home/abc/Nutstore Files/Kapital/"
total_words = count_words_in_directory(folder_path)
print(f"Total word count in all 'book.md' files: {total_words}")
