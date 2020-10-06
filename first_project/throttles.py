from rest_framework.throttling import ScopedRateThrottle


class PhoneNumberScopedReateTrottle(ScopedRateThrottle):
    def get_cache_key(self, request, view):
        if 'Phone_Number' in request.data:
            return self.cache_format % {
                'scope': self.scope,
                'ident': request.data['Phone_number']
            }
        return super().get_cache_key(request, view)
