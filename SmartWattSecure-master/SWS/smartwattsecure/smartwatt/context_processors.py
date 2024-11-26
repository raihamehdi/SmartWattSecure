from .forms import UserUpdateForm

def user_update_form(request):
    if request.user.is_authenticated:
        return {'update_form': UserUpdateForm(instance=request.user)}
    return {}