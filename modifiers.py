1# -*- coding: utf-8 -*-
from decimal import Decimal
from shop.cart.cart_modifiers_base import BaseCartModifier
from countries.locale.countries_info import COUNTRY_LIST_EU
import logging

class CurrencyModifier(BaseCartModifier):
    #def __init__(self, *args, **kwargs):
    #    super(BaseCartModifier, self).__init__(*args, **kwargs)

    #def pre_process_cart(self, cart, state):
        #self.rate = cart.is_eu_cart
        #if 'currency' in state:
        #    self.currency = state['currency'] in COUNTRY_LIST_EU

    def get_extra_cart_item_price_field(self, cart_item):
        #logging.debug('Currency')
        amount_with_vat = 0

class VatPerItemTaxModifier(BaseCartModifier):

    def __init__(self, *args, **kwargs):
        super(BaseCartModifier, self).__init__(*args, **kwargs)
        self.is_eu = False

    def pre_process_cart(self, cart, state):
        self.is_eu_cart = cart.is_eu_cart
        if 'country' in state:
            self.is_eu = state['country'] in COUNTRY_LIST_EU

    def process_cart_item(self, cart_item, state):
        if self.is_eu == False:
            return super(VatPerItemTaxModifier,self).process_cart_item(cart_item,state)

        field = self.get_extra_cart_item_price_field(cart_item)
        price = field[1]
        cart_item.current_total = price
        cart_item.extra_price_fields.append(field)

        return cart_item

    """
    This adds a VAT tax cart modifier, calculated on the item's given tax,
    plus any modifier applied to the cart item *so far* (order matters!).
    """

    def get_extra_cart_item_price_field(self, cart_item):
        if self.is_eu == False:
            return None

        if self.is_eu_cart:
            vat = 1
            amount_with_vat = cart_item.current_total*vat
            return (('%s%s') % (0,' % EU') ,amount_with_vat*cart_item.quantity, amount_with_vat)
        else:
            amount_with_vat = cart_item.product.get_price_brutto()
            return (('%s%s') % (cart_item.product.get_vat(),' %') ,amount_with_vat*cart_item.quantity, amount_with_vat)

        #def get_extra_cart_price_field(self, cart):
        #return ('Taxes total', Decimal('19.00'))



            

