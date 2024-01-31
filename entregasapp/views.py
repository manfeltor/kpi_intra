from django.shortcuts import render
import pandas as pd
import os

# Create your views here.

# render

def render_main(req):

    return render(req, "entregasmain.html")

#db

def importar_excel_tms() -> pd.DataFrame:

    folder_path = ''

    file_names = os.listdir(folder_path)
    
    return baselimpia
