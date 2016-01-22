from django import forms
from django.utils.translation import ugettext_lazy as _
from statistik.constants import PLAYSIDE_CHOICES, TECHNIQUE_CHOICES, \
    RECOMMENDED_OPTIONS_CHOICES, RATING_VALIDATORS, MAX_RATING, MIN_RATING, \
    localize_choices, DIFFICULTY_SPIKE_CHOICES


class RegisterForm(forms.Form):
    username = forms.CharField(label=_("USERNAME"))
    email = forms.EmailField(label=_("EMAIL"), required=False,
                             help_text=_('Optional.'))
    password = forms.CharField(label=_("PASSWORD"), widget=forms.PasswordInput)
    reenter_password = forms.CharField(label=_("RE-ENTER PASSWORD"),
                                       widget=forms.PasswordInput)
    dj_name = forms.CharField(label="DJ NAME", max_length=6)
    location = forms.CharField(label=_("LOCATION"), max_length=64)
    playside = forms.ChoiceField(label=_("PLAYSIDE"), choices=PLAYSIDE_CHOICES)
    best_techniques = forms.MultipleChoiceField(label=_("MOST INSANE TECHNIQUES"),
                                                help_text=_("Limit 3."),
                                                choices=localize_choices(TECHNIQUE_CHOICES),
                                                widget=forms.CheckboxSelectMultiple(),
                                                required=False)

    def is_valid(self):
        super(RegisterForm, self).is_valid()
        data = self.cleaned_data
        if data.get('password') != data.get('reenter_password'):
            self.add_error('password', _('Passwords do not match.'))
            self.add_error('reenter_password', _('Passwords do not match.'))
            return False

        if len(data.get('best_techniques')) > 3:
            self.add_error('best_techniques', _('Please select no more than 3.'))
            return False

        return True


class ReviewForm(forms.Form):
    RANGE_HELP_TEXT = _("Range: 1.0-14.0.")

    text = forms.CharField(label=_("REVIEW TEXT"),
                           help_text=_("Optional, limit 256 characters."),
                           max_length=256,
                           widget=forms.Textarea(
                               attrs={'rows': 4, 'cols': 15}), required=False)
    clear_rating = forms.FloatField(label=_("NC RATING"),
                                    help_text=RANGE_HELP_TEXT,
                                    required=False,
                                    validators=RATING_VALIDATORS)
    hc_rating = forms.FloatField(label=_("HC RATING"),
                                 help_text=RANGE_HELP_TEXT,
                                 required=False,
                                 validators=RATING_VALIDATORS)
    exhc_rating = forms.FloatField(label=_("EXHC RATING"),
                                   help_text=RANGE_HELP_TEXT,
                                   required=False,
                                   validators=RATING_VALIDATORS)
    score_rating = forms.FloatField(label=_("SCORE RATING"),
                                    help_text=RANGE_HELP_TEXT,
                                    required=False,
                                    validators=RATING_VALIDATORS)

    difficulty_spike = forms.MultipleChoiceField(label=_('DIFFICULTY FOCUS'),
                                                 required=False,
                                                 choices=DIFFICULTY_SPIKE_CHOICES)

    characteristics = forms.MultipleChoiceField(label=_("CHARACTERISTICS"),
                                                choices=localize_choices(TECHNIQUE_CHOICES),
                                                widget=forms.CheckboxSelectMultiple(),
                                                required=False)

    recommended_options = forms.MultipleChoiceField(
        label=_("RECOMMENDED OPTIONS (FOR YOUR PLAY SIDE)"),
        choices=localize_choices(RECOMMENDED_OPTIONS_CHOICES),
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
                               _('Please rate within 2.0 of actual difficulty.'))
                return False
        return True
