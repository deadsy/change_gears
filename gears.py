#! /usr/bin/python
#------------------------------------------------------------------------------

import math
import itertools
import html

#------------------------------------------------------------------------------
# common thread pitches

_common_metric = (
    0.20, 0.25, 0.35, 0.40, 0.45, 0.50, 0.60, 0.70,
    0.75, 0.80, 1.00, 1.25, 1.50, 1.75, 2.00, 2.50,
    3.00, 3.50, 4.00, 4.50, 5.00, 5.50, 6.00,
)

_common_inch = (
    8.0, 9.0, 10.0, 11.0, 11.5, 12.0, 13.0, 14.0, 16.0,
    18.0, 20.0, 24.0, 28.0, 32.0, 36.0, 40.0, 44.0,
    48.0, 56.0, 64.0, 72.0, 80.0
)

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

def generate_sets(sets, cfg, gear_set):
    """generate pitch solutions for a given gear configuration and set of gears"""
    for gears in gear_set:
        if is_valid(cfg, gears):
            sets.append((calc_pitch(cfg, gears), cfg, gears))

def generate_change_gears():
    """generate a sorted list of change gear sets across all gear configurations and gear sets"""
    sets = []
    # generate the gear permutations
    _3gears = tuple(itertools.permutations(_gear_set, 3))
    _4gears = tuple(itertools.permutations(_gear_set, 4))
    _5gears = tuple(itertools.permutations(_gear_set, 5))
    # pad all gear sets to 5 elements with dummys
    _3gears = tuple([(a, b, c, 0, 0)for (a, b, c) in _3gears])
    _4gears = tuple([(a, b, c, d, 0)for (a, b, c, d) in _4gears])
    # generate the solutions for each gear configuration
    generate_sets(sets, 'a-b-c', _3gears)
    generate_sets(sets, 'ab-c-d', _4gears)
    generate_sets(sets, 'a-bc-d', _4gears)
    generate_sets(sets, 'ab-cd-e', _5gears)
    sets.sort()
    return sets

#------------------------------------------------------------------------------

def search_gears(sets, pitch):
    """return the list index of the gear configuration most closely matching the pitch"""
    if not sets:
        return None
    # do a binary search of the sorted solution list
    hi = len(sets) - 1
    lo = 0
    while hi - lo > 1:
        i = (hi + lo) / 2
        if sets[i][0] >= pitch:
            # move to lower pitch values
            hi = i
        else:
            # move to higher pitch values
            lo = i
    # pick the index with the lowest error
    hi_error = sets[hi][0] - pitch
    lo_error = pitch - sets[lo][0]
    return (hi, lo)[lo_error <= hi_error]

#------------------------------------------------------------------------------

def gears_txt(soln, goal, mode):

    s = []
    (pitch, cfg, gears) = soln

    if mode == 'inch':
        s.append('desired tpi = %f' % (1.0 / goal))
        s.append('actual tpi = %f' % (1.0 / pitch))
    elif mode == 'metric':
        s.append('desired pitch = %f mm' % (goal * _MM_PER_INCH))
        s.append('actual pitch = %f mm' % (pitch * _MM_PER_INCH))
    else:
        assert(0)

    error = math.fabs(pitch - goal)
    error = (error / goal) * 100.0
    s.append('pitch error = %.2f%%' % error)

    (a, b, c, d, e) = gears

    if cfg == 'a-b-c':
        s.append('%d-%d-%d' % (a, b, c))
    elif cfg == 'ab-cd-e':
        s.append('%d:%d-%d:%d-%d' % (a, b, c, d, e))
    elif cfg == 'ab-c-d':
        s.append('%d:%d-%d-%d' % (a, b, c, d))
    elif cfg == 'a-bc-d':
        s.append('%d-%d:%d-%d' % (a, b, c, d))
    else:
        assert(0)

    return '\n'.join(s)


def gears_html(soln, goal, mode):

    td = []
    (pitch, cfg, gears) = soln

    if mode == 'inch':
        td.append(html.tag_td('%.1f' % (1.0 / goal)))
        td.append(html.tag_td('%.2f' % (1.0 / pitch)))
    elif mode == 'metric':
        td.append(html.tag_td('%.2f' % (goal * _MM_PER_INCH)))
        td.append(html.tag_td('%.3f' % (pitch * _MM_PER_INCH)))
    else:
        assert(0)

    error = math.fabs(pitch - goal)
    error = (error / goal) * 100.0
    td.append(html.tag_td('%.2f%%' % error))

    (a, b, c, d, e) = gears

    if cfg == 'a-b-c':
        td.append(html.tag_td('%d-%d-%d' % (a, b, c)))
    elif cfg == 'ab-cd-e':
        td.append(html.tag_td('%d:%d-%d:%d-%d' % (a, b, c, d, e)))
    elif cfg == 'ab-c-d':
        td.append(html.tag_td('%d:%d-%d-%d' % (a, b, c, d)))
    elif cfg == 'a-bc-d':
        td.append(html.tag_td('%d-%d:%d-%d' % (a, b, c, d)))
    else:
        assert(0)

    return html.indent('\n'.join(td))

#------------------------------------------------------------------------------

_ofile = 'stuff.html'

def main():

    # generate the complete set of valid change gears
    sets = generate_change_gears()

    inch_solns = []
    for tpi in _common_inch:
        pitch = 1.0 / float(tpi)
        inch_solns.append((search_gears(sets, pitch), pitch))

    metric_solns = []
    for mm in _common_metric:
        pitch = float(mm) / _MM_PER_INCH
        metric_solns.append((search_gears(sets, pitch), pitch))

    if _ofile.endswith('txt'):
        s = []
        for (i, pitch) in inch_solns:
            s.append(gears_txt(sets[i], pitch, 'inch'))
        for (i, pitch) in metric_solns:
            s.append(gears_txt(sets[i], pitch, 'metric'))
        f = open(_ofile, 'w')
        f.write('\n'.join(s))
        f.close()


    if _ofile.endswith('html'):
        page = []
        page.append(html.include('info.txt'))

        page.append((html.tag_h2('Inch Solutions')))
        th = []
        th.append(html.tag_th('Desired Pitch (tpi)'))
        th.append(html.tag_th('Actual Pitch (tpi)'))
        th.append(html.tag_th('Pitch Error'))
        th.append(html.tag_th('Configuration'))
        tr = []
        tr.append(html.tag_tr(html.indent('\n'.join(th))))
        for (i, pitch) in inch_solns:
            tr.append(html.tag_tr(gears_html(sets[i], pitch, 'inch')))
        table = html.tag_table(html.indent('\n'.join(tr)), 'border="1" cellpadding="5"')
        page.append(table)

        page.append((html.tag_h2('Metric Solutions')))
        th = []
        th.append(html.tag_th('Desired Pitch (mm)'))
        th.append(html.tag_th('Actual Pitch (mm)'))
        th.append(html.tag_th('Pitch Error'))
        th.append(html.tag_th('Configuration'))
        tr = []
        tr.append(html.tag_tr(html.indent('\n'.join(th))))
        for (i, pitch) in metric_solns:
            tr.append(html.tag_tr(gears_html(sets[i], pitch, 'metric')))
        table = html.tag_table(html.indent('\n'.join(tr)), 'border="1" cellpadding="5"')
        page.append(table)

        # build the body
        body = []
        # add the content
        body.append('\n'.join(page))
        body = html.tag_body(html.indent('\n'.join(body)))
        # build the head
        head = []
        head = html.tag_head(html.indent('\n'.join(head)))

        f = open(_ofile, 'w')
        f.write(html.tag_html(html.indent('\n'.join((head, body)))))
        f.close()


#------------------------------------------------------------------------------

main()

#------------------------------------------------------------------------------
