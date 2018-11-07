#! /usr/bin/python3
import datetime


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


# ask for where to run simulation
print('Do you wish to run the simulation locally or on the remote server?')
print('\t1) Locally')
print('\t2) Remote server')
run_remote = get_choice(range(2)) - 1

# ask if the user wants the GUI or not
print('Do you wish to run the simulation using the GUI or the command line?')
print('Note: waves are only available when using the GUI.')
print('\t1) GUI')
print('\t2) Command line')
cli_mode = get_choice(range(2)) - 1

# ask for version to usesimulate
print('\nWhich version do you wish to use?')
version = get_choice(range(4))

# ask for design to simulate
print('\nWhich design do you wish to simulate?')
print('\t1) Original VHDL architecture')
print('\t2) Post-synthesis netlist')
design_choice = get_choice(range(2))

# generate TCL script
print('Generating TCL script...')
with open('py-sim-script.tcl', 'w') as script_file:
    script_file.write("""# =================================================================
# *****************************************************************
# ************ GENERATED USING sim_script_generator.py ************
# ************           {}           ************
# *****************************************************************
# =================================================================\n""".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    if cli_mode:
        script_file.write('\nputs "Running in command line mode. No waveforms will be available."')
    else:
        script_file.write('\nputs "Running in GUI mode."')

    script_file.write('\n\n# compile source files')
    script_file.write('\nvcom -93 -work ./work ../src/{}.vhd'.format('*' if design_choice == 1 else 'filter_pkg'))
    script_file.write('\nvcom -93 -work ./work ../version{}/*.{}'.format(version, 'vhd' if design_choice == 1 else 'v'))

    script_file.write('\n\n# compile testbench')
    script_file.write('\nvcom -93 -work ./work ../tb/*.vhd')
    if cli_mode:
        script_file.write('\nvlog -work ./work +define{}+NO_GUI=1 ../tb/iir_filterTB.v'.format('' if design_choice == 1 else '+SYN=1'))
    else:
        script_file.write('\nvlog -work ./work {} ../tb/iir_filterTB.v'.format('' if cli_mode else '+define+SYN=1'))

    script_file.write('\n\n# load design')
    script_file.write('\nvsim {} work.iir_filterTB'.format('' if design_choice == 1 else '-L /software/dk/nangate45/verilog/msim6.2g -sdftyp /iir_filterTB/UUT=../netlist/iir_filter.sdf -pli /software/synopsys/syn_current/auxx/syn/power/vpower/lib-linux/libvpower.so'))

print('Done.')