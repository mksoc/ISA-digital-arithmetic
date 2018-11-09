#! /usr/bin/python3
import os
import subprocess
from common.samples_generator import gen_samples
from common.compare_outputs import compare
from common.sim_script_gen import gen_tcl

# ==============================================================
# SET THESE VARIABLES BEFORE USING!!
REMOTE_ROOT = '/home/isa22/lab2'
MSIM_INIT_PATH = '/home/marco/.local/bin/init_msim_ase'
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
        if choice not in choices:
            print('Error. Invalid option. Try again.')
            choice = get_choice(choices)
    return choice


def bash_source(file):
    if os.path.isfile(file):
        command = 'sh -c ". {} && env"'.format(file)
        for line in subprocess.getoutput(command).split('\n'):
            if line.startswith('PATH'):
                key, value = line.split('=')
                os.environ[key] = value
    else:
        raise FileNotFoundError('File "{}" not found'.format(file))


# ====================================== main execution starts here ======================================
# check if the script is run inside the root of the repository
assert os.getcwd().endswith(
    'ISA-digital-arithmetic'), 'Error: script must be run in the repository root directory'

# ask for where to run simulation
print('Do you wish to run the simulation locally or on the remote server?')
print('\t1) Locally')
print('\t2) Remote server')
run_remote = get_choice(range(1, 3)) - 1

if not run_remote:
    print('Running locally...')
else:
    print('Running on the remote server...')
    USER_HOST = 'isa22@led-x3850-2.polito.it'
    PORT = 10020
    SSH_SOCKET = '~/.ssh/{}'.format(USER_HOST)
    print('\nConnect to server.')
    os.system(
        'ssh -M -f -N -o ControlPath={} -p {} {}'.format(SSH_SOCKET, PORT, USER_HOST))

# check if there are samples available
# otherwise ask to create new ones or keep old ones
if os.path.isfile('common/samples.txt'):
    print('\nA "samples.txt" file was found. Do you want to use those samples or to generate new ones?')
    print('\t1) Use already existing samples')
    print('\t2) Generate new ones')

    if get_choice(range(1, 3)) - 1:
        with cd('common'):
            gen_samples()
            os.rename('py-samples.txt', 'samples.txt')
else:
    print('No "samples.txt" file found. Will generate new samples.')
    with cd('common'):
        gen_samples()
        os.rename('py-samples.txt', 'samples.txt')

if run_remote:
    print('\nCopy samples to server.')
    os.system('rsync -avz -e "ssh -o ControlPath={} -p {}" common/samples.txt {}:{}/common/'.format(
        SSH_SOCKET, PORT, USER_HOST, REMOTE_ROOT))

# compile C model if not already there and run it
with cd('C_filter'):
    C_EX_NAME = 'iir_filter.o'
    if not os.path.isfile(C_EX_NAME):
        print('\nNo executable for C model found. Will compile C file.')
        os.system('g++ iir_filter.c -o {}'.format(C_EX_NAME))
    print('\nRun C model on selected samples.')
    os.system('./{} ../common/samples.txt ../common/results-c.txt'.format(C_EX_NAME))

# ask for version to use
print('\nWhich version do you wish to use?')
version = get_choice(range(4))
while not os.path.isfile('HW_filter/version{}/iir_filter.vhd'.format(version)):
    print('Entity for version {} is not defined (yet). Please choose another version.'.format(version))
    version = get_choice(range(4))

# ask for design to simulate
print('\nSelect design to simulate.')
print('\t1) Original VHDL architecture')
print('\t2) Post-synthesis netlist')
design_choice = get_choice(range(1, 3))
if design_choice == 2:
    while not os.path.isfile('HW_filter/version{}/iir_filter.v'.format(version)):
        print('Post-synthesis netlist for version {} was not found. Please use original VHDL or press Ctrl+C to exit simulator.'.format(version))
        design_choice = get_choice(range(1, 3))

# generate script for simulation
with cd('HW_filter/sim'):
    print('\nGenerate TCL script for simulation.')
    gen_tcl(run_remote, 1, version, design_choice)
    if run_remote:
        print('\nCopy script to server.')
        os.system('rsync -avz -e "ssh -o ControlPath={} -p {}" py-sim-script.tcl {}:{}/sim/'.format(
            SSH_SOCKET, PORT, USER_HOST, REMOTE_ROOT))

# run simulation
print('\nRun simulation.')
if run_remote:
    with open('ssh_commands.sh', 'w') as command_file: 
        command_file.write("""cd {}/sim
            source /software/scripts/init_msim6.2g
            if [ ! -d work ]; then vlib work; fi
            vsim -c -do py-sim-script.tcl""".format(REMOTE_ROOT))
    os.system('cat ssh_commands.sh | ssh -S {} -p {} {}'.format(SSH_SOCKET, PORT, USER_HOST))
    os.remove('ssh_commands.sh')

    print('\nCopy results from server.')
    os.system('scp -o ControlPath={} -P {} {}:{}/common/results-hw.txt common/'.format(
        SSH_SOCKET, PORT, USER_HOST, REMOTE_ROOT))

    print('\nClose connection.')
    os.system('ssh -S {} -O exit {}'.format(SSH_SOCKET, USER_HOST))
else:
    with cd('HW_filter/sim'):
        try:
            bash_source(MSIM_INIT_PATH)
        except FileNotFoundError as e:
            raise type(e)('The simulation could not run locally, because the Modelsim executable was not found in PATH. \nPlease check that you set the correct path inside this script and try again.') from e
        else:
            os.system('vsim -c -do ../../common/py-sim-script.tcl')

# compare results
with cd('common'):
    compare('results-c.txt', 'results-hw.txt')
