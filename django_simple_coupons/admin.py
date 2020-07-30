from django.contrib import admin

from django_simple_coupons.actions import delete_expired_coupons
from django_simple_coupons.actions import reset_coupon_usage
from django_simple_coupons.models import AllowedUsersRule
from django_simple_coupons.models import Coupon
from django_simple_coupons.models import CouponUser
from django_simple_coupons.models import Discount
from django_simple_coupons.models import MaxUsesRule
from django_simple_coupons.models import Ruleset
from django_simple_coupons.models import ValidityRule


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'ruleset', 'times_used', 'created',)
    actions = [delete_expired_coupons]


@admin.register(Ruleset)
class RulesetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'allowed_users', 'max_uses', 'validity',)
    raw_id_fields = (
        'allowed_users',
    )


@admin.register(CouponUser)
class CouponUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'coupon', 'times_used',)
    actions = [reset_coupon_usage]
    raw_id_fields = (
        'user',
        'coupon',
    )


@admin.register(AllowedUsersRule)
class AllowedUsersRuleAdmin(admin.ModelAdmin):
    raw_id_fields = (
        'users',
    )

    def get_model_perms(self, request):
        return {}


@admin.register(MaxUsesRule)
class MaxUsesRuleAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


@admin.register(ValidityRule)
class ValidityRuleAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


admin.site.register(Discount)
