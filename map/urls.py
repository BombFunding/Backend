
from django.urls import path
from map.views import PinListView, PinCreateView

urlpatterns = [
    path('pins/', PinListView.as_view(), name='list_pins'),  
    path('pins/add/', PinCreateView.as_view(), name='add_pin'),  
]
