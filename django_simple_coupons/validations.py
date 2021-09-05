from django.utils import timezone

from django_simple_coupons.models import Coupon
from django_simple_coupons.models import CouponUser

INVALID_TEMPLATE = {
    "valid": False,
    "message": ""
}

VALID_TEMPLATE = {
    "valid": True
}


def assemble_invalid_message(message=""):
    response = INVALID_TEMPLATE
    response['message'] = message
    return response


def validate_allowed_users_rule(coupon_object, user):
    allowed_users_rule = coupon_object.ruleset.allowed_users
    if allowed_users_rule.all_users:
        return True

    return user in allowed_users_rule.users.all()


def validate_max_uses_rule(coupon_object, user):
    max_uses_rule = coupon_object.ruleset.max_uses
    if coupon_object.times_used >= max_uses_rule.max_uses and not max_uses_rule.is_infinite:
        return False

    try:
        coupon_user = CouponUser.objects.get(user=user, coupon=coupon_object)
        if coupon_user.times_used >= max_uses_rule.uses_per_user:
            return False
    except CouponUser.DoesNotExist:
        pass

    return True


def validate_validity_rule(coupon_object):
    validity_rule = coupon_object.ruleset.validity
    if not validity_rule.is_permanent:
        if validity_rule.expiration_date and timezone.now() < validity_rule.expiration_date:
            return validity_rule.is_active

        return False

    return validity_rule.is_active


def validate_min_price_rule(coupon_object, initial_value):
    min_price_rule = coupon_object.ruleset.min_price
    if initial_value <= min_price_rule.min_price:
        return False

    return True


def validate_coupon(coupon_code, user, initial_value):
    if not coupon_code:
        return assemble_invalid_message(message="No coupon code provided!")

    if not user:
        return assemble_invalid_message(message="No user provided!")

    try:
        coupon_object = Coupon.objects.get(code__iexact=coupon_code)
    except Coupon.DoesNotExist:
        return assemble_invalid_message(message="Hmm, that's not one of our codes. Please try again!")

    valid_allowed_users_rule = validate_allowed_users_rule(coupon_object=coupon_object, user=user)
    if not valid_allowed_users_rule:
        return assemble_invalid_message(message="This Promo Code has already been used")

    valid_max_uses_rule = validate_max_uses_rule(coupon_object=coupon_object, user=user)
    if not valid_max_uses_rule:
        return assemble_invalid_message(message="This Promo Code has already been used")

    valid_validity_rule = validate_validity_rule(coupon_object=coupon_object)
    if not valid_validity_rule:
        return assemble_invalid_message(message="This Promo Code is no longer valid")

    valid_min_price_rule = validate_min_price_rule(coupon_object=coupon_object, initial_value=initial_value)
    if not valid_min_price_rule:
        return assemble_invalid_message(message="You must spend more than ${} to use this code".format(
            coupon_object.ruleset.min_price.min_price))

    return VALID_TEMPLATE
