import pandas as pd
from django.core.management.base import BaseCommand
from entregasapp.models import bdoms
from entregasapp.views import importar_excel_tms

class Command(BaseCommand):
    help = 'Import data from Excel file into database'

    def handle(self, *args, **kwargs):
        
        excel_data = importar_excel_tms(r'C:\Users\ftorres\OneDrive - INTRALOG ARGENTINA S.A\kpi\dash_pr\TMS_por_meses\*.xlsx')

        for index, row in excel_data.iterrows():
            bdoms.objects.create(**row.to_dict())

        self.stdout.write(self.style.SUCCESS('Data imported successfully.'))