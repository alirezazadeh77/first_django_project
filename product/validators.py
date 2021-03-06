from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


class PhoneNumberValidator(RegexValidator):
    regex = '^9[0-3,9]\d{8}$'
    message = _("Phone number is not a valid 9XXXXXXXXX")
    code = 'invalid phone number'


clean_phone_number_validator = PhoneNumberValidator()
