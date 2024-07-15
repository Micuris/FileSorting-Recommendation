
import pandas as pd
def chatglm():
    from Functions.file_to_text import docx_to_text
    from Functions.getFilePath import get_file_path
    file_paths = []
    file_paths = get_file_path(directory='./Content/inputContent')
    texts = docx_to_text(file_paths)
    # texts现在是一个列表，包含了所有文件的内容
    resTexts = [

    ]
    # 初始化结果列表resTexts
    # 列名
    columns = [
        "文件名称", "发文部门", "针对的省市和下属区县", "针对产业", "企业类型",
        "企业规模", "针对的企业建立时长", "政策内容分类", "大致内容"
    ]

    df = pd.DataFrame(columns=columns)
    df_list_row = []
    for i, text in enumerate(texts):
        from zhipuai import ZhipuAI

        client = ZhipuAI(api_key="yourAPIKey")  # 填写您自己的APIKey
        response = client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "user",
                 "content": "请给出这篇文档的文件题目 发文部门 针对的省市和下属区县 针对产业 企业类型 企业规模 针对的企业建立时长政策内容分类,大致内容(100字以内,中间不要有句号),请确保你的回答有且仅有这八项"
                            "其中,发文部门,从下列标签选择:重庆市政府/办公厅政策 重庆市发改委 重庆市数育委员会 重庆市科学技术局 重庆市经济和信息化委员会 重庆市公安局 重庆市民政局 重庆市财政局 重庆市人社局 重庆市规划和自然资源局 重庆市生态环境局 重庆市住房城乡建委 重庆市城市管理局 重庆市交通局 重庆市水利局 高新区管委会 重庆经开区管委会 国庆市农业衣村委员会 重庆市商务委员会 重庆市文旅局 重庆市卫生健康委员会 重庆市退役军人事务局 重庆市应急管理局 重庆市市场监督管理局 重庆市乡村振兴局 重庆市大数据局 重庆市人民政府口岸物流办 重庆市招商投资促进局 重庆市公共资源交易管理局 重庆市林业局 重庆市药品监督管理局 重庆市知识产权局 两江新区管委会;没有符合项则回答其他"
                            "针对产业,从下列标签选择,没有则务必回答无:节能环保、生物医药、大数据、科研单位、集成电路、高端装备、科技中介、医疗器械、农业、云计算、新能源与节能、传统实业、新材料、文化创意设计、电子信息、软件海洋产业、传统服务业、公共服务、生态修复、物联网、生命健康、人工智能、产业园、金融业、新能源汽车、采矿业、区块链、汽车制造业、高技术服务、军工业、电子科技产业、现代服务业、建筑业、化工产业、5G/移动通信、机器人、贸易、电子商务、交通/物流/供应链、互联网、航空航天、其他"
                            "企业类型,从下列标签选择:国有企业、民营企业、外资企业、合资企业、个体工商户、非盈利性组织、独角兽,没有符合项回答未提及"
                            "企业规模,从下列标签选择:小微企业、中小企业、大型企业,没有符合项回答未提及"
                            "针对的企业建立时长,从下列标签选择:1年以下、1-3年，3-5年，5-10年，10年以上,没有符合项回答未提及"
                            "政策内容分类,从下列标签选择:碳达峰、资质认定与奖励、高增长/独角兽、转型转产、贷款贴息贴保、中小微企业、产业联盟、节能减排、企业培训、社会组织、上市/并购、科研立项、商贸物流、房租水电补贴、纳税奖励、中介服务、股权资助、品牌/市场开拓、消费促进、活动策划、信息化/工业互联网、稳企稳岗、传统产业、创新载体、事前资助、新基建、事后咨助、科技成果奖励、专精特新、产业化、标准化、扩产上规模、大型企业、招商引资、重大项目、高新技术企业、应用示范、知识产权、人才认定与资助、新兴产业、配套资助、研发中试、技术改造、总部企业、产业基金、创新创业、研发资助,没有符合项则回答其他"
                            "回答过程中你只需要回答标签内容即可,不需要其他文字叙述以及对问题的重述,请注意每个类型的标签最多选择三个,"
                            "请注意保证你每次回答的格式为 文件名称: 发文部门: 针对的省市和下属区县: 针对产业: 企业类型: 企业规模: 针对的企业建立时长: 政策内容分类: 大致内容:  请严格遵循此格式!!!不要有多余的语言,不需要解释为什么这么选择,不要有任何逗号单引号双引号,不要有任何逗号单引号双引号,不要有任何逗号单引号双引号" + text},

            ],
        )

        content = str(response.choices[0].message).replace('\\n', ';').split(";")
        print(i)
        print(content)

        row_con = []
        for j in range(len(content)):
            if len(content[j].split(':')) > 1:
                value = content[j].split(':')[1].strip()  # 删除冒号前的内容
                row_con.append(value)
            df_list_row.append(row_con)

    # 将df_list_row转换为DataFrame的行
    n=max ([len(item) for item in df_list_row])
    for row_con in df_list_row:
        if len(row_con)==n:
            row_series = pd.Series(row_con, index=columns)
            df = pd.concat([df, row_series.to_frame().T], ignore_index=True)
    df.to_csv('./Content/temp/glmOutput.csv', index=False)

    import csv

    def remove_duplicates(input_file, output_file):
        # 用于存储已经出现过的行
        seen_rows = set()

        with open(input_file, 'r', newline='') as file_in, open(output_file, 'w', newline='') as file_out:
            reader = csv.reader(file_in)
            writer = csv.writer(file_out)

            for row in reader:
                # 将行转换为元组，以便可以将其添加到集合中进行比较
                row_tuple = tuple(row)

                if row_tuple not in seen_rows:
                    # 如果行不在集合中，写入到输出文件中，并将其添加到集合中
                    writer.writerow(row)
                    seen_rows.add(row_tuple)

    # 示例用法

    remove_duplicates('./Content/temp/glmOutput.csv', './Content/temp/embeddingInput.csv')

