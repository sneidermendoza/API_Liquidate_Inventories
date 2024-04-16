from django.core.management.base import BaseCommand, CommandError
from apps.generic_tables.seed.generic_seed import ParameterSeeder,AttributesSeeder,OptionsSeeder,MeasureUnitSeeder
from apps.users.seed.user_seed import RoleSeeder,CustomUserSeeder
class Command(BaseCommand):
    """Exec command $ python manage.py db_seed"""
    help='Corre los seeders necesarios para el funcionamiento de la aplciación'

    def add_arguments(self, parser):
        parser.add_argument('--class', nargs='+', type=str)


    def handle(self, *args, **options):

       try:
            class_seeder = options.get('class', None)
            if class_seeder is not None:
                globals()[class_seeder[0]]()
                pass
            else:
                # Se ejecutan todos los seeders

                #seeder del rol admi  
                RoleSeeder.seed()
                #seeder del super user
                CustomUserSeeder.seed()
                #seeder de unidades de medida
                MeasureUnitSeeder.seed()
                #seeder de parametros
                ParameterSeeder.seed()
                #seeder de atributos 
                AttributesSeeder.seed()
                #seeder de opciones
                OptionsSeeder.seed()
            self.stdout.write("Executed seeder ", ending='\n')
       except KeyError:
        print("El seeder especificado no existe")
       except Exception as e:
        raise e
        print("Ha ocurrido un error no previsto", type(e).__name__ )