from registration.signals import user_registered
from django.contrib.auth.signals import user_logged_in,user_logged_out
from django.contrib import messages
from django.dispatch import receiver
from django.utils.translation import ugettext as _

"""
look at __init__ where this handler is loaded. This is simple override of default backend behaviour
as we need to have account active as soon as it is created. Registration mail in sent with confirmation code
so we can still check if it has been activated = email was probably valid
"""
#@receiver(user_registered)
#def register_handler(sender, **kwargs):
#    pass
#user = kwargs['user']
#    user.is_active = True
#    user.save()

@receiver(user_logged_in)
def logged_in_handler(sender, request, user, **kwargs):
    messages.add_message(request,messages.SUCCESS, _("Hello %s. Welcome back @ mikran.com.") % user)

@receiver(user_logged_out)
def logged_out_handler(sender, request, **kwargs):
    messages.add_message(request,messages.SUCCESS, _("Thank You for visiting us @ mikran.com."))

# Wait for this till 1.5
#
#@receiver(user_login_failed)
#def register_handler(sender, request, **kwargs):
#    messages.add_message(request,messages.ERROR, _("Login failed."))
