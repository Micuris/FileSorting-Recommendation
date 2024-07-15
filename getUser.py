import pandas as pd
import csv
from collections import Counter



df = pd.read_csv('./Content/政策推荐企业数据.csv')

def matchUser(userNO):
    global df
    search_usc = userNO
    # 筛选社会信用代码匹配的行
    matching_row = df[df['统一社会信用代码'] == search_usc]
    matching_row.to_csv('./Content/temp/userInfo.csv')



def locMatch(string, csv_file):
        # 提取指定列进行匹配
    column_to_match = "针对的省市和下属区县"

    # 读取CSV文件并提取指定列的数据
    column_data = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            column_data.append(row[column_to_match])

        # 计算字符串和每个表格列的交集和并集比值
    locRatios = []
    for data in column_data:
        intersection = Counter(string) & Counter(data)
        union = Counter(string) | Counter(data)
        ratio = sum(intersection.values()) / sum(union.values())
        locRatios.append(ratio)

    return locRatios

def industryMatch(string, csv_file):
        # 提取指定列进行匹配
    column_to_match = "针对产业"

        # 读取CSV文件并提取指定列的数据
    column_data = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            column_data.append(row[column_to_match])

        # 计算字符串和每个表格列的交集和并集比值
        industryRatios = []
    for data in column_data:
        intersection = Counter(string) & Counter(data)
        union = Counter(string) | Counter(data)
        ratio = sum(intersection.values()) / sum(union.values())
        industryRatios.append(ratio)

    return industryRatios

def recommend(input,csv_file):
    locRatios = locMatch(input, csv_file)
    industryRatios = industryMatch(input, csv_file)

    # 从 DataFrame 中取出 "similarity" 列的数据，并存储到列表 similarity 中
    df_similarity = pd.read_csv('./Content/temp/policy_file_with_embedding_and_similarity')
    similarity = df_similarity['similarity'].tolist()

    avg = []
    for i in range(len(similarity)):
        avg.append(0.2 * locRatios[i] + 0.2 * industryRatios[i] + 0.6 * similarity[i])

        # 读取原始 CSV 文件
    df_output = pd.read_csv(csv_file)

    # 选择文件名称列和大致内容列
    df_new = df_output[['文件名称', '大致内容']]

    # 将选定的列保存为新的 CSV 文件
    df_avg = pd.DataFrame({'avg': avg})

    # 将 df_avg DataFrame 和 df_new DataFrame 进行连接
    df_combined = pd.concat([df_new, df_avg], axis=1)
    # 根据 avg 列的值进行降序排列
    df_combined_sorted = df_combined.sort_values(by='avg', ascending=False)

    # 仅保留前三行
    df_combined_sorted_top3 = df_combined_sorted.head(3)

    # 将排序后的DataFrame保存为新的CSV文件
    df_combined_sorted_top3.to_csv('./Content/outputContent/output.csv', index=False)
