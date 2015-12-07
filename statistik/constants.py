from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

MAX_RATING = 14.0
MIN_RATING = 1.0

RATING_VALIDATORS = [MaxValueValidator(MAX_RATING),
                     MinValueValidator(MIN_RATING)]

TECHNIQUE_CHOICES = [
    (0, 'Scratching'),
    (1, 'Jacks'),
    (2, 'Speed Changes'),
    (3, 'Charge Notes'),
    (4, 'Scales'),
    (5, 'Chord Scales'),
    (6, 'Denim')
]

SCORE_CATEGORY_CHOICES = [
    (0, 'NC'),
    (1, 'HC'),
    (2, 'EXHC'),
    (3, 'SCORE')
]

SCORE_CATEGORY_NAMES = [
    'clear_rating',
    'hc_rating',
    'exhc_rating',
    'score_rating'
]

CHART_TYPE_CHOICES = [
    (0, 'SPN'),
    (1, 'SPH'),
    (2, 'SPA'),
    (3, 'DPN'),
    (4, 'DPH'),
    (5, 'DPA')
]

VERSION_CHOICES = [
    (1, '1st'),
    (2, '2nd'),
    (3, '3rd'),
    (4, '4th'),
    (5, '5th'),
    (6, '6th'),
    (7, '7th'),
    (8, '8th'),
    (9, '9th'),
    (10, '10th'),
    (11, 'RED'),
    (12, 'HS'),
    (13, 'DD'),
    (14, 'GO'),
    (15, 'DJT'),
    (16, 'EMP'),
    (17, 'SIR'),
    (18, 'RA'),
    (19, 'LIN'),
    (20, 'TRI'),
    (21, 'SPD'),
    (22, 'PEN'),
    (23, 'COP')
]

FULL_VERSION_NAMES = {
    1: '1st Style',
    2: '2nd Style',
    3: '3rd Style',
    4: '4th Style',
    5: '5th Style',
    6: '6th Style',
    7: '7th Style',
    8: '8th Style',
    9: '9th Style',
    10: '10th Style',
    11: 'IIDX RED',
    12: 'Happy Sky',
    13: 'DistorteD',
    14: 'Gold',
    15: 'DJ Troopers',
    16: 'Empress',
    17: 'Sirius',
    18: 'Resort Anthem',
    19: 'Lincle',
    20: 'Tricoro',
    21: 'Spada',
    22: 'Pendual',
    23: 'Copula'
}

PLAYSIDE_CHOICES = [
    (0, '1P'),
    (1, '2P')
]

RECOMMENDED_OPTIONS_CHOICES = [
    (0, 'Regular'),
    (1, 'Random'),
    (2, 'S-Random'),
    (3, 'R-Random'),
    (4, 'Mirror')
]

def generate_version_urls():
    return [(version[1], reverse('ratings') + "?version=%d" % version[0])
            for version in VERSION_CHOICES]


def generate_level_urls():
    return [(level, reverse('ratings') + "?difficulty=%d" % level)
            for level in range(1,13)]
