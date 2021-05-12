__author__ = 'com'

from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('services_view', views.services_view, name='services_view'),
    path('get_service_by_id', views.get_service_by_id, name='get_service_by_id'),
    path('save_service', views.save_service, name='save_service'),
    path('remove_service', views.remove_service, name='remove_service'),
    path('get_service_price_by_id', views.get_service_price_by_id, name='get_service_price_by_id'),
    path('bulk_update_price', views.bulk_update_price, name='bulk_update_price'),

    path('softwares_view', views.softwares_view, name='softwares_view'),
    path('save_software', views.save_software, name='save_software'),
    path('get_software_by_id', views.get_software_by_id, name='get_software_by_id'),
    path('remove_software', views.remove_software, name='remove_software'),

    path('orders_view', views.orders_view, name='orders_view'),
    path('orders_datatable_api', views.orders_datatable_api, name='orders_datatable_api'),
    path('get_order_by_id', views.get_order_by_id, name='get_order_by_id'),
    path('save_comment', views.save_comment, name='save_comment'),
    path('accept_order', views.accept_order, name='accept_order'),
    path('cancel_accept_order', views.cancel_accept_order, name='accept_order'),
    path('reject_order', views.reject_order, name='reject_order'),
    path('finish_order', views.finish_order, name='finish_order'),

    path('get_off_days', views.get_off_days, name='get_off_days'),
    path('add_new_off_day', views.add_new_off_day, name='add_new_off_day'),
    path('remove_off_day', views.remove_off_day, name='remove_off_day'),

    path('show_calendar_view', views.show_calendar_view, name='show_calendar_view'),
    path('get_admin_calendar_data', views.get_admin_calendar_data, name='get_admin_calendar_data'),

    path('export_booking', views.export_booking, name='export_booking'),
]