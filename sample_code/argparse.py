
from optparse import OptionParser

#python3 sample_code/argparse.py -y 2016 -c 2 -d
parser = OptionParser()

parser.add_option(
    '-d', '--day',
    action = 'store_true',
    dest = 'day_switch',
    help = 'day mode on'
)

parser.add_option(
    '-y', '--year',
    action = 'store',
    type = 'str',           # 型指定
    dest = 'year',     # 保存先変数名
)

parser.add_option(
    '-c', '--cours',
    action = 'store',
    type = 'str',           # 型指定
    dest = 'cours',     # 保存先変数名
)

parser.set_defaults(
    year = 2016,
    cours_id = 2,
    day_switch = False
)

options, args = parser.parse_args()

print(options.day_switch)
print(options.year)
print(options.cours)