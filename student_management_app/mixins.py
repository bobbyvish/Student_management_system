from .models import CustomUser
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied

class AdminRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.user_type != CustomUser.HOD:
            raise PermissionDenied("Only Admin can access this")
        return super(AdminRequiredMixin, self).dispatch(request, *args, **kwargs)
        

class StaffRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.user_type != CustomUser.STAFF:
            raise PermissionDenied("Only Admin can access this")
