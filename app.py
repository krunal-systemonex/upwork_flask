import os

from flask import Flask, render_template
from constants import *

import pandas

app = Flask(__name__)

def get_excel_files(excel_file_path=EXCEL_FILE_PATH):
    excel_file_list = []
    for folder, sub, filespath in os.walk(excel_file_path):
        for file in filespath:
            if file.endswith(".xls") or file.endswith(".xlsx"):
                excel_file_list.append(os.path.join(folder,file))
    return excel_file_list


def read_excel():
    excel_files_list = get_excel_files()
    df_lst = []
    for filepath in excel_files_list:
        excel_data_df = pandas.read_excel(filepath) #, sheet_name='sheet1'
        df_lst.append(excel_data_df)
    # print whole sheet data
    print(df_lst)

@app.route('/')
def demo():
    read_excel()
    return render_template("leibanize.html")


if __name__ == "__main__":
    app.run(debug=True)
