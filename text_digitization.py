
import pandas as pd
import os
from tika import parser
import re
import sys
import traceback as tr
def pdf_converter(directory_path, min_length=200, include_line_breaks=False):
    file_path = 'file not created'
    list_pdf = []
    if directory_path.endswith("pdf"):
            list_pdf.append(directory_path)
    #i=0
    pdf=list_pdf[0]
    try:
        #df.loc[i] = [pdf.replace(".pdf",''), None]
        raw = parser.from_file(pdf)
        s = raw["content"].strip()
        paragraphs = re.split("\n\n\n+(?=\u2028|[A-Z-0-9])", s)  # Split by empty lines greater than 2
        list_par = []
        temp_para = ""  # variable that stores paragraphs with length<min_length
        # (considered as a line)
        for p in paragraphs:
            if not p.isspace():  # checking if paragraph is not only spaces
                if include_line_breaks:  # if True, check length of paragraph
                    if len(p) >= min_length:
                        if temp_para:
                            # if True, append temp_para which holds concatenated
                            # lines to form a paragraph before current paragraph p
                            list_par.append(temp_para.strip())
                            temp_para = (
                                ""
                            )  # reset temp_para for new lines to be concatenated
                            list_par.append(
                                p.replace("\n", "")
                            )  # append current paragraph with length>min_length
                        else:
                            list_par.append(p.replace("\n", ""))
                    else:
                        # paragraph p (line) is concatenated to temp_para
                        line = p.replace("\n", " ").strip()
                        temp_para = temp_para + f" {line}"
                else:
                    # appending paragraph p as is to list_par
                    list_par.append(p.replace("\n", ""))
            else:
                if temp_para:
                    list_par.append(temp_para.strip())

        #print(df.loc[0,"paragraphs"])
        #df["paragraphs"][0] = list_par
        #print()
        #txt_path = os.path.join(os.getcwd(), 'infer_files')
        file_path = pdf.replace('.pdf','.txt')
        #file_path = os.path.join(directory_path,pdf.replace('.pdf','.txt'))
        with open(file_path,'w',encoding='utf-8') as f:
            for para in list_par:
                f.write('%s\n' % para)
        #df["paragraphs"][0] = "_!".join(map(str,list_par))
    except:
        print(tr.format_exc())
        print("Unexpected error:", sys.exc_info()[0])
        print("Unable to process file {}".format(pdf))
    return file_path
