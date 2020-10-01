from django.db.models import BigIntegerField


class CustomBigIntegerField(BigIntegerField):
    def get_prep_value(self, value):
        if value is None:
            return value
        try:
            return int(value)
        except ValueError:
            pass