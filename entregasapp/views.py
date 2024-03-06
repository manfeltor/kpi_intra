from django.shortcuts import render
import pandas as pd
import numpy as np
from .models import cpPais, bdoms
from django.db.models import Q
import numpy as np
from .forms import DateRangeForm, DeliveryTypesForm
from registerapp.models import UserProfile

# Create your views here.

def generate_main_despacho_vs_entrega_context(user_profile, from_date_form, until_date_form):
    company = user_profile.company

    base_df = calculate_date_diff(first_date_column="fechaDespacho", last_date_column="fechaEntrega", zona="INTERIOR", tipo="DIST", seller=company.nombre, from_date_filter=from_date_form, until_date_filter=until_date_form)

    mode_table = mode_group_date_diff(base_df, "codigoPostal__Provincia", "date_difference", "bdDate_difference")
    html_mode_table = mode_table.to_html(index=False)

    mean_table = mean_group_date_diff(base_df, "codigoPostal__Provincia", "date_difference", "bdDate_difference")
    html_mean_table = mean_table.to_html(index=False)

    context = {'mode_table': html_mode_table, 'mean_table': html_mean_table}
    return context

def fecth_entregas_forms_data(form_dates):

    from_date_form = form_dates.cleaned_data['start_date']
    until_date_form = form_dates.cleaned_data['end_date']

def render_main_despacho_vs_entrega(request):
    if request.method == 'POST':
        form_dates = DateRangeForm(request.POST)
        form_filters = DeliveryTypesForm(request.POST)
        if form_dates.is_valid():
            user_profile = UserProfile.objects.get(user=request.user)
            from_date_form = form_dates.cleaned_data['start_date']
            until_date_form = form_dates.cleaned_data['end_date']
            # amba_filter = form_filters.cleaned_data['AMBA']
            # interior_filter = form_filters.cleaned_data['INTERIOR']         
            context = generate_main_despacho_vs_entrega_context(user_profile, from_date_form, until_date_form)
            context['form'] = form_dates

            return render(request, "entregasmain.html", context)
    else:
        dates_form = DateRangeForm()
        delivery_form = DeliveryTypesForm()

    return render(request, "entregasmain.html", {'dates_form': dates_form, 'delivery_form' : delivery_form})
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

def calculate_date_diff(first_date_column, last_date_column, seller=None, zona=None, tipo=None, from_date_filter=None, until_date_filter=None):

        filter_conditions = Q()

        if seller:
            filter_conditions &= Q(seller=seller)
        if zona:
            filter_conditions &= Q(zona=zona)
        if tipo:
            filter_conditions &= Q(tipo=tipo)
        if from_date_filter and until_date_filter:
            filter_conditions &= Q(fechaDespacho__gte=from_date_filter, fechaDespacho__lte=until_date_filter)

        query_result = bdoms.objects.filter(filter_conditions).values(first_date_column, last_date_column, 'codigoPostal__Provincia')
        df = pd.DataFrame.from_records(query_result)
        df = df.dropna()
        df['date_difference'] = (df[last_date_column] - df[first_date_column]).dt.days
        A = [d.date() for d in df[first_date_column]]
        B = [d.date() for d in df[last_date_column]]
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
