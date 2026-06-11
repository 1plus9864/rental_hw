from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import House
from .forms import HouseForm
from .models import Favorite
from django.contrib.auth.decorators import login_required
from .models import Appointment
from .forms import AppointmentForm

@login_required
def my_favorites(request):

    if request.user.userprofile.role not in ['renter', 'admin']:
        return redirect('house_list')

    favorites = Favorite.objects.filter(
        user=request.user
    )

    return render(request, 'houses/my_favorites.html', {
        'favorites': favorites
    })

@login_required
def toggle_favorite(request, house_id):

    house = House.objects.get(id=house_id)

    favorite = Favorite.objects.filter(
        user=request.user,
        house=house
    )

    if favorite.exists():
        favorite.delete()
    else:
        Favorite.objects.create(
            user=request.user,
            house=house
        )

    return redirect(request.META.get('HTTP_REFERER', 'house_list'))

def house_list(request):
    houses = House.objects.all()

    keyword = request.GET.get('keyword')
    room_type = request.GET.get('room_type')
    max_price = request.GET.get('max_price')

    if keyword:
        houses = houses.filter(location__icontains=keyword) | houses.filter(title__icontains=keyword)

    if room_type:
        houses = houses.filter(room_type=room_type)

    if max_price:
        houses = houses.filter(price__lte=max_price)

    favorite_house_ids = []

    if request.user.is_authenticated:
        favorite_house_ids = Favorite.objects.filter(
            user=request.user
        ).values_list('house_id', flat=True)

    return render(request, 'houses/house_list.html', {
        'houses': houses,
        'favorite_house_ids': favorite_house_ids,
    })
@login_required
def house_create(request):

    if request.user.userprofile.role not in ['landlord', 'admin']:
        return redirect('house_list')

    if request.method == 'POST':

        form = HouseForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            house = form.save(commit=False)

            house.owner = request.user

            house.save()

            return redirect('house_list')

    else:

        form = HouseForm()

    return render(
        request,
        'houses/house_form.html',
        {'form': form}
    )

def house_detail(request, pk):
    house = get_object_or_404(House, pk=pk)
    return render(request, 'houses/house_detail.html', {'house': house})


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .forms import RegisterForm
from .models import UserProfile
def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            UserProfile.objects.create(
                user=user,
                role=form.cleaned_data['role']
            )

            login(request, user)

            return redirect('house_list')

    else:
        form = RegisterForm()

    return render(
        request,
        'registration/register.html',
        {'form': form}
    )
def house_search(request):

    houses = House.objects.all()

    keyword = request.GET.get('keyword')
    room_type = request.GET.get('room_type')
    max_price = request.GET.get('max_price')
    favorite_house_ids = []

    if request.user.is_authenticated:
        favorite_house_ids = Favorite.objects.filter(
            user=request.user
        ).values_list('house_id', flat=True)

    if keyword:
        houses = houses.filter(
            title__icontains=keyword
        ) | houses.filter(
            location__icontains=keyword
        )

    if room_type:
        houses = houses.filter(
            room_type=room_type
        )

    if max_price:
        houses = houses.filter(
            price__lte=max_price
        )

    return render(request, 'houses/search_results.html', {
        'houses': houses,
        'favorite_house_ids': favorite_house_ids,
    })
@login_required
def create_appointment(request, house_id):

    if request.user.userprofile.role not in ['renter', 'admin']:
        return redirect('house_list')

    house = House.objects.get(id=house_id)

    if request.method == 'POST':

        form = AppointmentForm(request.POST)

        if form.is_valid():

            appointment = form.save(commit=False)

            appointment.user = request.user
            appointment.house = house

            appointment.save()

            return redirect('my_appointments')

    else:

        form = AppointmentForm()

    return render(
        request,
        'houses/appointment_form.html',
        {
            'form': form,
            'house': house
        }
    )
@login_required
def my_appointments(request):

    appointments = Appointment.objects.filter(
        user=request.user
    )

    return render(
        request,
        'houses/my_appointments.html',
        {
            'appointments': appointments
        }
    )
@login_required
def landlord_appointments(request):

    if request.user.userprofile.role not in  ['landlord', 'admin']:
        return redirect('house_list')

    appointments = Appointment.objects.filter(
        house__owner=request.user
    ).order_by('-created_at')

    return render(
        request,
        'houses/landlord_appointments.html',
        {
            'appointments': appointments
        }
    )
@login_required
def my_houses(request):

    if request.user.userprofile.role not in ['landlord', 'admin']:
        return redirect('house_list')

    if request.user.userprofile.role == 'admin':
        houses = House.objects.all()
    else:
        houses = House.objects.filter(
            owner=request.user
        )

    return render(
        request,
        'houses/my_houses.html',
        {
            'houses': houses
        }
    )
@login_required
def house_update(request, pk):

    house = House.objects.get(id=pk)

    if (
        house.owner != request.user
        and request.user.userprofile.role != 'admin'
    ):
        return redirect('house_list')

    if request.method == 'POST':

        form = HouseForm(
            request.POST,
            request.FILES,
            instance=house
        )

        if form.is_valid():
            form.save()
            return redirect('my_houses')

    else:
        form = HouseForm(request.POST, request.FILES, instance=house)

    return render(
        request,
        'houses/house_form.html',
        {
            'form': form
        }
    )
@login_required
def house_delete(request, pk):

    house = House.objects.get(id=pk)

    if (
        house.owner != request.user
        and request.user.userprofile.role != 'admin'
    ):
        return redirect('house_list')

    if request.method == 'POST':
        house.delete()
        return redirect('my_houses')

    return render(
        request,
        'houses/house_confirm_delete.html',
        {
            'house': house
        }
    )