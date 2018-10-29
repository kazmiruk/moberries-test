from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from pizza.docs import schema_view
from pizza.views.customer import CustomerViewSet
from pizza.views.customer_address import CustomerAddressViewSet
from pizza.views.order import OrderViewSet
from pizza.views.pizza import PizzaViewSet


router = routers.SimpleRouter()
router.register(r'customers/(?P<customer_id>\d+)/addresses', CustomerAddressViewSet, base_name='customer_addresses')
router.register(r'customers/(?P<customer_id>\d+)/orders', OrderViewSet, base_name='customer_orders')
router.register(r'customers', CustomerViewSet, base_name='customers')
router.register(r'pizzas', PizzaViewSet, base_name='pizzas')

urlpatterns = [
    url(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
url(r'^api/v1/', include((router.urls, 'api-v1'), namespace='v1')),
]
