from django.core.management.base import BaseCommand
from django.db import IntegrityError
from apps.generic_tables.models import MeasureUnits, Parameter, Attributes, Options, Menus
from apps.users.models import Role

class MeasureUnitSeeder:
    @classmethod
    def seed(cls):
        try:
            MeasureUnits.objects.get_or_create(name='unidad')
            MeasureUnits.objects.get_or_create(name='docena')
            MeasureUnits.objects.get_or_create(name='gramo')
            measure_unit, created = MeasureUnits.objects.get_or_create(name='Kilogramo')
            if created:
                print('Unidad de medida creada correctamente.')
            else:
                print('La unidad de medida ya existe.')
        except IntegrityError as e:
            print(f'Error de base de datos al crear la unidad de medida: {e}')

class ParameterSeeder:
    @classmethod
    def seed(cls):
        try:
            parameter, created = Parameter.objects.get_or_create(name='facturacion', description='parametros de facturacion')
            if created:
                print('Parámetro creado correctamente.')
            else:
                print('El parámetro ya existe.')
        except IntegrityError as e:
            print(f'Error de base de datos al crear el parámetro: {e}')

class AttributesSeeder:
    @classmethod
    def seed(cls):
        try:
            parameter, created = Parameter.objects.get_or_create(name='facturacion', description='parametros de facturacion')
            attributes, created = Attributes.objects.get_or_create(name='cancelado', parameter=parameter)
            attributes, created = Attributes.objects.get_or_create(name='pendiente', parameter=parameter)
            if created:
                print('Atributo creado correctamente.')
            else:
                print('El atributo ya existe.')
        except IntegrityError as e:
            print(f'Error de base de datos al crear el atributo: {e}')

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from apps.generic_tables.models import MeasureUnits, Parameter, Attributes, Options, Menus
from apps.users.models import Role

class OptionsSeeder:
    @classmethod
    def seed(cls):
        try:
            admin_role = Role.objects.get(name='admin')
            options = [
                ('opcion', 'gestion de opciones'),
                ('menu', 'gestion de menu'),
                ('unidades de medida', 'gestion de unidades de medida'),
                ('atributos', 'gestion de atributos'),
                ('parametros', 'gestion de parametros'),
                ('facturacion', 'gestion de facturacion'),
                ('inventario', 'gestion de inventario'),
                ('detalle de inventarios', 'gestion de detalle de inventarios'),
                ('usuarios', 'gestion de usuarios'),
                ('negosios', 'gestion de negosios'),
                ('productos', 'gestion de productos'),
                ('roles', 'gestion de roles')
            ]
            for name, description in options:
                option, created = Options.objects.get_or_create(name=name, description=description)
                if created:
                    print(f'Opción "{name}" creada correctamente.')
                else:
                    print(f'La opción "{name}" ya existe.')
                
                # Crear una instancia de Menus que relacione la opción con el rol
                menu, _ = Menus.objects.get_or_create(option=option, role=admin_role)
                
        except IntegrityError as e:
            print(f'Error de base de datos al crear la opción: {e}')
