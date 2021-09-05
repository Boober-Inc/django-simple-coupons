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
from django_simple_coupons.models import MinPriceRule


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'ruleset', 'times_used', 'created',)
    search_fields = ('code', )

    actions = [delete_expired_coupons]


@admin.register(Ruleset)
class RulesetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'allowed_users', 'max_uses', 'validity',)


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
    pass


admin.site.register(Discount)
admin.site.register(MaxUsesRule)
admin.site.register(ValidityRule)
admin.site.register(MinPriceRule)
