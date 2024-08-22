from django.core.management.base import BaseCommand
from django.db import IntegrityError
from apps.generic_tables.models import MeasureUnits, Parameter, Attributes, Options, Menus
from apps.users.models import Role
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
            parameter, created = Parameter.objects.get_or_create(name='inventario', description='parametros de Inventario')
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
            # Obtener o crear el parámetro de facturación
            billing_parameter, _ = Parameter.objects.get_or_create(name='facturacion', description='parametros de facturacion')
            
            # Crear los atributos asociados al parámetro de facturación
            Attributes.objects.get_or_create(name='cancelado', parameter=billing_parameter)
            Attributes.objects.get_or_create(name='pendiente', parameter=billing_parameter)
            
            # Obtener o crear el parámetro de inventario
            inventory_parameter, _ = Parameter.objects.get_or_create(name='inventario', description='parametros de Inventario')

            # Crear los atributos asociados al parámetro de inventario
            Attributes.objects.get_or_create(name='en proceso', parameter=inventory_parameter)
            Attributes.objects.get_or_create(name='sin empezar', parameter=inventory_parameter)
            Attributes.objects.get_or_create(name='finalizado', parameter=inventory_parameter)
            
            print('Atributos creados correctamente.')
            
        except IntegrityError as e:
            print(f'Error de base de datos al crear el atributo: {e}')

class OptionsSeeder:
    @classmethod
    def seed(cls):
        try:
            admin_role = Role.objects.get(name='admin')
            options = [
                ('opcion', 'gestion de opciones', '/option'),
                ('menu', 'gestion de menu', '/menu'),
                ('unidades de medida', 'gestion de unidades de medida', '/measure_units'),
                ('atributos', 'gestion de atributos', '/attributes'),
                ('parametros', 'gestion de parametros', '/parameters'),
                ('facturacion', 'gestion de facturacion', '/billings'),
                ('inventario', 'gestion de inventario', '/inventory'),
                ('detalle de inventarios', 'gestion de detalle de inventarios', '/detail_inventory'),
                ('usuarios', 'gestion de usuarios', '/users'),
                ('negosios', 'gestion de negosios', '/business'),
                ('productos', 'gestion de productos', '/products'),
                ('roles', 'gestion de roles', '/role')
            ]
            for name, description, link in options:
                option, created = Options.objects.get_or_create(name=name, description=description, link=link)
                if created:
                    print(f'Opción "{name}" creada correctamente.')
                else:
                    print(f'La opción "{name}" ya existe.')
                
                # Crear una instancia de Menus que relacione la opción con el rol
                menu, _ = Menus.objects.get_or_create(option=option, role=admin_role)
                
        except IntegrityError as e:
            print(f'Error de base de datos al crear la opción: {e}')
