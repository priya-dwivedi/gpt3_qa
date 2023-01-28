from pdfminer.high_level import extract_text
from pathlib import Path
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

from rich.console import Console
console = Console()

class Parser:
    def __init__(self):
        self.config=config

    def parser(self,pdf_name):
        with console.status("[bold green] Parsing PDF.....") as status:
            text = extract_text(pdf_name)
            pdf_=Path(pdf_name).stem
            with open(f"{self.config['FOLDER']['DATA']}{pdf_}/{pdf_}.txt", "a") as myfile:
                myfile.write(text)
        console.log(f"Parsing completed")
