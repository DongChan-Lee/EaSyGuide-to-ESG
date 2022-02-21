from glob import glob
from tqdm import tqdm
import re
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO, open, BytesIO

def read_pdf_file(pdfFile):
    pdfrm = PDFResourceManager()
    strio = StringIO()
    lapa = LAParams()
    device = TextConverter(pdfrm, strio, laparams = lapa)
    
    process_pdf(pdfrm, device, pdfFile)
    device.close()
    
    content = strio.getvalue()
    strio.close()
    
    return content

def texting_folder(year):
    list_year = glob(year + " " + "esg보고서들/*.pdf")
    for file_path in tqdm(list_year):
        try:
            with open(file_path, 'rb') as f:
                firm = read_pdf_file(f)
                firm = re.sub("[A-z\n�\x0c()·・\x00█*●○:©'/~%-,|※▶]", " ", firm)
                firm = re.sub("[0-9]", " ", firm)
                firm = re.sub("\u3000", " ", firm)
                # firm = firm.split(".")
                # firm = '. '.join(firm)
            
            with open(file_path + ".txt", "a", encoding = 'utf-8') as f:
                f.write(firm)
        
        except:
            print(file_path)

year = list(map(str, input().split(' ')))
for year in year:
    texting_folder(year = year)