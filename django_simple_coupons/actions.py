from django.contrib.admin import ModelAdmin
from django.utils import timezone

from django_simple_coupons.models import CouponUser


def reset_coupon_usage(modeladmin, request, queryset):
    to_update = []
    for coupon_user in queryset:
        if coupon_user.times_used > 0:
            coupon_user.times_used = 0
            to_update.append(coupon_user)

    CouponUser.objects.bulk_update(to_update, fields=['times_used'], batch_size=500)

    ModelAdmin.message_user(modeladmin, request, "Coupons reseted!")


def delete_expired_coupons(modeladmin, request, queryset):
    count = 0
    queryset = queryset.exclude(ruleset__validity__is_permanent=True)
    for coupon in queryset:
        expiration_date = coupon.ruleset.validity.expiration_date
        if timezone.now() >= expiration_date:
            coupon.delete()
            count += 1

    ModelAdmin.message_user(modeladmin, request, f"{count} Expired coupons deleted!")


# Actions short descriptions
# ==========================
reset_coupon_usage.short_description = "Reset coupon usage"
delete_expired_coupons.short_description = "Delete expired coupons"
