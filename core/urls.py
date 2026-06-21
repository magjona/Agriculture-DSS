from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-farm/', views.add_farm, name='add_farm'),
    path('recommend/<int:farm_id>/', views.generate_recommendation, name='generate_recommendation'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.custom_login, name='login'),
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('chat/', views.chat_index, name='chat_index'),
    path('chat/<int:session_id>/', views.chat_session_view, name='chat_session'),
    path('chat/new/', views.create_chat_session, name='create_chat_session'),
    path('chat/delete/<int:session_id>/', views.delete_chat_session, name='delete_chat_session'),
    path('crop/add/', views.edit_crop, name='add_crop'),
    path('crop/edit/<int:crop_id>/', views.edit_crop, name='edit_crop'),
    path('crop/delete/<int:crop_id>/', views.delete_crop, name='admin_delete_crop'),
    path('farm/add/', views.edit_farm, name='admin_add_farm'),
    path('farm/edit/<int:farm_id>/', views.edit_farm, name='admin_edit_farm'),
    path('farm/delete/<int:farm_id>/', views.delete_farm, name='admin_delete_farm'),
    path('recommendation/add/', views.edit_recommendation, name='admin_add_recommendation'),
    path('recommendation/edit/<int:rec_id>/', views.edit_recommendation, name='admin_edit_recommendation'),
    path('recommendation/delete/<int:rec_id>/', views.delete_recommendation, name='admin_delete_recommendation'),
    path('recommendation/delete/my/<int:rec_id>/', views.delete_my_recommendation, name='delete_my_recommendation'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
