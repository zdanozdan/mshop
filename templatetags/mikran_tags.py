# -*- coding: utf-8 -*-
from django import template

from classytags.core import Tag

from shop.util.cart import get_or_create_cart
from shop.models.productmodel import Product
from shop.forms import get_cart_item_formset

import logging

register = template.Library()


class MikranCart(Tag):
    """
    Inclusion tag for displaying cart summary.
    """
    name = "cart_items"

    def render_tag(self, context):
        cart = get_or_create_cart(context['request'])
        cart.update()
        context['cart'] = cart
        context['cart_items': cart.get_updated_cart_items()]
        formset = get_cart_item_formset(cart_items=context['cart_items'])
        context['formset': formset]

        return ''

register.tag(MikranCart)
