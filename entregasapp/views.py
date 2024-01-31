from django.shortcuts import render
import pandas as pd
import os
import glob

# Create your views here.

# render

def render_main(req):

    return render(req, "entregasmain.html")

#db

def importar_excel_tms(folder_path) -> pd.DataFrame:

    excel_files = glob.glob(folder_path)
    df_inc = []
    for file in excel_files:
        df = pd.read_excel(file)
        df_inc.append(df)

    bdfin = pd.concat(df_inc, ignore_index=True)
    bdfin = bdfin.drop_duplicates(subset='lpn')

    return bdfin

