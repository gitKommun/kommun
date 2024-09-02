import os
import pandas as pd
from django.core.management.base import BaseCommand
from core.models import Municipality, Province

class Command(BaseCommand):
    help = "Carga municipios desde un archivo Excel"

    def handle(self, *args, **kwargs):
        # Cambia la ruta del archivo Excel según sea necesario
        file_path = os.path.join("media", "data", "municipality_data_full.xlsx")

        # Leer el archivo Excel
        try:
            df = pd.read_excel(file_path, dtype={'UID': str, 'loine_cp': str, 'loine_cm': str})
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error al leer el archivo Excel: {e}"))
            return

        # Validar columnas esperadas
        expected_columns = ['UID', 'loine_cp', 'loine_cm', 'nm']
        if not all(col in df.columns for col in expected_columns):
            self.stdout.write(self.style.ERROR("El archivo Excel no tiene las columnas esperadas."))
            return

        # Procesar cada fila y crear los municipios
        for _, row in df.iterrows():
            try:
                # Asegurar que el código de provincia tenga 2 dígitos
                province_code = str(row['loine_cp']).zfill(2)
                municipality_name = row['nm']
                municipality_code_ine = str(row['UID'])  # Usar el campo UID como code_ine

                # Buscar la provincia correspondiente
                province = Province.objects.get(code=province_code)

                # Crear el municipio
                Municipality.objects.create(
                    code_ine=municipality_code_ine,
                    name=municipality_name,
                    province=province,
                )

            except Province.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Provincia con código {province_code} no encontrada."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error al crear el municipio {municipality_name}: {e}"))

        self.stdout.write(self.style.SUCCESS("Municipios cargados exitosamente."))
