from django import forms
from statistik.constants import PLAYSIDE_CHOICES, TECHNIQUE_CHOICES, \
    RECOMMENDED_OPTIONS_CHOICES, RATING_VALIDATORS, MAX_RATING, MIN_RATING, \
    LANGUAGE_CHOICES, SCORE_CATEGORY_CHOICES, get_localized_choices


class RegisterForm(forms.Form):

    def __init__(self, *args, language=0):
        super(RegisterForm, self).__init__(*args)
        self.localize(language)

    username = forms.CharField()
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    reenter_password = forms.CharField(widget=forms.PasswordInput)
    dj_name = forms.CharField(label="DJ NAME", max_length=6)
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES)
    location = forms.CharField(max_length=64)
    playside = forms.ChoiceField(choices=PLAYSIDE_CHOICES)
    best_techniques = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                                required=False)

    def localize(self, language):
        self.fields.get('username').label = ["USERNAME", "ユーザーネーム"][language]
        self.fields.get('email').label = ["EMAIL", "メールアドレス"][language]
        self.fields.get('email').help_text = ['Optional.', '任意'][language]
        self.fields.get('password').label = ["PASSWORD", "パスワード"][language]
        self.fields.get('reenter_password').label = ["RE-ENTER PASSWORD", "パスワード【再入力】"][language]
        self.fields.get('language').label = ["LANGUAGE", "言語選択"][language]
        self.fields.get('language').initial = language
        self.fields.get('location').label = ["LOCATION", "位置"][language]
        self.fields.get('playside').label = ["PLAYSIDE", "プレーサイド"][language]

        tech_field = self.fields.get('best_techniques')
        tech_field.label = ["MOST INSANE TECHNIQUES", "得意な特徴"][language]
        tech_field.help_text = ["Limit 3.", "最大3つ"][language]
        tech_field.choices = get_localized_choices('TECHNIQUE_CHOICES', language)

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

    def __init__(self, *args, language=0):
        super(ReviewForm, self).__init__(*args)
        self.localize(language)

    text = forms.CharField(max_length=256,
                           widget=forms.Textarea(
                               attrs={'rows': 4, 'cols': 15}), required=False)
    clear_rating = forms.FloatField(required=False,
                                    validators=RATING_VALIDATORS)
    hc_rating = forms.FloatField(required=False,
                                 validators=RATING_VALIDATORS)
    exhc_rating = forms.FloatField(required=False,
                                   validators=RATING_VALIDATORS)
    score_rating = forms.FloatField(required=False,
                                    validators=RATING_VALIDATORS)
    characteristics = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                                required=False)

    recommended_options = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    def localize(self, language):
        RANGE_HELP_TEXT = ["Range: 1.0-14.0.", "範囲は1.0から14.0まで"][language]
        self.fields.get('text').label = ["REVIEW TEXT", "意見・攻略テキスト"][language]
        self.fields.get('text').help_text = ["Optional, limit 256 characters.", "任意・最大256字"][language]
        for i, type in enumerate(['clear_rating', 'hc_rating', 'exhc_rating', 'score_rating']):
            field = self.fields.get(type)
            field.help_text = RANGE_HELP_TEXT
            type_abbrev = SCORE_CATEGORY_CHOICES[i][1]
            field.label = [type_abbrev + ' RATING', '難易度(' + type_abbrev + ')'][language]
        self.fields.get('characteristics').label = ["CHARACTERISTICS", "特徴"][language]
        self.fields.get('characteristics').choices = get_localized_choices('TECHNIQUE_CHOICES', language)
        self.fields.get('recommended_options').label = ["RECOMMENDED OPTIONS (FOR YOUR PLAY SIDE)", "おすすめのOP(あなたのプレーサイド)"][language]

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
