from django.core.exceptions import PermissionDenied


class DailyPostLimitExceeded(PermissionDenied):
    pass
