from django.shortcuts import render
import pandas as pd
import numpy as np
from .models import cpPais, bdoms
from django.db.models import Q
import numpy as np
from .forms import DateRangeForm

# Create your views here.

# render

# def filtered_date_columns(req):

#     columns = 

#     return columns

def render_main(request):
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            # Extract start_date and end_date from the form
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            # Call calculate_date_diff with the date range
            A = calculate_date_diff("fechaDespacho", "fechaEntrega", "CHEEKY", "INTERIOR", "DIST", start_date=start_date, end_date=end_date)
            # Process the data as usual
            B = mode_group_date_diff(A, "codigoPostal__Provincia", "date_difference", "bdDate_difference")
            html_mode_table = B.to_html(index=False)
            C = mean_group_date_diff(A, "codigoPostal__Provincia", "date_difference", "bdDate_difference")
            html_mean_table = C.to_html(index=False)
            context = {'mode_table': html_mode_table, 'mean_table': html_mean_table, 'form': form}

            # calculate_days_between_first_and_last_reception("pedido", "fechaRecepcion")

            return render(request, "entregasmain.html", context)
    else:
        # If it's a GET request or form is invalid, render the form with empty data
        form = DateRangeForm()

    return render(request, "entregasmain.html", {'form': form})
#db

import pandas as pd

def calculate_days_between_first_and_last_reception(pedcol, datecol):

    df = bdoms.objects.filter()
    # Filter purchases with more than one piece
    multi_piece_purchases = df.groupby(pedcol).filter(lambda x: len(x) > 1)
    
    # Group the data by purchase number
    grouped = multi_piece_purchases.groupby(pedcol)
    
    # Initialize lists to store results
    results = []
    mono_piece_purchases = []
    
    # Iterate over each group
    for purchase_number, group_df in grouped:
        # Sort the group by reception date
        sorted_group = group_df.sort_values(by=datecol)
        
        # Get the first and last reception dates
        first_reception_date = sorted_group.iloc[0][datecol]
        last_reception_date = sorted_group.iloc[-1][datecol]
        
        # Calculate the date difference in days
        date_difference = (last_reception_date - first_reception_date).days
        
        # Append the result to the list
        results.append({'purchase_number': purchase_number, 'date_difference': date_difference})
    
    # Convert the list of results to a DataFrame
    result_df = pd.DataFrame(results)
    
    # Identify mono-piece purchases
    mono_piece_purchases = df[pedcol].unique()
    mono_piece_purchases = [p for p in mono_piece_purchases if p not in result_df[pedcol]]
    
    return result_df, len(mono_piece_purchases), len(results)

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

def calculate_date_diff(col1, col2, seller=None, zona=None, tipo=None, start_date=None, end_date=None):

        filter_conditions = Q()

        if seller:
            filter_conditions &= Q(seller=seller)
        if zona:
            filter_conditions &= Q(zona=zona)
        if tipo:
            filter_conditions &= Q(tipo=tipo)
        if start_date and end_date:
            filter_conditions &= Q(fechaDespacho__gte=start_date, fechaDespacho__lte=end_date)

        query_result = bdoms.objects.filter(filter_conditions).values(col1, col2, 'codigoPostal__Provincia')
        df = pd.DataFrame.from_records(query_result)
        df = df.dropna()
        df['date_difference'] = (df[col2] - df[col1]).dt.days
        A = [d.date() for d in df[col1]]
        B = [d.date() for d in df[col2]]
        df['bdDate_difference'] = np.busday_count(A, B)
        df = df[df['date_difference'] > 0]
        df = df[df['date_difference'] <= df['date_difference'].quantile(0.985)]
        
        return df

def bring_quartile(df, percentage, column):

    dffin = df[df[column] <= df[column].quantile(percentage)]

    return dffin

def mode_group_date_diff(df, grcol, datecol1, datecol2=None):
    if datecol2:
        mode_per_group = df.groupby(grcol)[[datecol1, datecol2]].apply(lambda x: x.mode())
    else:
        mode_per_group = df.groupby(grcol)[datecol1].apply(lambda x: x.mode())
    mode_per_group.reset_index(inplace=True)
    mode_per_group.drop(['level_1'], axis=1, inplace=True)
    mode_per_group = mode_per_group[mode_per_group['codigoPostal__Provincia'] != 'CAPITAL FEDERAL']
    mode_per_group.sort_values(by=datecol1, inplace=True)
    return mode_per_group

def mean_group_date_diff(df, grcol, datecol1, datecol2=None):
    if datecol2:
        mean_per_group = df.groupby(grcol)[[datecol1, datecol2]].apply(lambda x: x.mean())
    else:
        mean_per_group = df.groupby(grcol)[datecol1].apply(lambda x: x.mean())
    mean_per_group.reset_index(inplace=True)

    mean_per_group = mean_per_group[mean_per_group['codigoPostal__Provincia'] != 'CAPITAL FEDERAL']

    # Calculate first quartile for each group
    first_quartile = df.groupby(grcol)[datecol2].quantile(0.25).reset_index()
    first_quartile.rename(columns={datecol2: 'First_Quartile'}, inplace=True)

    second_quartile = df.groupby(grcol)[datecol2].quantile(0.50).reset_index()
    second_quartile.rename(columns={datecol2: 'Second_Quartile'}, inplace=True)

    third_quartile = df.groupby(grcol)[datecol2].quantile(0.75).reset_index()
    third_quartile.rename(columns={datecol2: 'third_quartile'}, inplace=True)

    last_quartile = df.groupby(grcol)[datecol2].quantile(0.95).reset_index()
    last_quartile.rename(columns={datecol2: '95_quartile'}, inplace=True)
    
    # Merge first quartile with mode_per_group DataFrame
    mean_per_group = mean_per_group.merge(first_quartile, on=grcol, how='left')
    mean_per_group = mean_per_group.merge(second_quartile, on=grcol, how='left')
    mean_per_group = mean_per_group.merge(third_quartile, on=grcol, how='left')
    mean_per_group = mean_per_group.merge(last_quartile, on=grcol, how='left')
    
    # Sort by datecol1
    mean_per_group.sort_values(by=datecol1, inplace=True)
    
    return mean_per_group
