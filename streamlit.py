import os
import pandas as pd
import streamlit as st
from PIL import Image
import glob
from main import main
import configparser
config = configparser.ConfigParser()
config.read("config.ini")

from searcher import Searcher
SearcherObj=Searcher()

@st.cache
def finding_answer(input):
    #st.session_state["a"]=st.session_state["a"]+1
    output=main(input)
    return output

def init_file(option):
    load=False
    if 'old_option' not in st.session_state:
        st.session_state["old_option"]=option
        load=True
    else:
        if not st.session_state["old_option"]==option:
            load=True
    if load==True:
        print(">>>>>>>>>>>>>>>>>")
        input={}
        input["pdf_file"]=option+".pdf"

# if 'Gpt3QueryObj' not in st.session_state:
#     with st.spinner('Please Wait loading Models'):
#         print("<><<<<<<<<<<<<<<<<<<<")
#         Gpt3QueryObj=Gpt3Query()
#         st.session_state["Gpt3QueryObj"]=Gpt3QueryObj
#         print(">>>>>>>>>>>>>")

def get_file():
    path = "data/"
    files=[files.replace(path,"") for files in glob.glob(path + '*')]
    return files


def UI():
    st.set_page_config(
        page_title="PDF Q&A",
        page_icon="🤖",
    )
    #################################################################
    ######################### SIDEBAR-PAGE ##########################
    #################################################################
    st.sidebar.header('UPLOAD FILES')

    st.sidebar.subheader('Upload a file')
    uploaded_file = st.sidebar.file_uploader("Choose a file",type=["pdf"])

    if st.sidebar.button('upload files'):
        input={}
        input["type"]="add"
        input["pdf_file"]=f"{config['FOLDER']['PDF']}/{uploaded_file.name}"
        input["upload"]=uploaded_file
        main(input)



    ##################################################################
    ######################### MAIN-PAGE ##########################
    #################################################################
    st.subheader('choose a file')
    option = st.selectbox('Please choose a file?',(get_file()))
    

    st.subheader('Q&A')
    query=st.text_input('Please ask a question')
    
    
    

    ############################################################
    ########################## BUTTON ##########################
    ############################################################
    init_file(option)
    if st.button('Find Answer'):
        #with st.spinner('Finding Answer...'):
        if query=="":
            st.error("Please a question.")
            st.stop()
        
        input={}
        input["type"]="searcher"
        input["pdf_file"]=f"{option}"
        input["query"]=query

        output=finding_answer(input)
        if not output["disclaimer"]=="":
            st.warning("⚠️ "+output["disclaimer"])
        st.text_area(label="answer", value=output["answer"], height=400)


    #############################################################
    ######################## FOOTER-PAGE ########################
    #############################################################
    hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)

if __name__=="__main__":
    UI()