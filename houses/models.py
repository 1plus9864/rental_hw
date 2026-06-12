from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('renter', '租客'),
        ('landlord', '房東'),
        ('admin', '管理員'),
    ]

    id = models.AutoField(primary_key=True, db_column='profile_id')
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user_id')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='renter', db_column='role')
    phone = models.CharField(max_length=20, blank=True, db_column='phone')
    bio = models.TextField(blank=True, db_column='bio')

    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'

    class Meta:
        db_table = 'USER_PROFILE'
        managed = False


class House(models.Model):
    id = models.AutoField(primary_key=True, db_column='house_id')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='上架人', db_column='landlord_id')
    title = models.CharField(max_length=100, db_column='title')

    location = models.ForeignKey(
        'Location',
        on_delete=models.PROTECT,
        db_column='location_id',
        related_name='houses'
    )

    price = models.IntegerField(db_column='rent')

    house_type = models.ForeignKey(
        'HouseType',
        on_delete=models.PROTECT,
        db_column='type_id',
        related_name='houses'
    )

    address = models.CharField(max_length=255, db_column='address')
    size = models.FloatField(db_column='size_sqft')
    description = models.TextField(blank=True, db_column='description')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'HOUSE'
        managed = False

class HouseType(models.Model):
    type_id = models.AutoField(primary_key=True, db_column='type_id')
    type_name = models.CharField(max_length=100, db_column='type_name')

    def __str__(self):
        return self.type_name

    class Meta:
        db_table = 'HOUSE_TYPE'
        managed = False


class Location(models.Model):
    location_id = models.AutoField(primary_key=True, db_column='location_id')
    city = models.CharField(max_length=100, db_column='city')
    district = models.CharField(max_length=100, db_column='district')
    postal_code = models.CharField(max_length=20, blank=True, null=True, db_column='postal_code')

    def __str__(self):
        return f'{self.city} {self.district}'

    class Meta:
        db_table = 'LOCATION'
        managed = False


class HouseImage(models.Model):
    image_id = models.AutoField(primary_key=True, db_column='image_id')
    house = models.ForeignKey(House, on_delete=models.CASCADE, db_column='house_id', related_name='images')
    image_url = models.CharField(max_length=500, db_column='image_url')
    display_order = models.IntegerField(db_column='display_order', default=1)

    class Meta:
        db_table = 'HOUSE_IMAGE'
        managed = False


class LegacyHouse(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    title = models.CharField(max_length=100, db_column='title')
    location = models.CharField(max_length=100, db_column='location')
    price = models.IntegerField(db_column='price')
    room_type = models.CharField(max_length=50, blank=True, db_column='room_type')
    size = models.FloatField(db_column='size')
    description = models.TextField(blank=True, db_column='description')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, db_column='owner_id')
    image = models.CharField(max_length=200, blank=True, null=True, db_column='image')

    class Meta:
        db_table = 'houses_house'
        managed = False


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(LegacyHouse, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} 收藏 {self.house.title}'


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', '待確認'),
        ('approved', '已同意'),
        ('rejected', '已拒絕'),
    ]

    id = models.AutoField(primary_key=True, db_column='appt_id')

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='renter_id'
    )

    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
        db_column='house_id'
    )

    appointment_date = models.DateField(db_column='appt_date')

    phone = models.CharField(max_length=20, db_column='phone')

    message = models.TextField(
        blank=True,
        db_column='note'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_column='appt_status'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_column='created_at'
    )

    def __str__(self):
        return f'{self.user.username} 預約 {self.house.title}'

    class Meta:
        db_table = 'APPOINTMENT'
        managed = False