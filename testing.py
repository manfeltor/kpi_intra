from entregasapp.views import importar_excel_tms
import pandas as pd

dtp = importar_excel_tms(r'C:\Users\ftorres\OneDrive - INTRALOG ARGENTINA S.A\kpi\dash_pr\TMS_por_meses\*.xlsx').dtypes

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(dtp)

    