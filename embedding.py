
import openai



from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from typing import List, Optional
from openai import OpenAI

import pandas as pd

import numpy as np

def get_completion(prompt,model='gpt-3.5-turbo'):
  messages=[{'role':'user','content':prompt}]
  response=openai.ChatCompletion.create(
      model=model,
      messages=messages,
      temperature=0,
  )
  return response.choices[0].message["content"]

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def get_embedding(text: str, model="text-embedding-ada-002", **kwargs) -> List[float]:
    client = OpenAI(api_key='YourAPIKey')
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model, **kwargs)
    return response.data[0].embedding



def embeddingFunc(usertext,policyFile):
    # 调用openai 向量化
    embeddings = OpenAIEmbeddings(openai_api_key='yourAPIKey')
    # embedding model parameters
    embedding_model = "text-embedding-ada-002"
    embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
    max_tokens = 8000  # the maximum for text-embedding-ada-002 is 8191
    df_policy=pd.read_csv(policyFile)
    #df_user=pd.read_csv(userFile)

    dflist=df_policy.loc[:,['大致内容']]
    user_embedding = get_embedding(usertext, model="text-embedding-ada-002")
    df_policy['embedding'] = df_policy['大致内容'].apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))
    df_policy["similarity"] = df_policy.embedding.apply(lambda x: cosine_similarity(x, user_embedding))
    df_policy.to_csv("./Content/temp/policy_file_with_embedding_and_similarity")

