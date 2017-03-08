#!python2
# -*- coding: utf-8 -*-

import os.path
import re

from py3status.docstrings import core_module_docstrings, find_screenshots
from py3status.screenshots import get_samples

def fix(lines):
    out = []
    code = False
    for line in lines:
        if line.strip() == '```':
            code = not code
            space = ' ' * (len(line.rstrip()) - 3)
            if code:
                out.append('\n\n%s.. code-block:: none\n\n' % space)
            else:
                out.append('\n')
        else:
            if code and line.strip():
                line = '    ' + line
            out.append(line)
    return out


def file_sort(my_list):
    """
    Sort a list in a nice way.
    """
    def convert(text):
        return int(text) if text.isdigit() else text

    def alphanum_key(key):
        # remove extension
        key = key.rsplit('.', 1)[0]
        return [convert(c) for c in re.split('([0-9]+)', key)]

    my_list.sort(key=alphanum_key)
    return my_list


def screenshots(screenshots_data, module_name):
    """
    Create markdown output for any screenshots a module may have.
    """
    shots = screenshots_data.get(module_name)
    if not shots:
        return('')

    out = []
    for shot in file_sort(shots):
        if not os.path.exists('../doc/screenshots/%s.png' % shot):
            continue
        out.append(
                u'\n.. image:: screenshots/{}.png\n\n'.format(shot)
        )
    return u''.join(out)


def create_readme(data):
    '''
    Create README.md text for the given module data.
    '''

    # get screenshot data
    screenshots_data = {}
    samples = get_samples()
    for sample in samples.keys():
        module = sample.split('-')[0]
        if module not in screenshots_data:
            screenshots_data[module] = []
        screenshots_data[module].append(sample)

    out = []
    # details
    for module in sorted(data.keys()):
        out.append(
            '\n{name}\n{underline}\n\n{screenshots}{details}\n'.format(
                name=module,
                screenshots=screenshots(screenshots_data, module),
                underline='-' * len(module),
                details=''.join(fix(data[module])).strip()))
    return ''.join(out)

with open('../doc/modules-info.rst', 'w') as f:
    f.write(create_readme(core_module_docstrings(format='rst')))
