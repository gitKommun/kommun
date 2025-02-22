# DOCUMENTACION
# La documentacion esta disponible en la siguientes urls:
/core/swagger/
/core/redoc/

# Instrucciones para Poblar Datos Iniciales

# Requisitos Previos
# Asegúrate de haber configurado correctamente el entorno de Django y de haber ejecutado las migraciones de base de datos:
python manage.py makemigrations
python manage.py migrate

# Poblar Provincias
# Para cargar las provincias en la base de datos, ejecuta el siguiente comando:
python manage.py populate_provinces

# Poblar Municipios
# Para cargar los municipios en la base de datos, ejecuta el siguiente comando:

python manage.py populate_municipalities
# La carga se realiza a partir de un fichero excel ubicato en `media/data/municipalities_data_full.xlsx`. Esta version contiene todos municipios de España, incluidos los que no estan referenciados en el catastro (Pais Vasco + Navarra). 

# Poblar Codigos Postales
python manage.py populate_cp
# La carga se realiza a partir de un fichero excel ubicato en `media/data/municipalities_data_cp.xlsx`.

# Poblar Roles
# Para cargar los roles disponibles en el sistema, ejecuta el siguiente comando:
python manage.py populate_roles

#DJANGO COMANDOS UNIVERSALES
#Crear superuser para panel admin
python manage.py createsuperuser

# Estándares Utilizados en el Proyecto

```python
'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S',  # ISO 8601
'DATE_FORMAT': '%Y-%m-%d',
'TIME_FORMAT': '%H:%M',
```


