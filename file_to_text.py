from docx import Document
import os

def docx_to_text(docx_paths):
    full_texts = []  # 用于存储所有文档内容的列表

    for docx_path in docx_paths:
        # 确保路径是绝对路径
        docx_filename = os.path.abspath(docx_path)
        # 打开并读取文档
        doc = Document(docx_filename)
        text_list = []  # 用于存储单个文档中所有段落的文本

        # 遍历文档中的段落和运行（run），将它们合并成文本
        for para in doc.paragraphs:
            text_list.append(para.text)

        # 将单个文档的所有段落文本合并为一个字符串，并添加到full_texts列表中
        full_texts.append('\n'.join(text_list))

    # 返回包含所有文档内容的列表
    return full_texts


