# This Python file uses the following encoding: utf-8

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from shop.views.cart import CartDetails, CartItemDetail
from shop.views import ShopListView
from models import MikranProduct

import logging

from shop.util.cart import get_or_create_cart
from shop.forms import get_cart_item_formset

from shop.models.cartmodel import Cart,CartItem
from shop.forms import CartItemModelForm

from forms import CartForm

class WelcomeListView(ShopListView):
    template_name = 'welcome.html'
    model = MikranProduct

    def dispatch(self, *args, **kwargs):
        return super(WelcomeListView, self).dispatch(*args, **kwargs)

    def do_currency_switch(self):
        currency = self.request.session.get(settings.CURRENCY_COOKIE_NAME)
        if currency in settings.CURRENCIES_LIST:
            if MikranProduct.set_currency(self.request, code=currency) is True:
                #logging.debug('currency set OK')
                return

            if MikranProduct.set_currency(self.request, code=settings.DEFAULT_CURRENCY) is True:
                output = _('Error setting currency. Switched to default currency :  %(currency)s') % {'currency': settings.DEFAULT_CURRENCY }
                messages.add_message(self.request,messages.ERROR, output)
                self.request.session[settings.CURRENCY_COOKIE_NAME] = settings.DEFAULT_CURRENCY
                return

        """ error currency setting """
        if currency != settings.HOME_CURRENCY:
            output = _('Error setting currency. Switched to default currency :  %(currency)s') % {'currency': settings.DEFAULT_CURRENCY }
            messages.add_message(self.request,messages.ERROR, output)
            self.request.session[settings.CURRENCY_COOKIE_NAME] = settings.DEFAULT_CURRENCY

    def get_queryset(self):
        return MikranProduct.objects.all()[:5]

    def get_context_data(self, **kwargs):
        ctx = super(ShopListView, self).get_context_data(**kwargs)

        #set up the currency before we use the cart itself
        self.do_currency_switch()

        state={'country':self.request.session.get('django_country')}
        cart_object = get_or_create_cart(self.request)
        cart_object.update(state)
        ctx.update({'cart': cart_object})
        ctx.update({'cart_items': cart_object.get_updated_cart_items()})

        formset = get_cart_item_formset(cart_items=ctx['cart_items'])
        ctx.update({'formset': formset, })

        ctx.update({'cart_form': CartForm(instance=cart_object) })

        return ctx

class MikranCart(CartDetails):

    def update_context_with_cart_form(self,ctx):

        cart_object = get_or_create_cart(self.request)
        state={'country':self.request.session.get('django_country')}
        cart_object.update(state)
        ctx.update({'cart': cart_object})
        ctx.update({'cart_items': cart_object.get_updated_cart_items()})

        formset = get_cart_item_formset(cart_items=ctx['cart_items'])
        ctx.update({'formset': formset, })

        ctx.update({'cart_form': CartForm(instance=cart_object) })

        return ctx


class MikranCartItemDetail(MikranCart):
    template_name = "cart.html"

    def post_success(self, product, cart_item):
        """
        Post success hook
        """
        messages.add_message(self.request,messages.INFO, _('Product (%s) has been added to basket') % (product),extra_tags='basket_only')
        return redirect(self.request.POST.get('next'))

    def get(self, request, *args, **kwargs):
        #ctx = super(ShopListView, self).get_context_data(**kwargs)

        ctx = self.get_context_data(**kwargs)
        self.update_context_with_cart_form(ctx)

        return self.render_to_response(ctx)

class MikranCartDetails(MikranCart):
    template_name = 'cart.html'

    def get(self, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        self.update_context_with_cart_form(context)

        return self.render_to_response(context)

    """
    Deletes one of the cartItems. This should be posted to a properly
    RESTful URL (that should contain the item's ID):
    
    http://example.com/shop/cart/item/12345
    """

    def delete(self, request, *args, **kwargs):
        cart_object = get_or_create_cart(self.request)
        item_id = self.kwargs.get('id')
        item = cart_object.delete_item(item_id)

        messages.add_message(request,messages.INFO, _('Product (%s) has been deleted from basket') % (item.product),extra_tags='basket_only')

        if cart_object.get_items_count() == 0:
            messages.add_message(request,messages.WARNING, _('You have deleted all products. Basket in empty now.'),extra_tags='basket_only')
    
        return self.redirect()

    def post(self, *args, **kwargs):

        cart_object = get_or_create_cart(self.request)
        f = CartForm(self.request.POST,instance=cart_object)
        if f.is_valid():
            f.save()
            #Message only for EU cart clickers
            if cart_object.is_eu_cart:
                messages.add_message(self.request,messages.INFO, _('Remember that you need to have valid EU VAT number to claim 0% EU VAT rate'),extra_tags='basket_only')
        else:
            messages.add_message(self.request,messages.ERROR, _('Error changing VAT rate.'),extra_tags='basket_only')

        return redirect(self.request.POST.get('next'))

    def put(self, *args, **kwargs):
        """ Update shopping cart form. """

        context = self.get_context_data(**kwargs)
        self.update_context_with_cart_form(context)
        formset = get_cart_item_formset(cart_items=context['cart_items'],data=self.request.POST)

        """ valid form redirects to get cart again, otherwise re-display form with errors """
        if formset.is_valid():
            formset.save()
            messages.add_message(self.request,messages.INFO, _('Item quantity has been successfully changed.'),extra_tags='basket_only')
            return self.redirect()

        messages.add_message(self.request,messages.ERROR, _('Unable to change item quantity.'),extra_tags='basket_only')
        context.update({'formset': formset, })
        return self.render_to_response(context)

    """ ajax call redirects to render cart object only, otherwise we want to redirect to next, or main page if next is missing"""
    def redirect(self):
        if self.request.is_ajax():
            return HttpResponseRedirect(reverse('mikran_cart_get'))
            
        if self.request.POST.get('next') is not None:
            return HttpResponseRedirect(self.request.POST.get('next'))
            
        return HttpResponseRedirect(reverse('main_page'))

def shop(request):
    return render_to_response('welcome.html',
                              context_instance=RequestContext(request))



