from django import forms
from django.utils.translation import ugettext_lazy as _
from statistik.constants import PLAYSIDE_CHOICES, TECHNIQUE_CHOICES, \
    RECOMMENDED_OPTIONS_CHOICES, RATING_VALIDATORS, MAX_RATING, MIN_RATING, \
    localize_choices, DIFFICULTY_SPIKE_CHOICES, FULL_VERSION_NAMES, RATING_CHOICES, \
    CHART_TYPE_CHOICES, VERSION_CHOICES, PLAY_STYLE_CHOICES, IIDX, DDR


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
    best_techniques_iidx = forms.MultipleChoiceField(label=_("MOST INSANE IIDX TECHNIQUES"),
                                                help_text=_("Limit 3."),
                                                choices=localize_choices(TECHNIQUE_CHOICES[IIDX]),
                                                widget=forms.CheckboxSelectMultiple(),
                                                required=False)
    best_techniques_ddr = forms.MultipleChoiceField(label=_("MOST INSANE DDR TECHNIQUES"),
                                                help_text=_("Limit 3."),
                                                choices=localize_choices(TECHNIQUE_CHOICES[DDR]),
                                                widget=forms.CheckboxSelectMultiple(),
                                                required=False)

    def is_valid(self):
        super(RegisterForm, self).is_valid()
        data = self.cleaned_data
        if data.get('password') != data.get('reenter_password'):
            self.add_error('password', _('Passwords do not match.'))
            self.add_error('reenter_password', _('Passwords do not match.'))
            return False

        for techniques_field in ['best_techniques_iidx', 'best_techniques_ddr']:
            if len(data.get(techniques_field)) > 3:
                self.add_error(techniques_field, _('Please select no more than 3.'))
                return False
        return True

# TODO: see if this can be made back into just ReviewForm, wasn't letting me just have a game parameter
# because form fields are set when the class is imported and game isn't known until an instance is made much later


class IIDXReviewForm(forms.Form):

    RANGE_HELP_TEXT = _("Range: 1.0-14.0.")

    text = forms.CharField(label=_("REVIEW TEXT"),
                           help_text=_("Optional, limit 256 characters."),
                           max_length=256,
                           widget=forms.Textarea(
                               attrs={'rows': 4, 'cols': 15}), required=False)
    clear_rating = forms.FloatField(label=_("NC RATING"),
                                    help_text=RANGE_HELP_TEXT,
                                    required=False,
                                    validators=RATING_VALIDATORS[IIDX])
    hc_rating = forms.FloatField(label=_("HC RATING"),
                                 help_text=RANGE_HELP_TEXT,
                                 required=False,
                                 validators=RATING_VALIDATORS[IIDX])
    exhc_rating = forms.FloatField(label=_("EXHC RATING"),
                                   help_text=RANGE_HELP_TEXT,
                                   required=False,
                                   validators=RATING_VALIDATORS[IIDX])
    score_rating = forms.FloatField(label=_("SCORE RATING"),
                                    help_text=RANGE_HELP_TEXT,
                                    required=False,
                                    validators=RATING_VALIDATORS[IIDX])

    difficulty_spike = forms.ChoiceField(label=_('DIFFICULTY FOCUS'),
                                         required=False,
                                         choices=DIFFICULTY_SPIKE_CHOICES)

    characteristics = forms.MultipleChoiceField(label=_("CHARACTERISTICS"),
                                                choices=localize_choices(TECHNIQUE_CHOICES[IIDX]),
                                                widget=forms.CheckboxSelectMultiple(),
                                                required=False)

    recommended_options = forms.MultipleChoiceField(
        label=_("RECOMMENDED OPTIONS (FOR YOUR PLAY SIDE)"),
        choices=localize_choices(RECOMMENDED_OPTIONS_CHOICES[IIDX]),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    def clean(self):
        cleaned_data = super(IIDXReviewForm, self).clean()
        for attr in ['clear_rating', 'hc_rating', 'exhc_rating',
                     'score_rating']:
            if cleaned_data.get(attr):
                cleaned_data[attr] = round(cleaned_data[attr], 1)
        return cleaned_data

    def is_valid(self, difficulty=None):
        if not super(IIDXReviewForm, self).is_valid():
            return False
        max_rating = min(difficulty + 2, MAX_RATING[IIDX])
        min_rating = max(difficulty - 2, MIN_RATING)
        for field in ['clear_rating', 'hc_rating', 'exhc_rating',
                      'score_rating']:
            rating = self.cleaned_data.get(field)
            if rating is not None and not min_rating <= rating <= max_rating:
                self.add_error(field,
                               _('Please rate within 2.0 of actual difficulty.'))
                return False
        return True


class DDRReviewForm(forms.Form):

    RANGE_HELP_TEXT = _("Range: 1.0-21.0.")

    text = forms.CharField(label=_("REVIEW TEXT"),
                           help_text=_("Optional, limit 256 characters."),
                           max_length=256,
                           widget=forms.Textarea(
                               attrs={'rows': 4, 'cols': 15}), required=False)
    clear_rating = forms.FloatField(label=_("NC RATING"),
                                    help_text=RANGE_HELP_TEXT,
                                    required=False,
                                    validators=RATING_VALIDATORS[DDR])
    score_rating = forms.FloatField(label=_("SCORE RATING"),
                                    help_text=RANGE_HELP_TEXT,
                                    required=False,
                                    validators=RATING_VALIDATORS[DDR])

    difficulty_spike = forms.ChoiceField(label=_('DIFFICULTY FOCUS'),
                                         required=False,
                                         choices=DIFFICULTY_SPIKE_CHOICES)

    characteristics = forms.MultipleChoiceField(label=_("CHARACTERISTICS"),
                                                choices=localize_choices(TECHNIQUE_CHOICES[DDR]),
                                                widget=forms.CheckboxSelectMultiple(),
                                                required=False)

    recommended_options = forms.ChoiceField(
        label=_("RECOMMENDED SPEED MOD"),
        choices=localize_choices(RECOMMENDED_OPTIONS_CHOICES[DDR]),
        initial=RECOMMENDED_OPTIONS_CHOICES[DDR][3][0],
        required=False,
    )

    def clean(self):
        cleaned_data = super(DDRReviewForm, self).clean()
        for attr in ['clear_rating', 'score_rating']:
            if cleaned_data.get(attr):
                cleaned_data[attr] = round(cleaned_data[attr], 1)
        # put the speed mod in an array even though it's just one choice because iidx can expect multiple options
        if cleaned_data.get('recommended_options'):
            cleaned_data['recommended_options'] = [cleaned_data['recommended_options']]
        return cleaned_data

    def is_valid(self, difficulty=None):
        if not super(DDRReviewForm, self).is_valid():
            return False
        max_rating = min(difficulty + 2, MAX_RATING[DDR])
        min_rating = max(difficulty - 2, MIN_RATING)
        for field in ['clear_rating', 'score_rating']:
            rating = self.cleaned_data.get(field)
            if rating is not None and not min_rating <= rating <= max_rating:
                self.add_error(field,
                               _('Please rate within 2.0 of actual difficulty.'))
                return False
        return True


class RatingField(forms.ChoiceField):
    def to_python(self, value):
        if not value:
            return None
        return float(value)


class IIDXSearchForm(forms.Form):
    title = forms.CharField(label=_("TITLE"),
                            max_length=100,
                            required=False)
    artist = forms.CharField(label=_("ARTIST"),
                             max_length=50,
                             required=False)
    genre = forms.CharField(label=_("GENRE"),
                            max_length=50,
                            required=False)
    min_difficulty = RatingField(label=_("MIN DIFFICULTY"),
                                 choices=[(i, str(i)) for i in range(1, 13)],
                                 validators=RATING_VALIDATORS[IIDX],
                                 initial=1,
                                 required=False)
    max_difficulty = RatingField(label=_("MAX DIFFICULTY"),
                                 choices=[(i, str(i)) for i in range(1, 13)],
                                 validators=RATING_VALIDATORS[IIDX],
                                 initial=12,
                                 required=False)
    min_nc = RatingField(label=_("MIN NC RATING"),
                         choices=RATING_CHOICES[IIDX],
                         validators=RATING_VALIDATORS[IIDX],
                         initial=MIN_RATING,
                         required=False)
    max_nc = RatingField(label=_("MAX NC RATING"),
                         choices=RATING_CHOICES[IIDX],
                         validators=RATING_VALIDATORS[IIDX],
                         initial=MAX_RATING[IIDX],
                         required=False)
    min_hc = RatingField(label=_("MIN HC RATING"),
                         choices=RATING_CHOICES[IIDX],
                         validators=RATING_VALIDATORS[IIDX],
                         initial=MIN_RATING,
                         required=False)
    max_hc = RatingField(label=_("MAX HC RATING"),
                         choices=RATING_CHOICES[IIDX],
                         validators=RATING_VALIDATORS[IIDX],
                         initial=MAX_RATING[IIDX],
                         required=False)
    min_exhc = RatingField(label=_("MIN EXHC RATING"),
                           choices=RATING_CHOICES[IIDX],
                           validators=RATING_VALIDATORS[IIDX],
                           initial=MIN_RATING,
                           required=False)
    max_exhc = RatingField(label=_("MAX EXHC RATING"),
                           choices=RATING_CHOICES[IIDX],
                           validators=RATING_VALIDATORS[IIDX],
                           initial=MAX_RATING[IIDX],
                           required=False)
    min_score = RatingField(label=_("MIN SCORE RATING"),
                           choices=RATING_CHOICES[IIDX],
                           validators=RATING_VALIDATORS[IIDX],
                           initial=MIN_RATING,
                           required=False)
    max_score = RatingField(label=_("MAX SCORE RATING"),
                            choices=RATING_CHOICES[IIDX],
                            validators=RATING_VALIDATORS[IIDX],
                            initial=MAX_RATING[IIDX],
                            required=False)
    play_style = forms.ChoiceField(label=_("PLAY STYLE"),
                              choices=PLAY_STYLE_CHOICES,
                              initial=0,
                              widget=forms.RadioSelect(),
                              required=False)
    version = forms.MultipleChoiceField(label=_("VERSION"),
                                        choices=[(i, n) for i, n in VERSION_CHOICES[IIDX]],
                                        widget=forms.CheckboxSelectMultiple(),
                                        required=False)
    techs = forms.MultipleChoiceField(label=_("TECHNIQUES"),
                                                choices=TECHNIQUE_CHOICES[IIDX],
                                                widget=forms.CheckboxSelectMultiple,
                                                required=False)

    def is_valid(self):
        super(IIDXSearchForm, self).is_valid()
        data = self.cleaned_data
        for (minimum, maximum) in [('min_difficulty', 'max_difficulty'),
                                   ('min_nc', 'max_nc'),
                                   ('min_hc', 'max_hc'),
                                   ('min_exhc', 'max_exhc'),
                                   ('min_score', 'max_score')]:
            min_difficulty = data.get(minimum)
            max_difficulty = data.get(maximum)
            if min_difficulty and max_difficulty and float(max_difficulty) < float(min_difficulty):
                for field in [minimum, maximum]:
                    self.add_error(field, '%s cannot be lower than %s.' % (maximum, minimum))
                return False
        # have to have at least one search filter
        if not self.changed_data:
            # self.add_error(None, 'must have at least one search filter')
            return False

        return True


class DDRSearchForm(forms.Form):
    title = forms.CharField(label=_("TITLE"),
                            max_length=100,
                            required=False)
    artist = forms.CharField(label=_("ARTIST"),
                             max_length=50,
                             required=False)
    min_difficulty = RatingField(label=_("MIN DIFFICULTY"),
                                 choices=[(i, str(i)) for i in range(1, 20)],
                                 validators=RATING_VALIDATORS[DDR],
                                 initial=1,
                                 required=False)
    max_difficulty = RatingField(label=_("MAX DIFFICULTY"),
                                 choices=[(i, str(i)) for i in range(1, 20)],
                                 validators=RATING_VALIDATORS[DDR],
                                 initial=19,
                                 required=False)
    min_nc = RatingField(label=_("MIN CLEAR RATING"),
                         choices=RATING_CHOICES[DDR],
                         validators=RATING_VALIDATORS[DDR],
                         initial=MIN_RATING,
                         required=False)
    max_nc = RatingField(label=_("MAX CLEAR RATING"),
                         choices=RATING_CHOICES[DDR],
                         validators=RATING_VALIDATORS[DDR],
                         initial=MAX_RATING[DDR],
                         required=False)
    min_score = RatingField(label=_("MIN SCORE RATING"),
                           choices=RATING_CHOICES[DDR],
                           validators=RATING_VALIDATORS[DDR],
                           initial=MIN_RATING,
                           required=False)
    max_score = RatingField(label=_("MAX SCORE RATING"),
                            choices=RATING_CHOICES[DDR],
                            validators=RATING_VALIDATORS[DDR],
                            initial=MAX_RATING[DDR],
                            required=False)
    play_style = forms.ChoiceField(label=_("PLAY STYLE"),
                              choices=PLAY_STYLE_CHOICES,
                              initial=0,
                              widget=forms.RadioSelect(),
                              required=False)
    version = forms.MultipleChoiceField(label=_("VERSION"),
                                        choices=[(i, n) for i, n in VERSION_CHOICES[DDR]],
                                        widget=forms.CheckboxSelectMultiple(),
                                        required=False)
    techs = forms.MultipleChoiceField(label=_("TECHNIQUES"),
                                                choices=TECHNIQUE_CHOICES[DDR],
                                                widget=forms.CheckboxSelectMultiple,
                                                required=False)

    def is_valid(self):
        super(DDRSearchForm, self).is_valid()
        data = self.cleaned_data
        for (minimum, maximum) in [('min_difficulty', 'max_difficulty'),
                                   ('min_nc', 'max_nc'),
                                   ('min_score', 'max_score')]:
            min_difficulty = data.get(minimum)
            max_difficulty = data.get(maximum)
            if min_difficulty and max_difficulty and float(max_difficulty) < float(min_difficulty):
                for field in [minimum, maximum]:
                    self.add_error(field, '%s cannot be lower than %s.' % (maximum, minimum))
                return False
        # have to have at least one search filter
        if not self.changed_data:
            # self.add_error(None, 'must have at least one search filter')
            return False

        return True
