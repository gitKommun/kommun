from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404
from core.models import Municipality, Province, PostalCode

class ProvinceListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        provinces = Province.objects.all().values('code', 'name')
        return Response(list(provinces))

class MunicipalityListAPIView(APIView):
    def get(self, request, province_code=None, *args, **kwargs):
        if province_code:
            province = get_object_or_404(Province, code=province_code)
            municipalities = Municipality.objects.filter(province=province).values('code_ine', 'name')
        else:
            municipalities = Municipality.objects.all().values('code_ine', 'name')
        
        return Response(list(municipalities))

class MunicipalityByPostalCodeAPIView(APIView):
    def get(self, request, postal_code, *args, **kwargs):
        # Obtener todos los municipios asociados a un código postal
        postal_code_instances = get_list_or_404(PostalCode, postal_code=postal_code)
        
        # Construir la respuesta con todos los municipios relacionados con el código postal
        municipalities_data = []
        for postal_code_instance in postal_code_instances:
            municipalities_data.append({
                'municipality_name': postal_code_instance.municipality.name,
                'code_ine': postal_code_instance.municipality.code_ine
            })

        return Response(municipalities_data)

class PostalCodeListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        postal_codes = PostalCode.objects.all().values('postal_code', 'municipality__name', 'municipality__code_ine')
        return Response(list(postal_codes))
    
class PostalCodeListByProvinceAPIView(APIView):
    def get(self, request, province_code, *args, **kwargs):
        province = get_object_or_404(Province, code=province_code)
        postal_codes = PostalCode.objects.filter(municipality__province=province).values('postal_code', 'municipality__name', 'municipality__code_ine')
        return Response(list(postal_codes))
    
class PostalCodeByINEAPIView(APIView):
    def get(self, request, code_ine, *args, **kwargs):
        municipality = get_object_or_404(Municipality, code_ine=code_ine)
        postal_codes = PostalCode.objects.filter(municipality=municipality).values('postal_code', 'municipality__name')
        return Response(list(postal_codes))