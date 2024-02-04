from django.shortcuts import render
import pandas as pd
import os
import glob
import numpy as np

# Create your views here.

# render

def render_main(req):

    return render(req, "entregasmain.html")

#db

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
    ]]

    date_columns = ['fechaCreacion', 'fechaRecepcion', 'fechaDespacho', 'fechaEntrega']

    for column in date_columns:
        df[column] = pd.to_datetime(df[column])

    bdfin = df

    # excel_files = glob.glob(folder_path)
    # df_inc = []
    # for file in excel_files:
    #     df = pd.read_excel(file)
    #     df_inc.append(df)

    # bdfin = pd.concat(df_inc, ignore_index=True)
    # bdfin = bdfin.astype(str)
    # bdfin = bdfin.drop_duplicates(subset=['lpn'])
    # bdfin = bdfin.drop('fechaRecepcion.1', axis=1)

    # date_columns = ['fechaCreacion', 'fechaPactada', 'fechaConfirmacion', 'fechaColecta', 'fechaRecepcion', 'fechaDespacho', 'fechaEntrega', 'fechaGuardado']
    
    # conversion to time format

    # for column in date_columns:
    #     bdfin[column] = bdfin[column].str[:10]
        # print(bdfin[column])

    
    # bdfin[date_columns] = pd.to_datetime(bdfin[date_columns])


    # date_formats = ['%d/%m/%Y %H:%M:%S', '%d/%m/%YT %H:%M:%S']
    # bdfin[date_columns] = bdfin[date_columns].apply(pd.to_datetime, errors='coerce', utc=True, format=date_formats)
    # bdfin[date_columns] = pd.to_datetime(bdfin[date_columns], utc=True)

    # numeric_columns = ['diffMmConfirmacionCreacion', 'diffMmConfirmacionColecta', 'diffMmColectaEntrega', 'diffMmCreacionEntrega',
    #                 'unidades', 'bulto', 'bultosPedido', 'alto', 'ancho', 'largo', 'peso', 'valorDeclarado', 'ubicacion',
    #                 'ordenAnterior', 'distancia', 'excedente', 'pesoAforado', 'express', 'repartidor', 'costo', 'precioVenta', 'tiendaEntrega']
    # bdfin[numeric_columns] = bdfin[numeric_columns].apply(pd.to_numeric, errors='coerce')

    # integer_columns = ['unidades', 'bulto', 'bultosPedido']
    # bdfin[integer_columns] = bdfin[integer_columns].apply(pd.to_numeric, downcast='integer', errors='coerce')

    # bdfin.replace({pd.NaT: None, np.nan: None}, inplace=True)
    # bdfin.replace('nan', None)

    for column in date_columns:
        print(column)
        bdfin[column] = pd.to_datetime(bdfin[column])


    bdfin.replace({pd.NaT: None, np.nan: None}, inplace=True)
    bdfin.replace('nan', None)

    # bdfin = bdfin.rename(columns=lambda x: x.replace('.', 'x'))
    # print(type(bdfin))

    return bdfin