from django.core.management.base import BaseCommand
from core.models import Province  # Suponiendo que la app se llame common

class Command(BaseCommand):
    help = 'Populates the Province table with data'

    def handle(self, *args, **kwargs):
        provinces = [
            {"cpine": "15", "name": "A CORUÑA"},
            {"cpine": "03", "name": "ALACANT"},
            {"cpine": "02", "name": "ALBACETE"},
            {"cpine": "04", "name": "ALMERIA"},
            {"cpine": "33", "name": "ASTURIAS"},
            {"cpine": "05", "name": "AVILA"},
            {"cpine": "06", "name": "BADAJOZ"},
            {"cpine": "08", "name": "BARCELONA"},
            {"cpine": "09", "name": "BURGOS"},
            {"cpine": "10", "name": "CACERES"},
            {"cpine": "11", "name": "CADIZ"},
            {"cpine": "39", "name": "CANTABRIA"},
            {"cpine": "12", "name": "CASTELLO"},
            {"cpine": "51", "name": "CEUTA"},
            {"cpine": "13", "name": "CIUDAD REAL"},
            {"cpine": "14", "name": "CORDOBA"},
            {"cpine": "16", "name": "CUENCA"},
            {"cpine": "17", "name": "GIRONA"},
            {"cpine": "18", "name": "GRANADA"},
            {"cpine": "19", "name": "GUADALAJARA"},
            {"cpine": "21", "name": "HUELVA"},
            {"cpine": "22", "name": "HUESCA"},
            {"cpine": "07", "name": "ILLES BALEARS"},
            {"cpine": "23", "name": "JAEN"},
            {"cpine": "26", "name": "LA RIOJA"},
            {"cpine": "35", "name": "LAS PALMAS"},
            {"cpine": "24", "name": "LEON"},
            {"cpine": "25", "name": "LLEIDA"},
            {"cpine": "27", "name": "LUGO"},
            {"cpine": "28", "name": "MADRID"},
            {"cpine": "29", "name": "MALAGA"},
            {"cpine": "52", "name": "MELILLA"},
            {"cpine": "30", "name": "MURCIA"},
            {"cpine": "32", "name": "OURENSE"},
            {"cpine": "34", "name": "PALENCIA"},
            {"cpine": "36", "name": "PONTEVEDRA"},
            {"cpine": "38", "name": "S.C. TENERIFE"},
            {"cpine": "37", "name": "SALAMANCA"},
            {"cpine": "40", "name": "SEGOVIA"},
            {"cpine": "41", "name": "SEVILLA"},
            {"cpine": "42", "name": "SORIA"},
            {"cpine": "43", "name": "TARRAGONA"},
            {"cpine": "44", "name": "TERUEL"},
            {"cpine": "45", "name": "TOLEDO"},
            {"cpine": "46", "name": "VALENCIA"},
            {"cpine": "47", "name": "VALLADOLID"},
            {"cpine": "49", "name": "ZAMORA"},
            {"cpine": "50", "name": "ZARAGOZA"},
            {"cpine": "31", "name": "NAVARRA"},
            {"cpine": "01", "name": "ÁLAVA"},
            {"cpine": "20", "name": "GUIPÚZCOA"},
            {"cpine": "48", "name": "VIZCAYA"}
        ]
        for province_data in provinces:
            Province.objects.get_or_create(code=province_data['cpine'], name=province_data['name'])
        self.stdout.write(self.style.SUCCESS('Provinces have been populated'))
