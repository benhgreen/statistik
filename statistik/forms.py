from django import forms
from statistik.constants import PLAYSIDE_CHOICES, TECHNIQUE_CHOICES


class RegisterForm(forms.Form):
    username = forms.CharField(label="USERNAME", )
    email = forms.EmailField(label="EMAIL", required=False, help_text='Optional.')
    password = forms.CharField(label="PASSWORD", widget=forms.PasswordInput)
    reenter_password = forms.CharField(label="RE-ENTER PASSWORD",
                                       widget=forms.PasswordInput)
    dj_name = forms.CharField(label="DJ NAME", max_length=6)
    location = forms.CharField(label="LOCATION", max_length=64)
    playside = forms.ChoiceField(label="PLAYSIDE", choices=PLAYSIDE_CHOICES)
    best_stats = forms.MultipleChoiceField(label="MOST INSANE TECHNIQUES",
                                           help_text="Limit 3.",
                                           choices=TECHNIQUE_CHOICES,
                                           widget=forms.CheckboxSelectMultiple(),
                                           required=False)

    def is_valid(self):
        super(RegisterForm, self).is_valid()
        data = self.cleaned_data
        if data.get('password') != data.get('reenter_password'):
            self.add_error('password', 'Passwords do not match.')
            self.add_error('reenter_password', 'Passwords do not match.')
            return False

        if len(data.get('best_stats')) > 3:
            self.add_error('best_stats', 'Please select no more than 3.')
            return False

        return True


class ReviewForm(forms.Form):
    pass
