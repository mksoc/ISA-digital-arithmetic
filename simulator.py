#! /usr/bin/python3
import os
import sys
from common.samples_generator import gen_samples
from common.compare_outputs import compare

# ==============================================================
# SET THESE VARIABLES BEFORE USING!!
REMOTE_ROOT = '/home/isa22/lab1'
MSIM_COMMAND = '. /home/marco/.local/bin/init_msim_ase'
# ==============================================================


# class definitions
class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


# functions definitions
def get_choice(choices):
    try:
        choice = int(
            input('Type the number corresponding to your choice and press enter: '))
    except ValueError:
        print('Error. Invalid option. Try again.')
        choice = get_choice(choices)
    else:
        if (choice - 1) not in choices:
            print('Error. Invalid option. Try again.')
            choice = get_choice(choices)
    return choice

# ====================================== main execution starts here ======================================
# check if the script is run inside the root of the repository
if not os.getcwd().endswith('ISA-digital-arithmetic'):
    print('Error: script must be run in the repository root directory')
    sys.exit(1)

# ask for where to run simulation
print('Do you wish to run the simulation locally or on the remote server?')
print('\t1) Locally')
print('\t2) Remote server')
run_remote = get_choice(range(2)) - 1

if run_remote:
    print('Running locally...')
else:
    print('Running on the remote server...')
    USER_HOST = 'isa22@led-x3850-2.polito.it'
    PORT = 10020
    SSH_SOCKET = '~/.ssh/{}'.format(USER_HOST)

# check if there are samples available
# otherwise ask to create new ones or keep old ones
if os.path.isfile('common/samples.txt'):
    print('\nA "samples.txt" file was found. Do you want to use those samples or to generate new ones?')
    print('\t1) Use already existing samples')
    print('\t2) Generate new ones')

    gen_new_samples = get_choice(range(2)) - 1
    if gen_new_samples:
        with cd('common'):
            gen_samples()
            os.rename('py-samples.txt', 'samples.txt')
else:
    print('No "samples.txt" file found. Will generate new samples.')
    with cd('common'):
        gen_samples()
        os.rename('py-samples.txt', 'samples.txt')

# compile C model if not already there and run it
with cd('C_filter'):
    C_EX_NAME = 'iir_filter.o'
    if not os.path.isfile(C_EX_NAME):
        print('\nNo executable for C model found. Will compile C file.')
        os.system('g++ iir_filter.c -o {}'.format(C_EX_NAME))
    print('\nRun C model on selected samples.')
    os.system('./{} ../common/samples.txt ../common/results-c.txt'.format(C_EX_NAME))

# copy files to server if needed
if run_remote:
    print('\nConnect to server.')
    os.system('ssh -M -f -N -o ControlPath={} -p {} {}}'.format(SSH_SOCKET, PORT, USER_HOST))
    print('\nCopy samples to server.')
    os.system('scp -o ControlPath={} -P {} common/samples.txt {}:{}/common'.format(SSH_SOCKET, PORT, USER_HOST, REMOTE_ROOT))

# ask for design to simulate and run simulation
print('\nSelect design to simulate.')
print('\t1) Original VHDL architecture')
print('\t2) Post-synthesis netlist')
design_choice = get_choice(range(2))
if design_choice == 1:
    DESIGN_VAR = 'arch'
elif design_choice == 2:
    DESIGN_VAR = 'postsyn'

print('\nRun simulation.')
if run_remote:
    os.system("""ssh -S {} -p {} {} /bin/bash << EOF
            cd {}/sim
            source /software/scripts/init_msim6.2g
            export SIM_MODE="no-gui"
            export SIM_DESIGN={}
            vsim -c -do sim-script.tcl
        EOF""".format(SSH_SOCKET, PORT, USER_HOST, REMOTE_ROOT, DESIGN_VAR))

    print('\nCopy results from server.')
    os.system('scp -o ControlPath={} -P {} {}:{}/common/results-hw.txt common/'.format(SSH_SOCKET, PORT, USER_HOST, REMOTE_ROOT))

    print('\nClose connection.')
    os.system('ssh -S {} -O exit {}'.format(SSH_SOCKET, USER_HOST))
else:
    with cd('HW_filter/sim'):
        os.system('{}'.format(MSIM_COMMAND))
        os.environ['SIM_MODE'] = 'no-gui'
        os.environ['SIM_DESIGN'] = DESIGN_VAR
        os.system('vsim -c -do sim-script.tcl')

# compare results
with cd('common'):
    compare('results-c.txt', 'results-hw.txt')
