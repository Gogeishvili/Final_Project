from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import (
    validate_password as django_validate_password,
)
from rest_framework.exceptions import ValidationError


def validate_positive_amount(amount):

    if amount <= 0:
        raise ValidationError("Amount must be greater than zero.")


def validate_enogh_amount(current_money, amount):
    if current_money < amount:
        raise ValidationError("You don't have enough money.")


def validate_string_match(password, password2):
    if password != password2:
        raise ValidationError("Passwords do not match!")


def validate_password_strength(password):
    try:
        django_validate_password(password)
    except ValidationError as e:
        raise ValidationError({"password": e.messages})
