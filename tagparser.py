from functools import reduce

class Records:
    def __init__(self):
        self.record_list = []
    def add(self, line1, line2):
        self.record_list.append((line1, line2))


class PairedTagsAccumulator:
    def __init__(self, open_tag, close_tag):
        self.records = {}
        self.matches = {}
        self.open_tag = open_tag
        self.close_tag = close_tag

    def get_result(self):
        return self.records

    def accumulate(self, name, line):
        if not name in self.records:
            self.records[name] = Records()
            
        if line.find(self.open_tag) >= 0:
            # Update current open line to the latest one
            self.matches[name] = line

        elif line.find(self.close_tag) >= 0:
            if name in self.matches:
                self.records[name].add(self.matches[name], line)
                self.matches[name] = ''


class TimedValues:
    def __init__(self):
        self.time = 0.0
        self.values = []

SECOND = '(ms)'
PAIR_START_POS = 3
EQUAL_SIGN = '='

def get_time(line):
    pos = line.find(SECOND)
    if pos:
        return float(line[:pos].strip())
    else:
        return 0.0

def get_values(line):
    return list(map(lambda x: float(x[x.find(EQUAL_SIGN) + 1:].strip()),
                   line.split(':')[PAIR_START_POS:]))
    
def calculate_time_delta(p):
    (str1, str2) = p
    tv = TimedValues()
    tv.time = get_time(str2) - get_time(str1)
    tv.values = get_values(str1)
    return tv


def get_time_value(p):
    (str1, str2) = p
    tv = TimedValues()
    tv.time = get_time(str1)
    tv.values = get_values(str1)
    return tv


def format_values(info):
    vstr = ''
    for v in info.values:
        vstr += '\t' + str(v)
    return str(info.time) + vstr


def write_matrix_header(f, name, row_num, col_num):
    if f and name and row_num and col_num:
        f.write('# name: ' + name + '\n')
        f.write('# type: matrix\n')
        f.write('# rows: ' + str(row_num) + '\n')
        f.write('# columns: ' + str(col_num) + '\n')


def write_scalar(f, name, val):
    if f and name and val:
        f.write('# name: ' + name + '\n')
        f.write('# type: scalar\n')
        f.write(str(val) + '\n')
        f.write('\n')


def write_string_list(f, lst):
    if f and lst:
        for s in lst:
            f.write(s + '\n')
    f.write('\n')


if __name__ == '__main__':
    tag_lines = ['000 (ms): foo : Begin : amount = 1 : amount1 = 10000',
                 '001 (ms): bar : Begin : amount = 2 : amount1 = 10000',
                 '002 (ms): bar : End : amount = 2 : amount1 = 10000',
                 '003 (ms): foo : End : amount = 1 : amount1 = 10000',
                 '006 (ms): foo : Begin : amount = 3 : amount1 = 10000',
                 '008 (ms): bar : Begin : amount = 4 : amount1 = 10000',
                 '009 (ms): bar : End : amount = 4 : amount1 = 10000',
                 '012 (ms): foo : End : amount = 3 : amount1 = 10000']
    accu = PairedTagsAccumulator('Begin', 'End')
    for l in tag_lines:
        accu.accumulate(l.split(':')[1].strip(), l)
    results = accu.get_result()
    with open('out.m', 'w') as out_file:
        for name in results:
            l1 = list(map(calculate_time_delta, results[name].record_list))
            write_scalar(out_file, name + '_total', reduce(lambda x, acc: x + acc.time, l1, 0.0))
            p = list(map(format_values, l1))
            write_matrix_header(out_file, name + '_delta', len(l1), len(l1[0].values) + 1)
            write_string_list(out_file, p)
            

 

        
 
