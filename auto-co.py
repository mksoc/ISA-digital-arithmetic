#! /usr/bin/python3
from common import isa

# ==============================================================
# SET THESE VARIABLES BEFORE USING!!
remote_root = '/home/isa22/lab2'
# ==============================================================


# function declarations
def parse_dict():
    print('    {:30}{:15}{}'.format('LOCAL', '', 'REMOTE'))
    for key, value in ops_dict.items():
        if value[2] == 'to':
            print('{key:2}) {local:30}{arrow:15}{root}/{remote}'.format(
                key=key,
                local=value[0],
                arrow='->',
                root=remote_root,
                remote=value[1] if value[1] else value[0].split('/')[-1]
            ))
        elif value[2] == 'from':
            print('{key:2}) {local:30}{arrow:15}{root}/{remote}'.format(
                key=key,
                local=value[1] if value[1] else value[0].split('/')[-1],
                arrow='<-',
                root=remote_root,
                remote=value[0]
            ))


# set repo root path
repo_root = isa.get_root('ISA-digital-arithmetic')

# define operations dictionary
ops_dict = {
    1: ('HW_filter/src', '', 'to'),  # destination is empty otherwise scp would copy into ../src/src/
    2: ('HW_filter/tb', '', 'to'),
    3: ('HW_filter/sim/*.tcl', 'sim/', 'to'),
    4: ('HW_filter/version{ver}', '', 'to'),
    5: ('common/samples.txt', 'common/', 'to'),
    6: ('common/results-hw.txt', 'common/', 'from'),
}

# connect to server
session = isa.ssh_session('isa22', 'led-x3850-2.polito.it', 10020)

# start infinite loop
end_loop = False
while not end_loop:
    # print welcome message
    print('This script provides automatic copy in many different ways:')
    parse_dict()

    ops = input('Type all numbers you want to execute (separated by space) and/or "q" to quit and press enter: ').split(' ')

    for op in ops:
        if op == 'q':
            end_loop = True
        else:
            op = int(op)
            if 'version' in ops_dict[op][0]:
                version = isa.ask_version('{}/HW_filter'.format(repo_root), 'iir_filter.vhd')
                if ops_dict[op][2] == 'to':
                    session.copy_to(ops_dict[op][0].format(ver=version), '{}/{}'.format(remote_root, ops_dict[op][1]))
                elif ops_dict[op][2] == 'from':
                    session.copy_from('{}/{}'.format(remote_root, ops_dict[op][0].format(ver=version)), ops_dict[op][1])
            else:
                if ops_dict[op][2] == 'to':
                    session.copy_to(ops_dict[op][0], '{}/{}'.format(remote_root, ops_dict[op][1]))
                elif ops_dict[op][2] == 'from':
                    session.copy_from('{}/{}'.format(remote_root, ops_dict[op][0]), ops_dict[op][1])

print('\nQuitting... bye bye!')
