from django.shortcuts import render, redirect

def order_requried():
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if not 'order_id' in request.COOKIES:
                return redirect('home')
            return func(request, *args, **kwargs)
        return wrapper
    return decorator