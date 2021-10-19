from django.forms import ModelForm, TextInput
from .models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = [
            'id',
            'user'
        ]
        widgets = {
            'phone_number': TextInput()
        }
