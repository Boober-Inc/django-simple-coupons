from django.db import models
from django.db.models import F

from django_simple_coupons.helpers import get_coupon_code_length
from django_simple_coupons.helpers import get_random_code
from django_simple_coupons.helpers import get_user_model


class Ruleset(models.Model):
    allowed_users = models.ForeignKey('AllowedUsersRule', on_delete=models.CASCADE, verbose_name="Allowed users rule")
    max_uses = models.ForeignKey('MaxUsesRule', on_delete=models.CASCADE, verbose_name="Max uses rule")
    validity = models.ForeignKey('ValidityRule', on_delete=models.CASCADE, verbose_name="Validity rule")

    def __str__(self):
        return (
            f"Ruleset Nº{self.pk}, allowed users rule {self.allowed_users}, "
            f"max user rule {self.max_uses}, validity rule {self.validity}"
        )

    class Meta:
        verbose_name = "Ruleset"
        verbose_name_plural = "Rulesets"


class AllowedUsersRule(models.Model):
    user_model = get_user_model()

    users = models.ManyToManyField(user_model, verbose_name="Users", blank=True)
    all_users = models.BooleanField(default=False, verbose_name="All users?")

    def __str__(self):
        return f"AllowedUsersRule Nº{self.pk}, all_users: {self.all_users}"

    class Meta:
        verbose_name = "Allowed User Rule"
        verbose_name_plural = "Allowed User Rules"


class MaxUsesRule(models.Model):
    max_uses = models.BigIntegerField(default=0, verbose_name="Maximum uses")
    is_infinite = models.BooleanField(default=False, verbose_name="Infinite uses?")
    uses_per_user = models.IntegerField(default=1, verbose_name="Uses per user")

    def __str__(self):
        return (
            f"MaxUsesRule Nº{self.pk}, uses {self.max_uses}, "
            f"infinite {self.is_infinite}, uses per user {self.uses_per_user}"
        )

    class Meta:
        verbose_name = "Max Uses Rule"
        verbose_name_plural = "Max Uses Rules"


class ValidityRule(models.Model):
    expiration_date = models.DateTimeField(verbose_name="Expiration date")
    is_active = models.BooleanField(default=False, verbose_name="Is active?")

    def __str__(self):
        return f"ValidityRule Nº{self.pk}, is_active: {self.is_active}, expires: {self.expiration_date}"

    class Meta:
        verbose_name = "Validity Rule"
        verbose_name_plural = "Validity Rules"


class CouponUser(models.Model):
    user_model = get_user_model()

    user = models.ForeignKey(user_model, on_delete=models.CASCADE, verbose_name="User")
    coupon = models.ForeignKey('Coupon', on_delete=models.CASCADE, verbose_name="Coupon")
    times_used = models.IntegerField(default=0, editable=False, verbose_name="Times used")

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Coupon User"
        verbose_name_plural = "Coupon Users"


class Discount(models.Model):
    value = models.IntegerField(default=0, verbose_name="Value")
    is_percentage = models.BooleanField(default=False, verbose_name="Is percentage?")

    def __str__(self):
        if self.is_percentage:
            return f"{self.value}% - Discount"

        return f"${self.value} - Discount"

    class Meta:
        verbose_name = "Discount"
        verbose_name_plural = "Discounts"


class Coupon(models.Model):
    code = models.CharField(max_length=100, default=get_random_code, verbose_name="Coupon Code", unique=True)
    discount = models.ForeignKey('Discount', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True, default='')
    times_used = models.IntegerField(default=0, editable=False, verbose_name="Times used")
    created = models.DateTimeField(editable=False, verbose_name="Created", auto_now_add=True)

    ruleset = models.ForeignKey('Ruleset', on_delete=models.CASCADE, verbose_name="Ruleset")

    def __str__(self):
        return self.code

    def use_coupon(self, user):
        coupon_user, _ = CouponUser.objects.get_or_create(user=user, coupon=self)
        coupon_user.times_used = F('times_used') + 1
        coupon_user.save()

        self.times_used = F('times_user') + 1
        self.save()

    def get_discount(self):
        return {
            "value": self.discount.value,
            "is_percentage": self.discount.is_percentage
        }

    def get_discounted_value(self, initial_value):
        discount = self.get_discount()

        if discount['is_percentage']:
            new_price = initial_value - (initial_value * discount['value']) / 100
        else:
            new_price = initial_value - discount['value']

        return max(new_price, 0.0)
