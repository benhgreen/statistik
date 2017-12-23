"""
Constants, choices, and methods that are directly related to them
"""
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from numpy import arange

IIDX = 0
DDR = 1
GAMES = {'IIDX': IIDX, 'DDR': DDR}

GAME_CHOICES = [
    (0, 'IIDX'),
    (1, 'DDR')
]

MAX_RATING = {IIDX: 14.0, DDR: 21.0}
MIN_RATING = 1.0

RATING_CHOICES = [[(i, str(i)) for i in arange(MIN_RATING, MAX_RATING[game[0]]+.1, 0.1)] for game in GAME_CHOICES]

RATING_VALIDATORS = {game[0]: [MaxValueValidator(MAX_RATING[game[0]]),
                            MinValueValidator(MIN_RATING)] for game in GAME_CHOICES}

# A threshold beyond which scores should be considered outliers and not counted in the average rating
RATING_AVERAGE_THRESHOLD = 0.5

TECHNIQUE_CHOICES = {IIDX: [
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
    ],
    DDR: [(100, _('Crossovers')),
        (101, _('Gallops')),
        (102, _('Jumps')),
        (103, _('Speed Changes')),
        (104, _('Stops')),
        (105, _('Turns')),
        (106, _('Freeze Notes')),
        (107, _('Shock Arrows')),
        (108, _('Drills')),
        (109, _('Jacks')),
        (110, _('Step-Jumps')),
        (111, _('Candles'))
    ]}

DIFFICULTY_SPIKE_CHOICES = [
    (0, ''),
    (1, _('Beginning')),
    (2, _('Middle')),
    (3, _('End'))
]

SCORE_CATEGORY_CHOICES = {IIDX: [
        (0, 'NC'),
        (1, 'HC'),
        (2, 'EXHC'),
        (3, 'SCORE')
    ],
    DDR: [(0, 'CLEAR'),
        (1, 'SCORE')
    ]
}

SCORE_CATEGORY_NAMES = {IIDX: [
    'clear_rating',
    'hc_rating',
    'exhc_rating',
    'score_rating'
    ],
    DDR: ['clear_rating',
        'score_rating'
    ]
}

CHART_TYPE_CHOICES = {IIDX: [
        (0, 'SPN'),
        (1, 'SPH'),
        (2, 'SPA'),
        (3, 'DPN'),
        (4, 'DPH'),
        (5, 'DPA')
    ],
    DDR: [
        (100, 'BEG'),
        (101, 'BSP'),
        (102, 'DSP'),
        (103, 'ESP'),
        (104, 'CSP'),
        (105, 'BDP'),
        (106, 'DDP'),
        (107, 'EDP'),
        (108, 'CDP')]}

PLAY_STYLE_CHOICES = [
    (0, 'SP'),
    (1, 'DP')
]

VERSION_CHOICES = {IIDX: [
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
        (24, 'SIN'),
        (25, 'CB')],
    DDR: [
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
        (116, 'A')]
}

FULL_VERSION_NAMES = {IIDX: {
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
        24: 'Sinobuz',
        25: 'Cannon Ballers'},
    DDR: {
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
    }}

PLAYSIDE_CHOICES = [
    (0, '1P'),
    (1, '2P')
]

RECOMMENDED_OPTIONS_CHOICES = {IIDX: [
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
        (15, _('Mirror Right'))
    ],
    DDR: [(0, '0.25x'),
          (1, '0.5x'),
          (2, '0.75x'),
          (3, '1.0x'),
          (4, '1.25x'),
          (5, '1.5x'),
          (6, '1.75x'),
          (7, '2.0x'),
          (8, '2.25x'),
          (9, '2.5x'),
          (10, '2.75x'),
          (11, '3.0x'),
          (12, '3.25x'),
          (13, '3.5x'),
          (14, '3.75x'),
          (15, '4.0x'),
          (16, '4.5x'),
          (17, '5.0x'),
          (18, '5.5x'),
          (19, '6.0x'),
          (20, '6.5x'),
          (21, '7.0x'),
          (22, '7.5x'),
          (23, '8.0x')
    ]}

# The levels for single play for each game
SINGLES_LEVELS = {IIDX: range(0, 3),
                  DDR: range(100, 105)}

def localize_choices(choices):
    return [(choice[0], _(choice[1])) for choice in choices]


def generate_version_urls(game=IIDX):
    """
    Generate urls for ratings page based on VERSION_CHOICES
    :rtype list: List of tuples containing version abbreviation and link
    """
    return [(version[1], reverse('ratings', kwargs={'game': GAME_CHOICES[game][1]}) + "?version=%d" % version[0])
            for version in VERSION_CHOICES[game] if version[0]//100 == game]


def generate_level_urls(game):
    """
    Generate urls for ratings page based on levels (1-12)
    :rtype list: List of tuples containing level number and link
    """
    return [(level, reverse('ratings', kwargs={'game': GAME_CHOICES[game][1]}) + "?difficulty=%d" % level)
            for level in range(1, {IIDX: 13, DDR: 20}[game])]


def generate_elo_level_urls(game):
    """
    Generate urls for elo pages
    :param game: The game to generate levels for
    :rtype list: List of tuples containing level number and link
    """
    return [(level, reverse('elo', kwargs={'game': GAME_CHOICES[game][1]}) + "?level=%d" % level)
            for level in range(1, {IIDX: 13, DDR: 20}[game])]
