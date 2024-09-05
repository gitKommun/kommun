import os
import pandas as pd
from django.core.management.base import BaseCommand
from core.models import Municipality, PostalCode

class Command(BaseCommand):
    help = "Carga códigos postales desde un archivo Excel y los asocia con los municipios"

    def handle(self, *args, **kwargs):
        # Ruta del archivo Excel
        file_path = os.path.join("media", "data", "cp_data.xlsx")

        # Leer el archivo Excel
        try:
            df = pd.read_excel(file_path, dtype={'ine': str, 'cp': str})  
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error al leer el archivo Excel: {e}"))
            return

        # Validar columnas esperadas
        expected_columns = ['ine', 'cp', 'nm']
        if not all(col in df.columns for col in expected_columns):
            self.stdout.write(self.style.ERROR("El archivo Excel no tiene las columnas esperadas."))
            return

        # Procesar cada fila y crear las relaciones entre Municipio y Código Postal
        for _, row in df.iterrows():
            try:
                # Buscar el municipio correspondiente usando el INE
                municipality_code_ine = row['ine']
                municipality = Municipality.objects.get(code_ine=municipality_code_ine)

                # Crear el código postal asociado al municipio
                PostalCode.objects.create(
                    postal_code=row['cp'],
                    municipality=municipality
                )

            except Municipality.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Municipio con código INE {municipality_code_ine} no encontrado."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error al crear la relación para el código postal {row['cp']}: {e}"))

        self.stdout.write(self.style.SUCCESS("Códigos postales cargados exitosamente."))

