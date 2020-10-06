from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError
from django.utils import timezone

from accounts.models import User, VerifyCode


class SMSBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        PhoneNumberField = User._meta.get_field('Phone_number')
        try:
            phone_number = kwargs.get('Phone_number')
            phone_number = int(phone_number)
            PhoneNumberField.run_validators(phone_number)
            verify_code = VerifyCode.objects.filter(
                verification_code=password,
                user__Phone_number=phone_number,
                verify_time__isnull=True,
                created_time__gt=timezone.now() - timezone.timedelta(hours=6),
            ).first()
            if verify_code:
                verify_code.verify_time = timezone.now()
                verify_code.save()
                return verify_code.user
        except (ValueError, ValidationError):
            pass
