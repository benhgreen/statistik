from django import forms
from statistik.constants import PLAYSIDE_CHOICES, TECHNIQUE_CHOICES, \
    RECOMMENDED_OPTIONS_CHOICES, RATING_VALIDATORS, MAX_RATING, MIN_RATING


class RegisterForm(forms.Form):
    username = forms.CharField(label="USERNAME")
    email = forms.EmailField(label="EMAIL", required=False,
                             help_text='Optional.')
    password = forms.CharField(label="PASSWORD", widget=forms.PasswordInput)
    reenter_password = forms.CharField(label="RE-ENTER PASSWORD",
                                       widget=forms.PasswordInput)
    dj_name = forms.CharField(label="DJ NAME", max_length=6)
    location = forms.CharField(label="LOCATION", max_length=64)
    playside = forms.ChoiceField(label="PLAYSIDE", choices=PLAYSIDE_CHOICES)
    best_techniques = forms.MultipleChoiceField(label="MOST INSANE TECHNIQUES",
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

        if len(data.get('best_techniques')) > 3:
            self.add_error('best_techniques', 'Please select no more than 3.')
            return False

        return True


class ReviewForm(forms.Form):
    RANGE_HELP_TEXT = "Range: 1.0-14.0."

    text = forms.CharField(label="REVIEW TEXT",
                           help_text="Optional, limit 256 characters.",
                           max_length=256,
                           widget=forms.Textarea(
                               attrs={'rows': 4, 'cols': 15}), required=False)
    clear_rating = forms.FloatField(label="NC RATING",
                                    help_text=RANGE_HELP_TEXT,
                                    required=False,
                                    validators=RATING_VALIDATORS)
    hc_rating = forms.FloatField(label="HC RATING",
                                 help_text=RANGE_HELP_TEXT,
                                 required=False,
                                 validators=RATING_VALIDATORS)
    exhc_rating = forms.FloatField(label="EXHC RATING",
                                   help_text=RANGE_HELP_TEXT,
                                   required=False,
                                   validators=RATING_VALIDATORS)
    score_rating = forms.FloatField(label="SCORE RATING",
                                    help_text=RANGE_HELP_TEXT,
                                    required=False,
                                    validators=RATING_VALIDATORS)
    characteristics = forms.MultipleChoiceField(label="CHARACTERISTICS",
                                                choices=TECHNIQUE_CHOICES,
                                                widget=forms.CheckboxSelectMultiple(),
                                                required=False)

    recommended_options = forms.MultipleChoiceField(
        label="RECOMMENDED OPTIONS (FOR YOUR PLAY SIDE)",
        choices=RECOMMENDED_OPTIONS_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    def clean(self):
        cleaned_data = super(ReviewForm, self).clean()
        for attr in ['clear_rating', 'hc_rating', 'exhc_rating',
                     'score_rating']:
            if cleaned_data.get(attr):
                cleaned_data[attr] = round(cleaned_data[attr], 1)
        return cleaned_data

    def is_valid(self, difficulty=None):
        if not super(ReviewForm, self).is_valid():
            return False
        max_rating = min(difficulty + 2, MAX_RATING)
        min_rating = max(difficulty - 2, MIN_RATING)
        for field in ['clear_rating', 'hc_rating', 'exhc_rating',
                      'score_rating']:
            rating = self.cleaned_data.get(field)
            if rating is not None and not min_rating <= rating <= max_rating:
                self.add_error(field,
                               'Please rate within 2.0 of actual difficulty.')
                return False
        return True
