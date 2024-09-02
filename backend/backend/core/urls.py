from django.urls import path, re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from core.views import ProvinceListAPIView, MunicipalityListAPIView
from core.views import PostalCodeListAPIView, PostalCodeListByProvinceAPIView, PostalCodeByINEAPIView, MunicipalityByPostalCodeAPIView

schema_view = get_schema_view(
   openapi.Info(
      title="API Documentation",
      default_version='v1',
      description="Documentación de la API para el proyecto",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="soporte@tudominio.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('provinces/', ProvinceListAPIView.as_view(), name='province-list-api'),  #Lista completa de provincias
    
    path('municipalities/', MunicipalityListAPIView.as_view(), name='municipality-list-api'),  #Lista completa de municipios
    path('municipalities/<str:province_code>/', MunicipalityListAPIView.as_view(), name='municipality-list-by-province'),  #Lista de municipios filtrados por provincia
    path('municipalities/postal-code/<str:postal_code>/', MunicipalityByPostalCodeAPIView.as_view(), name='municipality-by-postal-code'),  # Devolver municipio a partir del código postal

    path('postal-codes/', PostalCodeListAPIView.as_view(), name='postal-code-list-api'),  # Lista completa de códigos postales
    path('postal-codes/province/<str:province_code>/', PostalCodeListByProvinceAPIView.as_view(), name='postal-code-list-by-province'),  # Filtrado por provincia
    path('postal-codes/ine/<str:code_ine>/', PostalCodeByINEAPIView.as_view(), name='postal-code-by-ine'),  # Devolver código postal a partir del código INE

    #Documentacion Swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Otras URLs de tu proyecto

]
 