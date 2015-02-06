

from django.dispatch import Signal

user_signed_in = Signal(providing_args=('user',))
user_registration_problem = Signal(providing_args=('user', 'message'))