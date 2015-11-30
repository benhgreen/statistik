from django import forms
from statistik.constants import PLAYSIDE_CHOICES, TECHNIQUE_CHOICES
from statistik.models import Review


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
    text = forms.CharField(label="REVIEW TEXT", help_text="Optional, limit 256 characters.", widget=forms.Textarea(attrs={'rows':4, 'cols':15}), required=False)
    clear_rating = forms.FloatField(label="NC RATING", help_text="Example: 11.5")
    hc_rating = forms.FloatField(label="HC RATING", help_text="Example: 11.5")
    exhc_rating = forms.FloatField(label="EXHC RATING", help_text="Example: 11.5")
    score_rating = forms.FloatField(label="SCORE RATING", help_text="Example: 11.5")
    characteristics = forms.MultipleChoiceField(label="CHARACTERISTICS",
                                           choices=TECHNIQUE_CHOICES,
                                           widget=forms.CheckboxSelectMultiple(),
                                           required=False)

    def is_valid(self):
        return super(ReviewForm, self).is_valid()