def restructUserInfo(userInfo):
    enterprise_name = userInfo.loc[0,['企业名称']].values[0]
    industry_category = userInfo.loc[0,['行业大类']].values[0]
    usertext = enterprise_name + ' ' + industry_category
    return usertext

