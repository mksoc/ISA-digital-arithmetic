#! /usr/bin/python3
import os
import datetime
from common.syn_script_gen import setup_param

# ==============================================================
# SET THESE VARIABLES BEFORE USING!!
REMOTE_ROOT = '/home/isa22/lab2'
repo_name = 'ISA-digital-arithmetic'
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


# get current working dir and set repo root path
cwd = os.getcwd()
repo_root = cwd[0:cwd.find(repo_name) + len(repo_name)]

# print welcome message
print("""# =================================================================
# *****************************************************************
# ****************** Welcome to the pynthesizer! ******************
# ************           {date}           ************
# *****************************************************************
# =================================================================\n""".format(date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

# ask for folder to save reports
log_folder = input(
    '\nType the name of the folder you want to put logs and reports into (will be created inside ../syn/): ')
with cd('{}/HW_filter/syn'.format(repo_root)):
    try:
        os.mkdir(log_folder)
        with cd(log_folder):
            os.mkdir('reports')
            os.mkdir('logs')
    except FileExistsError:
        pass

# open connection to server
USER_HOST = 'isa22@led-x3850-2.polito.it'
PORT = 10020
SSH_SOCKET = '~/.ssh/{}'.format(USER_HOST)
print('\nConnect to server.')
os.system(
    'ssh -M -f -N -o ControlPath={} -p {} {}'.format(SSH_SOCKET, PORT, USER_HOST))

# select synthesis or power report
print('\nDo you want to synthesize or do a power report?')
print('NOTE: power report can be done only after simulation has been performed on the sinthesized design. Please make sure that "iir_filter_back.saif" in your version folder is up to date.')
print('\t1) Synthesize design')
print('\t2) Do power report')
pow_syn_n = get_choice(range(1, 3)) - 1
print('\n')

if not pow_syn_n:
    # generate synthesis script
    with cd('{}/HW_filter/syn'.format(repo_root)):
        version = setup_param()

    # run initial commands on server
    print('\nClean server side syn folder')
    with open('ssh_commands.sh', 'w') as command_file:
        command_file.write("""cd {}
            rm -r syn/*""".format(REMOTE_ROOT))
    os.system(
        'cat ssh_commands.sh | ssh -S {} -p {} {}'.format(SSH_SOCKET, PORT, USER_HOST))
    os.remove('ssh_commands.sh')
else:
    # ask for version to use
    print('Which version do you wish to use?')
    version = get_choice(range(4))
    while not os.path.isfile('{}/HW_filter/version{}/iir_filter.vhd'.format(repo_root, version)):
        print('Entity for version {} is not defined (yet). Please choose another version.'.format(version))
        version = get_choice(range(4))

    # generate power report script
    with cd('{}/HW_filter/syn'.format(repo_root)):
        with open('py-power-script.tcl', 'w') as pow_script:
            pow_script.write("""# read netlist
read_verilog -netlist ../version{ver}/iir_filter.v 

# read switching activity
read_saif -input ../version{ver}/iir_filter_back.saif -instance iir_filterTB/UUT -unit ns -scale 1

# create clock
create_clock -name CLOCK clk
 
# report power
report_power > ./reports/power-report.txt""".format(ver=version))

# copy script and setup file to server
print('\nCopy scripts to server')
if not pow_syn_n:
    os.system('rsync -avz -e "ssh -o ControlPath={} -p {}" {}/HW_filter/syn/py-syn-script.tcl {}:{}/syn/'.format(
        SSH_SOCKET, PORT, repo_root, USER_HOST, REMOTE_ROOT))
    os.system('rsync -avz -e "ssh -o ControlPath={} -p {}" {}/HW_filter/syn/.synopsys_dc.setup {}:{}/syn/'.format(
        SSH_SOCKET, PORT, repo_root, USER_HOST, REMOTE_ROOT))
else:
    os.system('rsync -avz -e "ssh -o ControlPath={} -p {}" {}/HW_filter/syn/py-power-script.tcl {}:{}/syn/'.format(
        SSH_SOCKET, PORT, repo_root, USER_HOST, REMOTE_ROOT))

if not pow_syn_n:
    # run synthesis on server
    print('\nRun synthesis')
    with open('ssh_commands.sh', 'w') as command_file:
        command_file.write("""cd {root}/syn
            source /software/scripts/init_synopsys
            mkdir work logs reports saif netlist
            dc_shell-xg-t -f py-syn-script.tcl
            mv netlist/* ../version{ver}
            mv saif/NangateOpenCellLibrary.saif ../sim""".format(root=REMOTE_ROOT, ver=version))
    os.system(
        'cat ssh_commands.sh | ssh -S {} -p {} {}'.format(SSH_SOCKET, PORT, USER_HOST))
    os.remove('ssh_commands.sh')
else:
    print('\nExecute power report')
    with open('ssh_commands.sh', 'w') as command_file:
        command_file.write("""cd {root}/syn
            source /software/scripts/init_synopsys
            dc_shell-xg-t -f py-power-script.tcl""".format(root=REMOTE_ROOT))
    os.system(
        'cat ssh_commands.sh | ssh -S {} -p {} {}'.format(SSH_SOCKET, PORT, USER_HOST))
    os.remove('ssh_commands.sh')

# copy logs and reports
print('\nRetrieve logs and reports from server')
os.system('rsync -avz -e "ssh -o ControlPath={} -p {}" {}:{}/syn/reports/ {}/HW_filter/syn/{}/reports/'.format(
    SSH_SOCKET, PORT, USER_HOST, REMOTE_ROOT, repo_root, log_folder))
os.system('rsync -avz -e "ssh -o ControlPath={} -p {}" {}:{}/syn/logs/ {}/HW_filter/syn/{}/logs/'.format(
    SSH_SOCKET, PORT, USER_HOST, REMOTE_ROOT, repo_root, log_folder))

# close connection
print('\nClose connection.')
os.system('ssh -S {} -O exit {}'.format(SSH_SOCKET, USER_HOST))
