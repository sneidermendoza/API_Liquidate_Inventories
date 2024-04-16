from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.users.models import CustomUser, Role

class RoleSeeder:
    @staticmethod
    def seed():
        try:
            # Crear el rol (Group) si no existe
            role, created = Role.objects.get_or_create(name='admin')
            if created:
                print('Rol "Admin" creado correctamente.')
            else:
                print('El rol "Admin" ya existe.')
        except Exception as e:
            print(f'Error al crear el rol: {e}')

class CustomUserSeeder:
    @staticmethod
    def seed():
        try:
            # Crear el superusuario si no existe
            User = get_user_model()
            user, created = CustomUser.objects.get_or_create(
                email='mariasol0304@gmail.com',
                defaults={'name': 'sneider', 'last_name': 'mendoza', 'is_superuser': True, 'is_staff': True}
            )
            if created:
                user.set_password('Cc1045698090')
                user.save()
                # Asignar el rol al usuario
                role = Role.objects.get(name='admin')
                user.role = role
                user.save()

                print('Superusuario creado correctamente y asignado al rol "Admin".')
            else:
                print('El superusuario ya existe.')
        except Exception as e:
            print(f'Error al crear el superusuario: {e}')

