from django import forms
from django.contrib.auth.models import User

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(render_value=False),  # Hide password field
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:  # Only validate if a new password is provided
            # Add password validation logic if needed
            if len(password) < 6:
                raise forms.ValidationError("Password must be at least 6 characters.")
        return password
