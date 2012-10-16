# -*- coding: utf-8 -*-

from decimal import Decimal
from unidecode import unidecode

from shop.models import Product
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify

#from shop.util.fields import CurrencyField
from django.utils.translation import ugettext_lazy as _
from shop.models.defaults.bases import BaseCart
from curr_conv.models import Rates

from django.utils import translation
import logging

class MikranProduct(Product):

    name_pl = models.CharField(max_length=255, verbose_name=_('Product name'))
    name_en = models.CharField(max_length=255, verbose_name=_('Product name'))
    name_de = models.CharField(max_length=255, verbose_name=_('Product name'))
    name_fr = models.CharField(max_length=255, verbose_name=_('Product name'))
    name_es = models.CharField(max_length=255, verbose_name=_('Product name'))
    name_sk = models.CharField(max_length=255, verbose_name=_('Product name'))
    description_pl = models.TextField(blank=True,verbose_name=_('Description'))
    description_en = models.TextField(blank=True,verbose_name=_('Description'))
    description_de = models.TextField(blank=True,verbose_name=_('Description'))
    description_fr = models.TextField(blank=True,verbose_name=_('Description'))
    description_es = models.TextField(blank=True,verbose_name=_('Description'))
    description_sk = models.TextField(blank=True,verbose_name=_('Description'))

    vat = models.DecimalField(max_digits=2,decimal_places=0,verbose_name=_('VAT'))
    native_price = models.DecimalField(max_digits=30,decimal_places=2,verbose_name=_('Original price'))
    #active = models.BooleanField(default=False,verbose_name=_('Active'))

    current_rate = 0.0
    current_spread = 0.0
    current_unit = 1

    """
    So when there is no such symbol in db expection is raise
    what should we do ? - probably assume some stupid thing and reset
    currency settings into default ones to we still able to use an app ...
    1. Symbol does not exst in DB - need to reset settings and change to default currency - PLN
    """
    @staticmethod
    def set_currency(request,code):
        MikranProduct.current_rate = 0.0
        MikranProduct.current_spread = 0.0
        MikranProduct.current_unit = 1

        if code == settings.HOME_CURRENCY:
            return True

        try:
            rate = Rates.objects.filter(symbol=code).latest('created')
            MikranProduct.current_rate = rate.average
            MikranProduct.current_spread = rate.spread
            MikranProduct.current_unit = rate.unit
            return True

        except Rates.DoesNotExist:
            return False


    def get_vat(self):
        return Decimal(23)

    def calculate_price(self,price):
        if MikranProduct.current_rate:
            return ((price / MikranProduct.current_rate) * MikranProduct.current_unit).quantize(Decimal('.01'))
        return Decimal(price).quantize(Decimal('.01'));

    def get_price_brutto(self):
        return (self.get_price() * Decimal(self.get_vat() / 100 + 1)).quantize(Decimal('.01'))

    def get_native_price(self):
        return self.native_price

    def get_price(self):
        return self.calculate_price(self.get_native_price())

    def get_name(self):
        """
        Return the name of this Product based on current translation)
        """
        #return self.name + translation.get_language()
        name = getattr(self, 'name_'+translation.get_language())
        if name:
            return name

        return "["+translation.get_language() + "] " + self.name + " [" + translation.get_language() + "]"

    def save_to_fix_in_the_future(self, *args, **kwargs):
        """
        Based on the Tag save() method in django-taggit, this method simply
        stores a slugified version of the title, ensuring that the unique
        constraint is observed
        """
        s = slugify(unidecode(self.name))
        return super(MikranProduct, self).save(*args, **kwargs)

    class Meta:
        pass


