#! /usr/bin/python3
import os
import subprocess
import shlex
import datetime
from common.samples_generator import gen_samples
from common.compare_outputs import compare
from common.sim_script_gen import gen_tcl
from common import isa

# ==============================================================
# SET THESE VARIABLES BEFORE USING!!
remote_root = '/home/isa22/lab2'
msim_init_path = '/home/marco/.local/bin/init_msim_ase'
# ==============================================================

# set repo root path
repo_root = isa.get_root('ISA-digital-arithmetic')

# print welcome message
print("""# =================================================================
# *****************************************************************
# ******************* Welcome to the simulator! *******************
# ************           {date}           ************
# *****************************************************************
# =================================================================\n""".format(date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

# ask for where to run simulation
print('Do you wish to run the simulation locally or on the remote server?')
run_remote = isa.get_choice(['Locally', 'Remote server']) - 1

if not run_remote:
    print('Running locally...')
else:
    print('Running on the remote server...')
    session = isa.ssh_session('isa22', 'led-x3850-2.polito.it', 10020)

# check if there are samples available
# otherwise ask to create new ones or keep old ones
if os.path.isfile('{}/common/samples.txt'.format(repo_root)):
    print('\nA "samples.txt" file was found. Do you want to use those samples or to generate new ones?')
    generate = isa.get_choice(['Use already existing samples', 'Generate new ones']) - 1
else:
    print('No "samples.txt" file found. Will generate new samples.')
    generate = True

if generate:
    with isa.cd('{}/common'.format(repo_root)):
        gen_samples()
        os.rename('py-samples.txt', 'samples.txt')

if run_remote:
    print('\nCopy samples to server.')
    session.copy_to('{}/common/samples.txt'.format(repo_root), '{}/common/'.format(remote_root))

# compile C model if not already there and run it
with isa.cd('{}/C_filter'.format(repo_root)):
    c_exe_name = 'iir_filter.o'
    if not os.path.isfile(c_exe_name):
        print('\nNo executable for C model found. Will compile C file.')
        os.system('g++ iir_filter.c -o {}'.format(c_exe_name))
    print('\nRun C model on selected samples.')
    os.system('./{} ../common/samples.txt ../common/results-c.txt'.format(c_exe_name))
    print()

# ask for version to use
version = isa.ask_version('{}/HW_filter'.format(repo_root), 'iir_filter.vhd')

# ask for design to simulate
if run_remote:
    print('\nSelect design to simulate.')
    design_choice = isa.get_choice(['Original VHDL architecture', 'Post-synthesis netlist'])
    if design_choice == 2:
        file_check = '{ssh} test -e {rem_root}/version{ver}/iir_filter.v'.format(ssh=session.get_param(), rem_root=remote_root, ver=version)
        while not (subprocess.call(shlex.split(file_check)) == 0):
            print('Post-synthesis netlist for version {} was not found. Please use original VHDL or press Ctrl+C to exit simulator.'.format(version))
            design_choice = isa.get_choice(['Original VHDL architecture', 'Post-synthesis netlist'], print_menu=False)
else:
    design_choice = 1

# generate script for simulation
with isa.cd('{}/HW_filter/sim'.format(repo_root)):
    print('\nGenerate TCL script for simulation.')
    gen_tcl(run_remote, 1, version, design_choice)
    if run_remote:
        print('\nCopy script to server.')
        session.copy_to('{}/HW_filter/sim/py-sim-script.tcl'.format(repo_root), '{}/sim/'.format(remote_root))

# run simulation
print('\nRun simulation.')
if run_remote:
    session.run_commands("""cd {root}/sim
        source /software/scripts/init_msim6.2g
        if [ ! -d work ]; then vlib work; fi
        vsim -c -do py-sim-script.tcl
        mv iir_filter_back.saif ../version{ver}""".format(root=remote_root, ver=version))

    print('\nCopy results from server.')
    session.copy_from('{}/common/results-hw.txt'.format(remote_root), '{}/common/'.format(repo_root))
else:
    with isa.cd('{}/HW_filter/sim'.format(repo_root)):
        try:
            isa.bash_source(msim_init_path)
        except FileNotFoundError as e:
            raise type(e)('The simulation could not run locally, because the Modelsim executable was not found in PATH. \nPlease check that you set the correct path inside this script and try again.') from e
        else:
            os.system('vsim -c -do py-sim-script.tcl')

# compare results
with isa.cd('{}/common'.format(repo_root)):
    compare('results-c.txt', 'results-hw.txt')
