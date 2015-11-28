from django import forms
from statistik.constants import PLAYSIDE_CHOICES, TECHNIQUE_CHOICES


class RegisterForm(forms.Form):
    username = forms.CharField(label="USERNAME", max_length=32)
    email = forms.EmailField(label="EMAIL", required=False, help_text='optional')
    password = forms.CharField(label="PASSWORD", widget=forms.PasswordInput)
    reenter_password = forms.CharField(label="RE-ENTER PASSWORD",
                                       widget=forms.PasswordInput)
    dj_name = forms.CharField(label="DJ NAME", max_length=6)
    location = forms.CharField(label="LOCATION", max_length=64)
    playside = forms.ChoiceField(label="PLAYSIDE", choices=PLAYSIDE_CHOICES)
    best_stats = forms.MultipleChoiceField(label="MOST INSANE TECHNIQUES",
                                           help_text="limit 3",
                                           choices=TECHNIQUE_CHOICES,
                                           widget=forms.CheckboxSelectMultiple(),
                                           required=False)


class ReviewForm(forms.Form):
    pass
