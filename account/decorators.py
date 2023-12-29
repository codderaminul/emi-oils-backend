from django.shortcuts import redirect

def verified_email_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('tbm:index')  # Redirect to home if email is verified
            else:
                return redirect('accounts:VerifyOTP')  # Redirect to VerifyOTP if email is not verified
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def if_email_verified(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('tbm:index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def verified_email(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff is False:
                return redirect('accounts:VerifyOTP')
        return view_func(request, *args, **kwargs)
    return _wrapped_view