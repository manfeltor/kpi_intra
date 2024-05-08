from django.core.management.base import BaseCommand
from entregasapp.models import bdoms
from entregasapp.views import importar_excel_tms

class Command(BaseCommand):
    help = 'Import data from Excel file into database'

    def handle(self, *args, **kwargs):
        
        excel_data = importar_excel_tms(r'C:\Users\ftorres\OneDrive - INTRALOG ARGENTINA S.A\kpi\braw\mrgd\mrgd.xlsx')
        total_rows = len(excel_data)
        rows_inserted = 0

        for index, row in excel_data.iterrows():
            try:
                bdoms.objects.create(**row.to_dict())
                rows_inserted += 1
                # Calculate progress percentage
                progress_percentage = (rows_inserted / total_rows) * 100

                # Print progress at every 5% interval
                rounded_progress = round(progress_percentage)
                if rounded_progress % 5 == 0 and rounded_progress != last_printed:
                    print(f"Progress: {progress_percentage:.2f}%")
                    last_printed = rounded_progress
            except Exception as e:
                print(f"Error inserting row {index + 1}: {e}")
                print(f"Problematic data: {row}")

        self.stdout.write(self.style.SUCCESS('Data imported successfully.'))