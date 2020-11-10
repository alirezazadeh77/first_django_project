from rest_framework.throttling import ScopedRateThrottle


class PhoneNumberScopedReateTrottle(ScopedRateThrottle):
    def get_cache_key(self, request, view):
        if self.scope == "register":
            if 'Phone_number' in request.data:
                self.num_requests, self.duration = self.parse_rate("5/minute")
            else:
                self.num_requests, self.duration = self.parse_rate("7/minute")

        if 'Phone_number' in request.data:
            return self.cache_format % {
                'scope': self.scope,
                'ident': request.data['Phone_number']
            }

        return super().get_cache_key(request, view)

    def throttle_success(self):
        """
        Inserts the current request's timestamp along with the key
        into the cache.
        """
        self.history.insert(0, self.now)
        if len(self.history) + 1 >= self.num_requests:
            self.cache.set(self.key, self.history, self.wait_time)
        else:
            self.cache.set(self.key, self.history, self.duration)
        return True

    def wait(self):
        """
        Returns the recommended next request time in seconds.
        """
        if self.history:
            remaining_duration = self.wait_time - (self.now - self.history[-1])
        else:
            remaining_duration = self.wait_time

        available_requests = self.num_requests - len(self.history) + 1
        if available_requests <= 0:
            return None

        return remaining_duration / float(available_requests)

    def parse_rate(self, rate,):
        """
        Given the request rate string, return a two tuple of:
        <allowed number of requests>, <period of time in seconds>
        """
        if rate is None:
            return (None, None)
        try:
            num, period, wait_time = rate.split('/')
            self.wait_time = int(wait_time)
            duration = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[period[0]]
        except ValueError:
            num, period = rate.split('/')
            duration = self.wait_time = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[period[0]]
        num_requests = int(num)
        return (num_requests, duration)
