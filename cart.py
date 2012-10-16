# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from shop.models.defaults.bases import BaseCart
import django.http
#import logging

class Cart(BaseCart):

    is_eu_cart = models.BooleanField(default=False, verbose_name=_('IS_EU_CART'))

    #def update(self, state=None):
    #    logging.debug('wow')
    #    return super(Cart,self).update(state)

    def get_items_count(self):
        return self.items.count()

    def delete_item(self, cart_item_id):
        """
        A simple convenience method to delete one of the cart's items. This
        allows to implicitely check for "access rights" since we insure the
        cartitem is actually in the user's cart
        """
        cart_item = self.items.get(pk=cart_item_id)
        cart_item.delete()
        self.save()
        return cart_item

    class Meta(object):
        abstract = False
        app_label = 'shop'
        verbose_name = _('MikranCart')
        verbose_name_plural = _('MikranCarts')


