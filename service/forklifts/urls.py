from django.urls import path
from .views import home, login_view,  technical_service_detail, complaint_detail, forklift_detail, edit_forklift,delete_complaint,add_technical_service,delete_technical_service,add_complaint, delete_forklift, add_forklift, logout_view, search_forklift, forklift_list, technical_service_list, complaint_list
from django.shortcuts import render
urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),  # Страница авторизации
    path('logout/', logout_view, name='logout'),
    path('search/', search_forklift, name='search_forklift'),
    path('forklifts/', forklift_list, name='forklift_list'),  # Список погрузчиков
    path('forklifts/<int:id>/', forklift_detail, name='forklift_detail'),
    path('complaints/<int:id>/', complaint_detail, name='complaint_detail'),  # Для деталей рекламации
    path('technical_services/<int:id>/', technical_service_detail, name='technical_service_detail'),
    path('forklifts/<int:forklift_id>/technical-services/add/', add_technical_service, name='add_technical_service'),  # Добавление ТО
    path('technical-service/delete/<int:service_id>/', delete_technical_service, name='delete_technical_service'),  # Удаление ТО
    path('forklifts/<int:forklift_id>/complaints/add/', add_complaint, name='add_complaint'),  # Добавление рекламации
    path('complaint/delete/<int:complaint_id>/', delete_complaint, name='delete_complaint'),  # Удал
    path('forklifts/<int:forklift_id>/technical-services/', technical_service_list, name='technical_service_list'),  # Список ТО для погрузчика
    path('forklifts/<int:forklift_id>/complaints/', complaint_list, name='complaint_list'),  # Список рекламаций для погрузчика
    path('forklifts/delete/<int:forklift_id>/', delete_forklift, name='delete_forklift'),  # Удаление погрузчика
    path('forklifts/edit/<int:forklift_id>/', edit_forklift, name='edit_forklift'),  # Изменение погрузчика
    path('forklifts/add/', add_forklift, name='add_forklift'),  # Добавление погрузчика
    path('technical-services/', technical_service_list, name='technical_service_list'),  # Список ТО
    path('complaints/', complaint_list, name='complaint_list'),  # Список рекламаций
]
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

handler404 = custom_404_view