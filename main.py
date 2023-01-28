##### config and argparse
import argparse
import configparser
from parse_data import Parser
from rich.console import Console
from utils import Utils
from embedding import Embedding
from searcher import Searcher

#### streamlit
import streamlit as st

#### 
from pathlib import Path
#### rich console
console=Console()

##### loading config
config = configparser.ConfigParser()
config.read("config.ini")


##### class Object
ParserObj=Parser()
UtilsObj=Utils()
EmbeddingObj=Embedding()
SearcherObj=Searcher()



def main(input:dict)->bool:
    if input["type"]=="add":
        ############# UPLOADING FILE #############
        UtilsObj.uploaded_file(input["upload"])
        st.sidebar.success("File upload successfully")

        ############# CREATING FOLDER #############
        UtilsObj.create_folder(Path(input["pdf_file"]).stem)
        
        ############# PARSING #############
        st.sidebar.info("parsing pdf")
        ParserObj.parser(input["pdf_file"])
        st.sidebar.success("sucessfully parse")
        
        ############# EMBEDDING #############
        st.sidebar.info("Doing Embedding")
        EmbeddingObj.Embedding(Path(input["pdf_file"]).stem)
        st.sidebar.success("sucessfully Embedded")

    if input["type"]=="searcher":
        SearcherObj.load_file(input["pdf_file"])
        output=SearcherObj.Searcher(input["query"])
        return output
    





if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-type", "--type", type=str, help="type add or searcher")
    parser.add_argument("-pdf_name", "--pdf_name", type=str, help="path+pdf file")
    parser.add_argument("-question", "--question", type=str, help="if searcher than ask a question")
    args = parser.parse_args()
    
    if args.pdf_name==None:
        console.print(f"[bold red] ** Please Provide PDF name ** [/bold red]")
        exit()    
    
    if args.type==None:
        console.print(f"[bold red] ** Please Provide type add or searcher ** [/bold red]")
        exit()   

    if args.type=="searcher" and args.question==None:
        console.print(f"[bold red] ** Please ask a question ** [/bold red]")
        exit() 

    console.print(f"[bold green] -- PDF NAME--: {args.pdf_name} [/bold green]")
    
    output=main({"type":args.type,"pdf_file": args.pdf_name,"question": args.question})
    console.print(f"[bold green] {output} [/bold green]")
    
        