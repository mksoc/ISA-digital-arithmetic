#! /usr/bin/python3
import os
import datetime
from common.syn_script_gen import setup_param
from common import isa

# ==============================================================
# SET THESE VARIABLES BEFORE USING!!
remote_root = '/home/isa22/lab2'
# ==============================================================

# set repo root path
repo_root = isa.get_root('ISA-digital-arithmetic')

# print welcome message
print("""# =================================================================
# *****************************************************************
# ****************** Welcome to the pynthesizer! ******************
# ************           {date}           ************
# *****************************************************************
# =================================================================\n""".format(date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

# ask for folder to save reports
print('Which folder do you want to put logs and reports into?')
subfolders = sorted([f.name for f in os.scandir('{}/HW_filter/syn'.format(repo_root)) if f.is_dir()])
log_folder = isa.get_choice(subfolders, 'Choose from the numbers below (if any) or type the name (will be created inside ../syn/): ', str_val=True)
if type(log_folder).__name__ == 'int':
    log_folder = subfolders[log_folder - 1]
print(log_folder)

with isa.cd('{}/HW_filter/syn'.format(repo_root)):
    try:
        os.mkdir(log_folder)
        with isa.cd(log_folder):
            os.mkdir('reports')
            os.mkdir('logs')
    except FileExistsError:
        pass

# open connection to server
session = isa.ssh_session('isa22', 'led-x3850-2.polito.it', 10020)

# select synthesis or power report
print('\nDo you want to synthesize or do a power report?')
print('NOTE: power report can be done only after simulation has been performed on the sinthesized design. Please make sure that "iir_filter_back.saif" in your version folder is up to date.')
pow_syn_n = isa.get_choice(['Synthesize design', 'Do power report']) - 1

if not pow_syn_n:
    # generate synthesis script
    with isa.cd('{}/HW_filter/syn'.format(repo_root)):
        version = setup_param()

    # run initial commands on server
    print('\nClean server side syn folder')
    session.run_commands("""cd {}
            rm -r syn/*""".format(remote_root))

else:
    # ask for version to use
    version = isa.ask_version('{}/HW_filter'.format(repo_root), 'iir_filter.vhd')

    # generate power report script
    with isa.cd('{}/HW_filter/syn'.format(repo_root)):
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
    session.copy_to('{}/HW_filter/syn/py-syn-script.tcl'.format(repo_root), '{}/syn/'.format(remote_root))
    session.copy_to('{}/HW_filter/syn/.synopsys_dc.setup'.format(repo_root), '{}/syn/'.format(remote_root))
else:
    session.copy_to('{}/HW_filter/syn/py-power-script.tcl'.format(repo_root), '{}/syn/'.format(remote_root))

if not pow_syn_n:
    # run synthesis on server
    print('\nRun synthesis')
    session.run_commands("""cd {root}/syn
            source /software/scripts/init_synopsys
            mkdir work logs reports saif netlist
            dc_shell-xg-t -f py-syn-script.tcl
            mv netlist/* ../version{ver}
            mv saif/NangateOpenCellLibrary.saif ../sim""".format(root=remote_root, ver=version))
else:
    print('\nExecute power report')
    session.run_commands("""cd {root}/syn
            source /software/scripts/init_synopsys
            dc_shell-xg-t -f py-power-script.tcl""".format(root=remote_root))

# copy logs and reports
print('\nRetrieve logs and reports from server')
session.copy_from('{}/syn/reports/'.format(remote_root), '{}/HW_filter/syn/{}/reports/'.format(repo_root, log_folder))
session.copy_from('{}/syn/logs/'.format(remote_root), '{}/HW_filter/syn/{}/logs/'.format(repo_root, log_folder))
