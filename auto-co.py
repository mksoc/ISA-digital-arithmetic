#! /usr/bin/python3
import os

# ==============================================================
# SET THESE VARIABLES BEFORE USING!!
REMOTE_ROOT = '/home/isa22/lab2'
# ==============================================================


# function declarations
def parse_dict():
    print('    {:30}{:15}{}'.format('LOCAL', '', 'REMOTE'))
    for key, value in ops_dict.items():
        local_dir = next(item for item in value.split(' ') if item.startswith('./'))
        remote_dir = next(item.split(':')[1] for item in value.split(' ') if ':' in item)
        print('{key:2}) {local:30}{arrow:15}{remote}'.format(
            key=key,
            local=local_dir,
            arrow='->' if '-r' in value.split(' ') else '<-',
            remote=remote_dir
            )
        )


# check if the script is run inside the root of the repository
assert os.getcwd().endswith(
    'ISA-digital-arithmetic'), 'Error: script must be run in the repository root directory'

# define constants
USER_HOST = 'isa22@led-x3850-2.polito.it'
PORT = '10020'
SSH_SOCKET = '~/.ssh/{}'.format(USER_HOST)

# define operations dictionary
to_cmd_str = 'scp -r -o ControlPath={socket} -P {port} ./{source} {login}:{remote_root}/{dest}'
from_cmd_str = 'scp -o ControlPath={socket} -P {port} {login}:{remote_root}/{source} ./{dest}'
ops_dict = {
    1: to_cmd_str.format(
        socket=SSH_SOCKET,
        port=PORT,
        login=USER_HOST,
        remote_root=REMOTE_ROOT,
        source='HW_filter/src',
        dest='' # destination is empty otherwise scp would copy into ../src/src/
    ),
    2: to_cmd_str.format(
        socket=SSH_SOCKET,
        port=PORT,
        login=USER_HOST,
        remote_root=REMOTE_ROOT,
        source='HW_filter/tb',
        dest=''
    ),
    3: to_cmd_str.format(
        socket=SSH_SOCKET,
        port=PORT,
        login=USER_HOST,
        remote_root=REMOTE_ROOT,
        source='HW_filter/sim/*.tcl',
        dest='sim'
    ),
    4: to_cmd_str.format(
        socket=SSH_SOCKET,
        port=PORT,
        login=USER_HOST,
        remote_root=REMOTE_ROOT,
        source='HW_filter/version{ver}',
        dest=''
    ),
    5: to_cmd_str.format(
        socket=SSH_SOCKET,
        port=PORT,
        login=USER_HOST,
        remote_root=REMOTE_ROOT,
        source='common/samples.txt',
        dest='common'
    ),
    6: from_cmd_str.format(
        socket=SSH_SOCKET,
        port=PORT,
        login=USER_HOST,
        remote_root=REMOTE_ROOT,
        source='common/results-hw.txt',
        dest='common'
    ),
}

# connect to server
print('\nConnect to server.')
os.system('ssh -M -f -N -o ControlPath={socket} -p {port} {login}'.format(
    socket=SSH_SOCKET,
    port=PORT,
    login=USER_HOST
))

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
            if op == 4:
                version = input('Which version do you need? Type 0-3 and press enter: ')
                while not os.path.isfile('HW_filter/version{}/iir_filter.vhd'.format(version)):
                    print('Entity for version {} is not defined (yet). Please choose another version.'.format(version))
                    version = input('Which version do you need? Type 0-3 and press enter: ')
                os.system(ops_dict[op].format(ver=version))
            else:
                os.system(ops_dict[op])

print('Quitting... bye bye!')
