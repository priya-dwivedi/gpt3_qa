
import csv
import pandas as pd
import nltk
from nltk import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
import numpy as np

import os
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity
from pathlib import Path

import configparser
config = configparser.ConfigParser()
config.read('config.ini')

from rich.console import Console
console = Console()

detokenizer = TreebankWordDetokenizer()

class Embedding:
    def __init__(self):
        self.config=config


    def reading_text(self,file_):
        with open(f"{self.config['FOLDER']['DATA']}{file_}/{file_}.txt") as f:
            contents = f.read()
            content=contents.strip()
        return content
    
    def split_to_csv(self,text, split_threshold=300):
        ## Tokenize into words
        words = word_tokenize(text)
        df = pd.DataFrame()
        split_sentences = []
        ## Make chunks of split threshold
        for i in range(0, len(words), split_threshold):
            word_chunk = words[i:i+split_threshold]
            ## Convert words to sentences
            sentence_chunk = detokenizer.detokenize(word_chunk)
            split_sentences.append(sentence_chunk)
        ## Write to data frame
        df['text'] = split_sentences
        return df

    def get_embedding(self,text, model="text-embedding-ada-002"):
        text = text.replace("\n", " ")
        return openai.Embedding.create(input = [text], engine=model)['data'][0]['embedding']

    def Embedding(self,file_):
        openai.api_key = self.config['KEYS']['OPENAI_API_KEY']
        with console.status("[bold green] Doing Embedding.....") as status:
            #openai.api_key =  self.config['KEYS']['OPENAI_API_KEY']
            content=self.reading_text(Path(file_).stem)
            df = self.split_to_csv(content)

            df['ada_embedding'] = df.text.apply(lambda x: self.get_embedding(x, model='text-embedding-ada-002'))
            df.to_csv(f"{self.config['FOLDER']['DATA']}{file_}/embedded_data.csv", index=False)
        console.log(f"Embedding completed")
