from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('http://127.0.0.1:3000/')
        return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            check = False
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            for role in allowed_roles:
                if role == group:
                    check = True
            if check:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not Authorized')
        return wrapper_func
    return decorator
