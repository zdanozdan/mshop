from registration.signals import user_registered
from django.dispatch import receiver

"""
look at __init__ where this handler is loaded. This is simple override of default backend behaviour
as we need to have account active as soon as it is created. Registration mail in sent with confirmation code
so we can still check if it has been activated = email was probably valid
"""
@receiver(user_registered)
def register_handler(sender, **kwargs):
    pass
#user = kwargs['user']
#    user.is_active = True
#    user.save()
