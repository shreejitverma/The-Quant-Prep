#
# Script to Convert Jupyter Notebook
# to IPython Style Text File
#
# (c) The Python Quants GmbH
# WORK IN PROGRESS | DRAFT VERSION
# FOR ILLUSTRATION PURPOSES ONLY
import re
import os
import sys
import json

ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')


def parse(argv):
    if len(argv) < 1:
        raise ValueError('Please provide a file')
    path = argv[0]

    if not os.path.isfile(path):
        raise ValueError('Can not open %s. No such file or directory.' % path)

    parts = path.split('.')
    if len(parts) < 2 or len(parts) > 2 or parts[1] != 'ipynb':
        raise ValueError('Invalid filename')
    target = parts[0] + '.' + 'txt'

    notebook = read_in(argv[0])

    with open(target, 'w') as target_file:
        for cell in notebook['cells']:
            if cell['cell_type'] == 'raw':
                for l in cell['source']:
                    target_file.write(l)
                if l.startswith('# end'):
                    target_file.write('\n\n')
                else:
                    target_file.write('\n')

            if cell['cell_type'] == 'code':
                if 'execution_count' in cell:
                    execution_count = cell['execution_count']
                else:
                    execution_count = ""
                prefix = 'In [%s]: ' % execution_count
                len_prefix = len(prefix)
                code = ''
                first = 0
                for line in cell['source']:
                    code = code + ' ' * len_prefix * first + line
                    first = 1
                text_input = prefix + code
                target_file.write(text_input)
                if cell['outputs']:
                    target_file.write('\n')
                else:
                    target_file.write('\n\n')

                for output in cell['outputs']:
                    if 'execution_count' in output:
                        execution_count = output['execution_count']
                    else:
                        execution_count = ''
                    suffix = 'Out[%s]: ' % execution_count
                    len_suffix = len(suffix)
                    if 'data' in output and 'text/plain' in output['data'] \
                            and 'image/png' not in output['data']:
                        result = ""
                        first = 0
                        lb = 0
                        for line in output['data']['text/plain']:
                            add_lines = list()
                            if len(line) + len_suffix <= 81:
                                add_lines.append(line)
                            else:
                                add_lines = break_long_lines(line, len_suffix)
                            for l in add_lines:
                                if len(add_lines) >= 2:
                                    lb = 1
                                result += (' ' * len_suffix * first + l +
                                           lb * '\n')
                                first = 1
                            if len(add_lines) == 2:
                                result = result[:-1]
                        text_output = suffix + result
                        target_file.write(text_output)
                        target_file.write('\n\n')

                    if 'name' in output:
                        result = ""
                        first = 0
                        result = ""
                        first = 0
                        lb = 0
                        for line in output['text']:
                            add_lines = list()
                            if len(line) + len_suffix <= 81:
                                add_lines.append(line)
                            else:
                                add_lines = break_long_lines(line, len_suffix)
                                lb = 1
                            for l in add_lines:
                                result += ' ' * (len_prefix + 0) * \
                                    first + l + lb * '\n'
                                first = 1
                            if len(add_lines) == 2:
                                result = result[:-1]
                            lb = 0

                        text_output = (len_prefix + 0) * ' ' + result
                        target_file.write(text_output)
                        target_file.write('\n')

                    if 'ename' in output:
                        result = ""
                        first = 0
                        target_file.write('\n')
                        for line in output['traceback']:
                            line = ansi_escape.sub('', line)
                            result = (result + ' ' * len_prefix * first +
                                      line + '\n')
                            first = 1
                        text_output = len_prefix * ' ' + result
                        target_file.write(text_output)
                        target_file.write('\n')


def break_long_lines(line, len_suffix):
    comma = False
    # line.replace('\n', '')
    if line[len_suffix + 1:].find(' ') >= 0:
        line_parts = line.split(' ')
    elif line[len_suffix + 1:].find(',') >= 0:
        line_parts = line.split(',')
        comma = True
    else:
        line_parts = [line[start:start + 70] for
                      start in range(0, len(line) + 1, 70)]
    p_line = ''
    lines = list()
    splitter = ',' if comma else ' '
    for l in line_parts:
        if len(p_line) + len(l) + len_suffix < 81:
            if len(p_line) == 0:
                p_line = l
            else:
                p_line = p_line + splitter + l
        else:
            lines.append(p_line + splitter)
            p_line = splitter + l
    lines.append(p_line)
    return lines


def read_in(path):
    with open(path, 'r') as f:
        notebook = f.read()

    notebook = json.loads(notebook)
    return notebook


if __name__ == '__main__':
    parse(sys.argv[1:])
    import os
    fn = sys.argv[1].split('.')[0] + '.txt'
    os.rename(fn, fn + '~')
    with open(fn + '~', 'r') as f:
        with open(fn, 'w') as o:
            for line in f:
                if line.find('# plt.save') >= 0:
                    pass
                else:
                    o.write(line)
#    os.remove(sys.argv[2] + '~')
