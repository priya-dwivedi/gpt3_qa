from pathlib import Path
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

from rich.console import Console
console=Console()

import os

class Utils():
    def __init__(self):
        self.config=config
    
    def create_folder(self,pdf_name:str)->bool:
        try:
            if not os.path.isdir(f"{self.config['FOLDER']['DATA']}{pdf_name.replace('.pdf','')}"):
                os.mkdir(f"{self.config['FOLDER']['DATA']}{pdf_name.replace('.pdf','')}")
                console.print("[bold green] FOLDER CREATED FOR PDF FILE !! [/bold green]")
                return True
            else:
                console.print('[bold yellow] ** WARNING! PDF NAMED FOLDER IS ALREADY THERE OVERWRITING THE PREVIOUS OUTPUT ** [/bold yellow]')
                return True
        except Exception as e:
            console.print(f'[bold red] **ALERT! {e} ** [/bold red]')
            return False
    
    def uploaded_file(self,uploaded_file_):
        save_folder = self.config['FOLDER']['PDF']
        save_path = Path(save_folder, uploaded_file_.name)
        with open(save_path, mode='wb') as w:
            w.write(uploaded_file_.getvalue())