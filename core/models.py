import re
import hashlib
import bcrypt

from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from rut_chile import rut_chile

# Create your models here.

CATEGORY_CHOICES = (
    ('A', 'Arboles'),
    ('AR', 'Arbustos'),
    ('M', 'Macetas'),
    ('S', 'Semillas'),
    ('H', 'Herramientas'),
)

LABEL_CHOICES = (
    ('S', 'success'),
    ('D', 'danger'),
    ('W', 'warning')
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField(validators=[MinValueValidator(1)])
    discount_price = models.FloatField(blank=True, null=True,validators=[MinValueValidator(1)])
    on_sale = models.BooleanField(default=False)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=2, blank=True, null=True)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(default='default.png', upload_to='productos')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:core-product", kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse("core:core-add-to-cart", kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse("core:core-remove-from-cart", kwargs={'slug': self.slug})

    def get_discount_pencentaje(self):
        return int(((self.price - self.discount_price) / self.price) * 100)

    def get_update_url(self):
        return reverse("staff:staff-product-update", kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse("staff:staff-product-delete", kwargs={'pk': self.pk})

    @property
    def display_price(self):
        if self.on_sale and self.discount_price:
            return self.discount_price
        return self.price

    def save(self, *args, **kwargs):
        if self.on_sale:
                self.label = 'D'
        elif self.on_sale == False and self.label == 'D':
                self.label = None

        super().save(*args, **kwargs)



ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        if self.user:
            return self.user.username
        else:
            return 'No username available'





class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        if self.item.on_sale:
            return self.quantity * self.item.discount_price
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return (self.quantity * self.item.price) - self.get_total_discount_item_price()


    def get_final_price(self):
        if self.item.on_sale:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()




class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)


    @property
    def reference_number(self):
        return f"ORDEN-{self.pk}"

    def __str__(self):
        if self.user:
            return self.user.username
        else:
            return 'No username available'

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        if total < 0:
            total = 0
        return total

    def get_no_coupon_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    def get_total_number_of_items(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.quantity
        return total


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return self.user.username
        else:
            return 'No username available'


class Coupon(models.Model):
    code = models.CharField(max_length=15, unique=True)
    amount = models.FloatField(validators=[MinValueValidator(1)])
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    def get_update_url(self):
        return reverse("staff:staff-coupon-update", kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse("staff:staff-coupon-delete", kwargs={'pk': self.pk})


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)




class Donacion(models.Model):
    nombre = models.CharField(max_length=100, blank=False)
    apellido = models.CharField(max_length=100, blank=False)
    correo = models.EmailField(blank=False)
    monto = models.IntegerField(blank=False, validators=[MinValueValidator(1)])
    codigo_pais = models.CharField(max_length=100, blank=False, default="+56")
    telefono = models.IntegerField(blank=False, validators=[MinValueValidator(100000000), MaxValueValidator(999999999)])
    rut = models.CharField(max_length=12, blank=False)
    rut_cifrado = models.CharField(max_length=64, blank=False)
    rut_bcrypt = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'



    def save(self, *args, **kwargs):
        if self.rut and not self.rut_cifrado:
            self.rut_cifrado = hashlib.sha256(self.rut.encode()).hexdigest()
        if self.rut and not self.rut_bcrypt:
            self.rut_bcrypt = bcrypt.hashpw(self.rut.encode(), bcrypt.gensalt()).decode()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if not rut_chile.is_valid_rut(self.rut):
            raise ValidationError('Ingrese un RUT válido.')
        self.rut = re.sub(r'[\.\-]', '', self.rut)



from django_extensions.db.models import (
	TimeStampedModel,
)

class OnePieceCapituloManga(TimeStampedModel,models.Model):
    capitulo = models.IntegerField()
    volumen = models.IntegerField()
    titulo = models.CharField(max_length=255)
    titulo_romanizado = models.CharField(max_length=255)
    titulo_viz = models.CharField(max_length=255)
    paginas = models.IntegerField()
    fecha_publicacion = models.DateField()
    episodios = models.CharField(max_length=100)
