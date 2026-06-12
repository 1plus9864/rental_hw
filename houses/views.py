from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import House, LegacyHouse
from .forms import HouseForm
from .models import Favorite
from django.contrib.auth.decorators import login_required
from .models import Appointment
from .forms import AppointmentForm
from .models import House, Location

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
    # Favorite model currently points to LegacyHouse. Try to find a legacy mapping first.
    legacy = None
    try:
        legacy = LegacyHouse.objects.get(id=house_id)
    except LegacyHouse.DoesNotExist:
        # fallback: try matching by title
        try:
            house_obj = House.objects.get(id=house_id)
            legacy = LegacyHouse.objects.filter(title=house_obj.title).first()
        except House.DoesNotExist:
            legacy = None

    if legacy is None:
        # cannot favorite this house because no legacy mapping exists; no-op
        return redirect(request.META.get('HTTP_REFERER', 'house_list'))

    favorite = Favorite.objects.filter(
        user=request.user,
        house=legacy
    )

    if favorite.exists():
        favorite.delete()
    else:
        Favorite.objects.create(
            user=request.user,
            house=legacy
        )

    return redirect(request.META.get('HTTP_REFERER', 'house_list'))

def house_list(request):
    houses = House.objects.select_related('house_type', 'location').prefetch_related('images').all()

    keyword = request.GET.get('keyword')
    room_type = request.GET.get('room_type')
    max_price = request.GET.get('max_price')

    if keyword:
        houses = houses.filter(title__icontains=keyword) | houses.filter(location__city__icontains=keyword) | houses.filter(location__district__icontains=keyword)

    if room_type:
        houses = houses.filter(house_type__type_name=room_type)

    if max_price:
        houses = houses.filter(price__lte=max_price)

    favorite_house_ids = []

    if request.user.is_authenticated:
        # Map legacy favorite house ids to current HOUSE ids when possible
        favs = Favorite.objects.filter(user=request.user).select_related('house')
        mapped = []
        for f in favs:
            legacy_id = getattr(f.house, 'id', None)
            if legacy_id is None:
                continue
            # try find formal House with same id
            try:
                formal = House.objects.get(id=legacy_id)
                mapped.append(formal.id)
                continue
            except House.DoesNotExist:
                pass
            # fallback: try match by title
            try:
                title = f.house.title
                formal = House.objects.filter(title=title).first()
                if formal:
                    mapped.append(formal.id)
            except Exception:
                pass

        favorite_house_ids = mapped

    return render(request, 'houses/house_list.html', {
        'houses': houses,
        'favorite_house_ids': favorite_house_ids,
    })
@login_required
def house_create(request):

    if request.user.userprofile.role not in ['landlord', 'admin']:
        return redirect('house_list')

    if request.method == 'POST':
        form = HouseForm(request.POST, request.FILES)

        if form.is_valid():
            house = form.save(commit=False)
            house.owner = request.user

            house.location = Location.objects.first()

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
    house = get_object_or_404(House.objects.select_related('house_type', 'location').prefetch_related('images'), pk=pk)
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

            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'role': form.cleaned_data['role']
                }
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

    houses = House.objects.select_related('house_type', 'location').prefetch_related('images').all()

    keyword = request.GET.get('keyword')
    room_type = request.GET.get('room_type')
    max_price = request.GET.get('max_price')
    favorite_house_ids = []

    if request.user.is_authenticated:
        favs = Favorite.objects.filter(user=request.user).select_related('house')
        mapped = []
        for f in favs:
            legacy_id = getattr(f.house, 'id', None)
            if legacy_id is None:
                continue
            try:
                formal = House.objects.get(id=legacy_id)
                mapped.append(formal.id)
                continue
            except House.DoesNotExist:
                pass
            try:
                title = f.house.title
                formal = House.objects.filter(title=title).first()
                if formal:
                    mapped.append(formal.id)
            except Exception:
                pass

        favorite_house_ids = mapped

    if keyword:
        houses = houses.filter(title__icontains=keyword) | houses.filter(location__city__icontains=keyword) | houses.filter(location__district__icontains=keyword)

    if room_type:
        houses = houses.filter(house_type__type_name=room_type)

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
        houses = House.objects.select_related('house_type', 'location').prefetch_related('images').all()
    else:
        houses = House.objects.select_related('house_type', 'location').prefetch_related('images').filter(
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
        form = HouseForm(instance=house)

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