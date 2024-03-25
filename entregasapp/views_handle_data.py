import pandas as pd
from .models import cpPais
import numpy as np

def importar_excel_tms(folder_path) -> pd.DataFrame:

    df = pd.read_excel(folder_path)
    df = df[[
    'pedido',
    'flujo',
    'seller',
    'sucCodigo',
    'estadoPedido',
    'fechaCreacion',
    'fechaRecepcion',
    'fechaDespacho',
    'fechaEntrega',
    'lpn',
    'estadoLpn',
    'trackingDistribucion',
    'trackingTransporte',
    'tipo',
    'codigoPostal',
    'tte',
    'tteSucursalDistribucion',
    'tiendaEntrega',
    'zona'
    ]]

    date_columns = ['fechaCreacion', 'fechaRecepcion', 'fechaDespacho', 'fechaEntrega']

    for column in date_columns:
        df[column] = pd.to_datetime(df[column])

    df['codigoPostal'] = df['codigoPostal'].astype(object)

    for index, row in df.iterrows():
        cp_value = row['codigoPostal']  # Assuming this is the CP value as a string
        cp_instance = cpPais.objects.get(CP=cp_value)
        df.at[index, 'codigoPostal'] = cp_instance

    bdfin = df

    for column in date_columns:
        print(column)
        bdfin[column] = pd.to_datetime(bdfin[column])

    bdfin.replace({pd.NaT: None, np.nan: None}, inplace=True)
    bdfin.replace('nan', None)

    # bdfin = bdfin.rename(columns=lambda x: x.replace('.', 'x'))
    # print(type(bdfin))

    return bdfin