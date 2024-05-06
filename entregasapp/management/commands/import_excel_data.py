import pandas as pd
from django.core.management.base import BaseCommand
from entregasapp.models import bdoms
from entregasapp.views import importar_excel_tms

class Command(BaseCommand):
    help = 'Import data from Excel file into database'

    def handle(self, *args, **kwargs):
        
        excel_data = importar_excel_tms(r'C:\Users\ftorres\OneDrive - INTRALOG ARGENTINA S.A\kpi\braw\mrgd.xlsx')

        for index, row in excel_data.iterrows():
            try:
                bdoms.objects.create(**row.to_dict())
            except Exception as e:
                print(f"Error inserting row {index + 1}: {e}")
                print(f"Problematic data: {row}")
                
        self.stdout.write(self.style.SUCCESS('Data imported successfully.'))

# class Command(BaseCommand):
#     help = 'Delete all data from bdoms table'

#     def handle(self, *args, **kwargs):
#         # Delete all data from the bdoms table
#         bdoms.objects.all().delete()

#         self.stdout.write(self.style.SUCCESS('All data deleted successfully.'))