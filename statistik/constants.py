"""
Constants, choices, and methods that are directly related to them
"""
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _

MAX_RATING = 14.0
MIN_RATING = 1.0

RATING_VALIDATORS = [MaxValueValidator(MAX_RATING),
                     MinValueValidator(MIN_RATING)]

TECHNIQUE_CHOICES = [
    (0, _('Scratching')),
    (1, _('Jacks')),
    (2, _('Speed Changes')),
    (3, _('Charge Notes')),
    (4, _('Scales')),
    (5, _('Chord Scales')),
    (6, _('Denim')),
    (7, _('Trills')),
    (8, _('Rolls')),
    (9, _('Chords'))
]

DIFFICULTY_SPIKE_CHOICES = [
    (0, ''),
    (1, _('Beginning')),
    (2, _('Middle')),
    (3, _('End'))
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
    (23, 'COP'),


    (101, '1st'),
    (102, '2nd'),
    (103, '3rd'),
    (104, '4th'),
    (105, '5th'),
    (106, 'MAX'),
    (107, 'MAX2'),
    (108, 'EXT'),
    (109, 'SN'),
    (110, 'SN2'),
    (111, 'X'),
    (112, 'X2'),
    (113, 'X3'),
    (114, '2013'),
    (115, '2014'),
    (116, 'A')
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
    23: 'Copula',
    
    101: '1stMIX',
    102: '2ndMIX',
    103: '3rdMIX',
    104: '4thMIX',
    105: '5thMIX',
    106: 'DDRMAX',
    107: 'DDRMAX2',
    108: 'DDR EXTREME',
    109: 'DDR SuperNOVA',
    110: 'DDR SuperNOVA2',
    111: 'DDR X',
    112: 'DDR X2',
    113: 'DDR X3',
    114: 'DDR 2013',
    115: 'DDR 2014',
    116: 'DDR A'
}

PLAYSIDE_CHOICES = [
    (0, '1P'),
    (1, '2P')
]

RECOMMENDED_OPTIONS_CHOICES = [
    (0, _('Regular')),
    (1, _('Random')),
    (2, _('S-Random')),
    (3, _('R-Random')),
    (4, _('Mirror')),
    (5, _('Flip')),
    (6, _('Regular Left')),
    (7, _('Random Left')),
    (8, _('S-Random Left')),
    (9, _('R-Random Left')),
    (10, _('Mirror Left')),
    (11, _('Regular Right')),
    (12, _('Random Right')),
    (13, _('S-Random Right')),
    (14, _('R-Random Right')),
    (15, _('Mirror Right')),

]


def localize_choices(choices):
    return [(choice[0], _(choice[1])) for choice in choices]


def generate_version_urls(game):
    """
    Generate urls for ratings page based on VERSION_CHOICES
    :rtype list: List of tuples containing version abbreviation and link
    """
    return [(version[1], reverse('ratings') + "?version=%d&game=%d" % (version[0], game))
            for version in VERSION_CHOICES if version[0]//100 == game]


def generate_level_urls(game):
    """
    Generate urls for ratings page based on levels (1-12)
    :rtype list: List of tuples containing level number and link
    """
    return [(level, reverse('ratings') + "?difficulty=%d&game=%d" % (level, game))
            for level in range(1,{0: 13, 1: 20}[game])]


def generate_elo_level_urls():
    """
    Generate urls for elo pages
    :rtype list: List of tuples containing level number and link
    """
    return [(level, reverse('elo') + "?level=%d" % level)
            for level in range(1,13)]
