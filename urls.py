from django.conf.urls import patterns,include,url
from views import MikranCartDetails, MikranCartItemDetail
#from shop.views.cart import CartItemDetail

urlpatterns = patterns('mshop.views',
    url(r'^$', 'shop', name='main_page'),
    url(r'^update/$', MikranCartDetails.as_view(action='put'),name='mikran_cart_update'),
    url(r'^update/ue$', MikranCartDetails.as_view(action='post'),name='mikran_eu_cart_update'),
    url(r'^mikran/cart/get/$', MikranCartDetails.as_view(action='get'),name='mikran_cart_get'),
    url(r'^mikran/cart/(?P<id>[0-9A-Za-z-_.//]+)/delete/$',MikranCartDetails.as_view(action='delete'),name='mikran_cart_item_delete'),

    url(r'^mikran/cart/add/$', MikranCartItemDetail.as_view(action='post'),name='mikran_cart_add'),
    url(r'^mikran/show/cart/$', MikranCartItemDetail.as_view(),name='mikran_cart'),
)
