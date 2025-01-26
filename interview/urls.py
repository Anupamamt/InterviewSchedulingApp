from django.urls import path
from django.conf import settings
from .views import AddUser,GetUsers,AddAvailableTime,GetAvailableTime
urlpatterns = [
    path('add-user/', AddUser.as_view(), name='add_user'),
    path('get-users/', GetUsers.as_view(), name='get_users'),
    path('add-time-slot/<int:id>/', AddAvailableTime.as_view(), name='add_time_slot'),
    path('get-time-slots/', GetAvailableTime.as_view(), name='get_time_slots'),

]