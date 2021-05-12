from rbasis.urlrouter import router
from . import views

def RegPath():
    router.register(r'contactus', views.contactusView, 'contactus', ''),
    router.register(r'devicetypes', views.devicetypesView, 'devicetypes', ''),
    router.register(r'menu', views.menu, 'menu', ''),
    router.register(r'offdays', views.offdaysView, 'offdays', ''),
    router.register(r'orders', views.ordersView, 'orders', ''),
    router.register(r'oss', views.ossView, 'oss', ''),
    router.register(r'prices', views.pricesView, 'prices', ''),
    router.register(r'room', views.roomView, 'room', ''),
    router.register(r'services', views.servicesView, 'services', ''),
    router.register(r'softwares', views.softwaresView, 'softwares', ''),
    router.register(r'transactions', views.transactionsView, 'transactions', ''),
    router.register(r'users', views.tblusersView, 'users', ''),