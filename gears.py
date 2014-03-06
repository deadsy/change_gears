#! /usr/bin/python
#------------------------------------------------------------------------------

import math

#------------------------------------------------------------------------------
# geometric constants

_MM_PER_INCH = 25.4
_IDLER_TEETH = 40.0
_LEADSCREW_TPI = 12.0
_GEAR_PITCH = 0.125

#------------------------------------------------------------------------------

# gear configurations
# ab -> gears a and b are on the same shaft
# a-b -> gears a and b are meshed
_gear_cfg = (
    'a-b-c',
    'ab-cd-e',
    'ab-c-d',
    'a-bc-d',
)

# the change gear set (by tooth count)
_gear_set = (
    30.0, 35.0, 40.0, 45.0, 48.0, 50.0, 60.0, 66.0,
    68.0, 70.0, 70.0, 72.0, 75.0, 80.0, 90.0, 100.0
)

#------------------------------------------------------------------------------

def calc_pitch(cfg, gears):
    """return the screw pitch in inches"""

    (a, b, c, d, e) = gears

    ratio = _IDLER_TEETH / a

    if cfg == 'a-b-c':
        ratio *= (a / c)
    elif cfg == 'ab-cd-e':
        ratio *= (b / c)
        ratio *= (d / e)
    elif cfg == 'ab-c-d':
        ratio *= (b / d)
    elif cfg == 'a-bc-d':
        ratio *= (a / b)
        ratio *= (c / d)
    else:
        assert(0)

    return ratio / _LEADSCREW_TPI

#------------------------------------------------------------------------------

def calc_length(cfg, gears):
    """return the gear train length in teeth"""

    (a, b, c, d, e) = gears

    n = _IDLER_TEETH / 2.0

    if cfg == 'a-b-c':
        n += (a + b + (c / 2.0))
    elif cfg == 'ab-cd-e':
        n += ((a / 2.0) + (b / 2.0) + (c / 2.0) + (d / 2.0) + (e / 2.0))
    elif cfg == 'ab-c-d':
        n += ((a / 2.0)+ (b / 2.0) + c + (d / 2.0))
    elif cfg == 'a-bc-d':
        n += (a + (b / 2.0) + (c / 2.0) + (d / 2.0))
    else:
        assert(0)

    return n

#------------------------------------------------------------------------------
# geometric constraints

_MINIMUM_GTL = 154.0        # Minimum gear train length
_MIN_FINAL_GEARS = 80.0     # Minimum center to center for final 2 gears
_MAX_AB_DIFFERENCE = 6.0    # Maximum AB difference for gear configs 1 & 2
_MIN_GEAR_CLEARANCE = 4.0   # Minimum gear to gear clearance
_GEAR_X_SIZE = 30.0         # Size of a hub with no gear present
_MAX_SLOT_GEARS = 168.0     # Maximum length for engaged gears in the slot

def is_valid(cfg , gears):
    """return True if this is a geometrically valid gear configuration"""

    (a, b, c, d, e) = gears

    if cfg == 'a-b-c':
        if (a + b) > _MAX_SLOT_GEARS:
            return False
        if (b + c) < _MIN_FINAL_GEARS:
            return False
    elif cfg == 'ab-cd-e':
        if (b + c) > _MAX_SLOT_GEARS:
            return False
        if (d + e) < _MIN_FINAL_GEARS:
            return False
        if (b - a) > _MAX_AB_DIFFERENCE:
            return False
        if (b + c) - (a + d) < _MIN_GEAR_CLEARANCE:
            return False
        if (d + e) - (c + _GEAR_X_SIZE) < _MIN_GEAR_CLEARANCE:
            return False
    elif cfg == 'ab-c-d':
        if (b + c) > _MAX_SLOT_GEARS:
            return False
        if (c + d) < _MIN_FINAL_GEARS:
            return False
        if (b - a) > _MAX_AB_DIFFERENCE:
            return False
    elif cfg == 'a-bc-d':
        if (a + b) > _MAX_SLOT_GEARS:
            return False
        if (c + d) < _MIN_FINAL_GEARS:
            return False
        if (a + b) - (c + _GEAR_X_SIZE) < _MIN_GEAR_CLEARANCE:
            return False
        if (c + d) - (b + _GEAR_X_SIZE) < _MIN_GEAR_CLEARANCE:
            return False
    else:
        assert(0)

    if calc_length(cfg, gears) < _MINIMUM_GTL:
        return False

    return True

#------------------------------------------------------------------------------

def display_gears(cfg, gears, goal, mode):

    pitch = calc_pitch(cfg, gears)

    if mode == 'imperial':
        print('desired tpi = %f' % (1.0 / goal))
        print('actual tpi = %f' % (1.0 / pitch))
    elif mode == 'metric':
        print('desired pitch = %f mm' % (goal * _MM_PER_INCH))
        print('actual pitch = %f mm' % (pitch * _MM_PER_INCH))
    else:
        assert(0)

    error = math.fabs(pitch - goal)
    error = (error / goal) * 100.0
    print('pitch error = %.2f%%' % error)

    (a, b, c, d, e) = gears

    if cfg == 'a-b-c':
        print('%d-%d-%d' % (a, b, c))
    elif cfg == 'ab-cd-e':
        print('%d:%d-%d:%d-%d' % (a, b, c, d, e))
    elif cfg == 'ab-c-d':
        print('%d:%d-%d-%d' % (a, b, c, d))
    elif cfg == 'a-bc-d':
        print('%d-%d:%d-%d' % (a, b, c, d))
    else:
        assert(0)

#------------------------------------------------------------------------------

def search_gears(pitch):
    """find the gear configuration most closely matching the provided pitch"""
    pass

#------------------------------------------------------------------------------

def main():
    goal_pitch = 1.75 / _MM_PER_INCH
    display_gears('ab-cd-e', (68.0, 72.0, 80.0, 75.0, 48.0), goal_pitch, 'metric')

#------------------------------------------------------------------------------

main()

#------------------------------------------------------------------------------
