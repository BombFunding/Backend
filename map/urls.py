
from django.urls import path
from map.views import PinListView, PinCreateView,PinDeleteView,user_details,ProvincePinCountView

urlpatterns = [
    path('pins/', PinListView.as_view(), name='list_pins'),  
    path('pins/add/', PinCreateView.as_view(), name='add_pin'),  
    path('pins/delete/', PinDeleteView.as_view(), name='delete_pins'),
    path('user/details/', user_details, name='user-details'),
    path('pins/province-count/', ProvincePinCountView.as_view(), name='province-pin-count'),
]
