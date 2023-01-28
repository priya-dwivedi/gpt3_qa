import os
import numpy as np
import pandas as pd
import json
import configparser
import argparse
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity
from pathlib import Path

import csv
from rich.console import Console
console=Console()
config = configparser.ConfigParser()
config.read("config.ini")

class Searcher():
    def __init__(self) -> None:
        ## config parsers
        self.config=config
        self.df = pd.DataFrame()

    def load_file(self,input_data):
        ## loading files accenture embbedding
        pdf_file, ext = os.path.splitext(input_data)
        accenture_embedding = f"{self.config['FOLDER']['DATA']}{pdf_file}/embedded_data.csv"
        self.df = pd.read_csv(os.path.join(os.getcwd(), accenture_embedding))
        self.df["ada_embedding"] = self.df['ada_embedding'].apply(eval).apply(np.array)
        print((self.df.head(4)))

    
    def get_embedding(self,text, model="text-embedding-ada-002"):
        """
        Functionality-given the text do text embedding

        INPUT: text -> string text you wnat to give
        RETURN: list
        """
        text = text.replace("\n", " ")
        return openai.Embedding.create(input = [text], engine=model)['data'][0]['embedding']
    
    ## search question in dataframe
    def search_data(self, query, n=3):
        embedding_query = self.get_embedding(query)
        self.df["similarities"] = self.df['ada_embedding'].apply(lambda x: cosine_similarity(x, embedding_query))
        res = self.df.sort_values("similarities", ascending=False).head(n)
        return res['text'].tolist(),res['similarities'].to_list()[0]
        
    
    ## Question Answering using GPT3
    def gpt_completion(self,text, query):
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"{text} \n Q: Based on the above text, explain in detail: {query} \n A:",
                temperature=0.7,
                max_tokens=3000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            response_texts = [f'{item["text"].strip()}' for item in response["choices"]]
            return response_texts
        except:
            return False
    
    def search_df_add_memory(self, query):
        console.print(f"[bold green] ** Query-> {query}[/bold green]")
        ## Load data
        # self.load_file(filename)
        res,sim = self.search_data(query, n=2)
        #webpages,res=self.WebPageFinder(res)
        gpt_answer = self.gpt_completion((res[0]+res[1]), query)[0]
        output={}
        output['status'] = "Success"
        output['query'] = query
        output['answer'] = gpt_answer.replace("\n","")
        disclaimer=""
        if sim<=0.85:
            disclaimer="Disclaimer - I could not find information directly related to your question in the Manual, but i did search online and learned this."
        output['disclaimer'] = disclaimer
        #output['webpage'] = webpages

        #if sim>0.85:
            #self.refesh_memory()
            #self.memory("add",'accenture',output)
        return output


    def Searcher(self,query):
        try:
            openai.api_key = self.config['KEYS']['OPENAI_API_KEY']
            return self.search_df_add_memory(query)
        except Exception as e:
           print(e)
           output={}
           output['status'] = "Failed"
           output['query'] = query
           output['answer'] = ""
           output['disclaimer'] = ""
           #output['webpage'] = ""
           return output

        
    
if __name__=="__main__":
    query="How to create an agile finance function?"
    SearcherObj=Searcher()
    output=SearcherObj.Searcher('ar_2022_e.pdf', query)
    print(output)