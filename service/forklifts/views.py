from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied# Импортируйте нужные модели
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Forklift, TechnicalService, Complaint
from forklifts.forms import ForkliftForm
from django.contrib import messages
from .forms import TechnicalServiceForm, ComplaintForm  # Импортируйте соответствующие формы

from django.shortcuts import render


def home(request):
    user_can_view_forklift = request.user.is_authenticated and request.user.is_staff  # Проверяем, является ли пользователь авторизованным и менеджером
    user_can_add_forklift = request.user.is_authenticated and request.user.is_staff   # Проверяем, является ли пользователь авторизованным и менеджером

    return render(request, 'home.html', {
        'user_can_view_forklift': user_can_view_forklift,
        'user_can_add_forklift': user_can_add_forklift,
        'user': request.user,
        # другие данные
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Перенаправление на главную страницу
        else:
            return render(request, 'login.html', {'error': 'Неверное имя пользователя или пароль'})

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')  # Перенаправление на главную страницу


@login_required
@permission_required('forklifts.add_technicalservice', raise_exception=True)
def add_technical_service(request):
    if request.method == 'POST':
        # Логика для обработки формы добавления ТО
        pass
    return render(request, 'add_technical_service.html')

@login_required
@permission_required('forklifts.add_complaint', raise_exception=True)
def add_complaint(request):
    if request.method == 'POST':
        # Логика для обработки формы добавления рекламации
        pass
    return render(request, 'add_complaint.html')



def search_forklift(request):
    forklift = None
    error_message = None

    if request.method == 'GET':
        serial_number = request.GET.get('serial_number')
        if serial_number:
            try:
                forklift = get_object_or_404(Forklift, serial_number=serial_number)

                # Если пользователь авторизован, показываем все данные
                if request.user.is_authenticated:
                    technical_services = TechnicalService.objects.filter(forklift=forklift)
                    complaints = Complaint.objects.filter(forklift=forklift)
                    return render(request, 'home.html', {
                        'forklift': forklift,
                        'technical_services': technical_services,
                        'complaints': complaints,
                        'error_message': error_message,
                        'can_add_complaint': is_manager(request.user) or is_service_organization(request.user),
                        'is_manager': is_manager(request.user)
                    })
                else:
                    # Если пользователь не авторизован, показываем только основные характеристики
                    return render(request, 'home.html', {
                        'forklift': forklift,
                        'error_message': error_message,
                        'can_add_complaint': False,
                        'is_manager': False
                    })

            except Forklift.DoesNotExist:
                error_message = "Погрузчик с указанным заводским номером не найден."

    return render(request, 'home.html', {
        'forklift': forklift,
        'error_message': error_message,
        'can_add_complaint': False,
        'is_manager': False
    })
def is_client(user):
    return user.groups.filter(name='Клиент').exists()

def is_service_organization(user):
    return user.groups.filter(name='Сервисная организация').exists()

def is_manager(user):
    return user.groups.filter(name='Менеджер').exists()

@login_required
def forklift_list(request):
    if is_client(request.user):
        # Если пользователь - клиент, показываем только его машины
        forklifts = Forklift.objects.filter(client=request.user)  # Предполагается, что у вас есть связь с клиентом
    elif is_service_organization(request.user):
        # Сервисная организация может только смотреть свои машины
        forklifts = Forklift.objects.filter(service_company=request.user)  # Предполагается, что у вас есть связь с сервисной компанией
    elif is_manager(request.user):
        # Менеджер может видеть и редактировать все машины
        forklifts = Forklift.objects.all()
    else:
        return render(request, 'access_denied.html')  # Доступ запрещен для других пользователей

    return render(request, 'forklift_list.html', {'forklifts': forklifts})

@login_required
def technical_service_list(request, forklift_id):
    forklift = get_object_or_404(Forklift, id=forklift_id)

    if is_client(request.user):
        # Клиент может смотреть и вносить данные только для своих машин
        if forklift.client != request.user:
            return render(request, 'access_denied.html')  # Доступ запрещен для клиента
        technical_services = TechnicalService.objects.filter(forklift=forklift)  # Только записи клиента

    elif is_service_organization(request.user):
        # Сервисная организация может смотреть и добавлять данные только для своих машин
        if forklift.service_company != request.user:
            return render(request, 'access_denied.html')  # Доступ запрещен для сервисной компании
        technical_services = TechnicalService.objects.filter(forklift=forklift)  # Только записи сервисной организации

    elif is_manager(request.user):
        # Менеджер может видеть и редактировать все машины
        technical_services = TechnicalService.objects.filter(forklift=forklift)  # Все записи для конкретного погрузчика

    else:
        return render(request, 'access_denied.html')  # Доступ запрещен для других пользователей

    return render(request, 'technical_service_list.html', {'forklift': forklift, 'technical_services': technical_services})

@login_required
def complaint_list(request, forklift_id):
    forklift = get_object_or_404(Forklift, id=forklift_id)

    if is_client(request.user):
        # Клиент может видеть только свои рекламации
        if forklift.client != request.user:
            return render(request, 'access_denied.html')  # Доступ запрещен для клиента
        complaints = Complaint.objects.filter(forklift=forklift)  # Только рекламации клиента

    elif is_service_organization(request.user):
        # Сервисная организация может видеть и добавлять данные только для своих рекламаций
        if forklift.service_company != request.user:
            return render(request, 'access_denied.html')  # Доступ запрещен для сервисной компании
        complaints = Complaint.objects.filter(forklift=forklift)  # Только рекламации для данного погрузчика

    elif is_manager(request.user):
        # Менеджер может видеть и редактировать все рекламации
        complaints = Complaint.objects.filter(forklift=forklift)  # Все рекламации для данного погрузчика

    else:
        return render(request, 'access_denied.html')  # Доступ запрещен для других пользователей

    return render(request, 'complaint_list.html', {'forklift': forklift, 'complaints': complaints})
@login_required
@permission_required('forklifts.add_forklift', raise_exception=True)
def add_forklift(request):
    if request.method == 'POST':
        form = ForkliftForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Погрузчик успешно добавлен!")
            return redirect('forklift_list')
        else:
            messages.error(request, "Ошибка при добавлении погрузчика. Проверьте форму.")  # Сообщение об ошибке
            print(form.errors)  # Вывод ошибок в консоль для отладки
    else:
        form = ForkliftForm()
    return render(request, 'add_forklift.html', {'form': form})
@login_required
@permission_required('forklifts.view_forklift', raise_exception=True)
def forklift_list(request):
    forklifts = Forklift.objects.all()  # Получаем все погрузчики
    return render(request, 'forklift_list.html', {'forklifts': forklifts})

@login_required
@permission_required('forklifts.delete_forklift', raise_exception=True)
def delete_forklift(request, forklift_id):
    forklift = get_object_or_404(Forklift, id=forklift_id)
    forklift.delete()
    messages.success(request, "Погрузчик успешно удален.")
    return redirect('forklift_list')

@login_required
@permission_required('forklifts.change_forklift', raise_exception=True)
def edit_forklift(request, forklift_id):
    forklift = get_object_or_404(Forklift, id=forklift_id)
    if request.method == 'POST':
        form = ForkliftForm(request.POST, instance=forklift)
        if form.is_valid():
            form.save()
            messages.success(request, "Погрузчик успешно обновлен.")
            return redirect('forklift_list')
    else:
        form = ForkliftForm(instance=forklift)
    return render(request, 'edit_forklift.html', {'form': form})



@login_required
@permission_required('forklifts.view_technicalservice', raise_exception=True)
def technical_service_list(request, forklift_id):
    forklift = get_object_or_404(Forklift, id=forklift_id)
    technical_services = TechnicalService.objects.filter(forklift=forklift)
    return render(request, 'technical_service_list.html', {'forklift': forklift, 'technical_services': technical_services})

@login_required
@permission_required('forklifts.view_complaint', raise_exception=True)
def complaint_list(request, forklift_id):
    forklift = get_object_or_404(Forklift, id=forklift_id)
    complaints = Complaint.objects.filter(forklift=forklift)
    return render(request, 'complaint_list.html', {'forklift': forklift, 'complaints': complaints})
@login_required
@permission_required('forklifts.add_technicalservice', raise_exception=True)
def add_technical_service(request, forklift_id):
    forklift = get_object_or_404(Forklift, id=forklift_id)
    if request.method == 'POST':
        form = TechnicalServiceForm(request.POST)
        if form.is_valid():
            technical_service = form.save(commit=False)
            technical_service.forklift = forklift  # Привязываем к погрузчику
            technical_service.save()
            messages.success(request, "Техническое обслуживание успешно добавлено!")
            return redirect('technical_service_list', forklift_id=forklift.id)
    else:
        form = TechnicalServiceForm()
    return render(request, 'add_technical_service.html', {'form': form, 'forklift': forklift})

@login_required
@permission_required('forklifts.delete_technicalservice', raise_exception=True)
def delete_technical_service(request, service_id):
    technical_service = get_object_or_404(TechnicalService, id=service_id)
    technical_service.delete()
    messages.success(request, "Запись о техническом обслуживании успешно удалена.")
    return redirect('technical_service_list', forklift_id=technical_service.forklift.id)

@login_required
@permission_required('forklifts.add_complaint', raise_exception=True)
def add_complaint(request, forklift_id):
    forklift = get_object_or_404(Forklift, id=forklift_id)
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.forklift = forklift  # Привязываем к погрузчику
            complaint.save()
            messages.success(request, "Рекламация успешно добавлена!")
            return redirect('complaint_list', forklift_id=forklift.id)
    else:
        form = ComplaintForm()
    return render(request, 'add_complaint.html', {'form': form, 'forklift': forklift})

@login_required
@permission_required('forklifts.delete_complaint', raise_exception=True)
def delete_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    complaint.delete()
    messages.success(request, "Запись о рекламации успешно удалена.")
    return redirect('complaint_list', forklift_id=complaint.forklift.id)