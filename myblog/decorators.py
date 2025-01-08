from functools import wraps
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Datas

def user_is_post_creator(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        datas_emailid = kwargs.get('emailid')
        data = get_object_or_404(Datas, emailid=datas_emailid)
        if data.created_by != request.user:
            messages.error(request, "You do not have permission to perform this action.")
            return redirect('view')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
