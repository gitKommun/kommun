from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction

class Command(BaseCommand):
    help = 'Inicializa la base de datos con datos básicos y de prueba'

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
                self.stdout.write(self.style.WARNING('Iniciando población de la base de datos...'))
                
                # 1. Poblar roles
                self.stdout.write(self.style.WARNING('1. Poblando roles...'))
                call_command('populate_roles')
                self.stdout.write(self.style.SUCCESS('✓ Roles poblados correctamente\n'))

                # 2. Poblar provincias
                self.stdout.write(self.style.WARNING('2. Poblando provincias...'))
                call_command('populate_provinces')
                self.stdout.write(self.style.SUCCESS('✓ Provincias pobladas correctamente\n'))

                # 3. Crear entorno de prueba
                self.stdout.write(self.style.WARNING('3. Creando entorno de prueba...'))
                call_command('populate_test_env')
                self.stdout.write(self.style.SUCCESS('✓ Entorno de prueba creado correctamente\n'))

                self.stdout.write(self.style.SUCCESS("""
╔════════════════════════════════════════╗
║    Base de datos inicializada con:     ║
║    - Roles básicos                     ║
║    - Provincias de España              ║
║    - Datos de prueba                   ║
║                                        ║
║    Proceso completado con éxito        ║
╚════════════════════════════════════════╝
                """))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"""
╔════════════════════════════════════════╗
║    ¡Error durante la inicialización!   ║
║    {str(e)}
╚════════════════════════════════════════╝
            """))
            raise e
