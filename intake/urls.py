from django.urls import path
from . import views

urlpatterns = [
    path('intake/add/', views.add_intake_view, name='add_intake'),
    path('intake/', views.intake_list_view, name='intake_list'),
    path('intake/<int:intake_id>/edit/', views.edit_intake_view, name='edit_intake'),
    path('intake/<int:intake_id>/delete/', views.delete_intake_view, name='delete_intake'),

    path('history/', views.intake_history_view, name='intake_history'),
    path('history/<str:intake_date>/', views.intake_history_detail_view, name='intake_history_detail'),
]