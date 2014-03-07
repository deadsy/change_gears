# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
"""

html generation/output functions

"""
#------------------------------------------------------------------------------

def text_html(content):
    return 'Content-type: text/html\n\n%s\n' % content

def redirect(uri):
    return 'Location: %s\n' % uri

#------------------------------------------------------------------------------

def gen_tag1(tag, attrib):
    """generate a <tag attribute \> string"""
    if attrib:
        return '<%s %s />' % (tag, attrib)
    else:
        return '<%s />' % tag

def gen_tag2(tag, content, attrib):
    """generate a <tag attribute>content</tag> string"""
    if attrib:
        return '<%s %s>%s</%s>' % (tag, attrib, content, tag)
    else:
        return '<%s>%s</%s>' % (tag, content, tag)

def indent(s):
    items = s.split('\n')
    items.insert(0, '')
    items.append('')
    return '\n  '.join(items)[:-2]

#------------------------------------------------------------------------------
# <x> ... </x> tags

def tag_a(content, attrib = ''):
    return gen_tag2('a', content, attrib)

def tag_p(content, attrib = ''):
    return gen_tag2('p', content, attrib)

def tag_body(content, attrib = ''):
    return gen_tag2('body', content, attrib)

def tag_head(content, attrib = ''):
    return gen_tag2('head', content, attrib)

def tag_html(content, attrib = ''):
    return gen_tag2('html', content, attrib)

def tag_form(content, attrib = ''):
    return gen_tag2('form', content, attrib)

def tag_td(content, attrib = ''):
    return gen_tag2('td', content, attrib)

def tag_th(content, attrib = ''):
    return gen_tag2('th', content, attrib)

def tag_tr(content, attrib = ''):
    return gen_tag2('tr', content, attrib)

def tag_table(content, attrib = ''):
    return gen_tag2('table', content, attrib)

def tag_h1(content, attrib = ''):
    return gen_tag2('h1', content, attrib)

def tag_h2(content, attrib = ''):
    return gen_tag2('h2', content, attrib)

def tag_h3(content, attrib = ''):
    return gen_tag2('h3', content, attrib)

def tag_h4(content, attrib = ''):
    return gen_tag2('h4', content, attrib)

def tag_li(content, attrib = ''):
    return gen_tag2('li', content, attrib)

def tag_ul(content, attrib = ''):
    return gen_tag2('ul', content, attrib)

def tag_ol(content, attrib = ''):
    return gen_tag2('ol', content, attrib)

def tag_i(content, attrib = ''):
    return gen_tag2('i', content, attrib)

def tag_span(content, attrib = ''):
    return gen_tag2('span', content, attrib)

def tag_label(content, attrib = ''):
    return gen_tag2('label', content, attrib)

def tag_select(content, attrib = ''):
    return gen_tag2('select', content, attrib)

def tag_option(content, attrib = ''):
    return gen_tag2('option', content, attrib)

def tag_b(content, attrib = ''):
    return gen_tag2('b', content, attrib)

def tag_pre(content, attrib = ''):
    return gen_tag2('pre', content, attrib)

def tag_script(content, attrib = ''):
    return gen_tag2('script', content, attrib)

#------------------------------------------------------------------------------
# <x /> tags

def tag_br(attrib = ''):
    return gen_tag1('br', attrib)

def tag_input(attrib = ''):
    return gen_tag1('input', attrib)

def tag_hr(attrib = ''):
    return gen_tag1('hr', attrib)

#------------------------------------------------------------------------------
