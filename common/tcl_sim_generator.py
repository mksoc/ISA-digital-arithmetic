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
        if choice not in choices:
            print('Error. Invalid option. Try again.')
            choice = get_choice(choices)
    return choice


def gen_tcl(run_remote, cli_mode, version, design):
    print('Generating TCL script...')
    with open('py-sim-script.tcl', 'w') as script_file:
        script_file.write("""# =================================================================
# *****************************************************************
# ************ GENERATED USING sim_script_generator.py ************
# ************           {date}           ************
# *****************************************************************
# The script was generated starting from these values of variables:
# run_remote = {remote}
# cli_mode = {cli}
# version = {ver}
# design = {des}
# =================================================================\n""".format(
            date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            remote=run_remote,
            cli=cli_mode,
            ver=version,
            des=design
        ))

        script_file.write('\n{}'.format('puts "Running in command line mode. No waveforms will be available."' if cli_mode else 'puts "Running in GUI mode."'))

        script_file.write('\n\n# compile source files')
        script_file.write(
            '\nvcom -93 -work ./work ../src/{}.vhd'.format('*' if design == 1 else 'filter_pkg'
        ))
        script_file.write('\nvcom -93 -work ./work ../version{ver}/*.{ext}'.format(
            ver=version, 
            ext='vhd' if design == 1 else 'v'
        ))

        script_file.write('\n\n# compile testbench')
        script_file.write('\nvcom -93 -work ./work ../tb/*.vhd')
        script_file.write('\nvlog -work ./work {define}{syn}{no_gui} ../tb/iir_filterTB.v'.format(
            define='+define' if (cli_mode or design == 2) else '',
            syn='+SYN=1' if design == 2 else '',
            no_gui='+NO_GUI=1' if cli_mode else ''
        ))

        script_file.write('\n\n# load design')
        script_file.write('\nvsim {library} {in_path} {out_path} work.iir_filterTB'.format(
            library='' if design == 1 else '-L /software/dk/nangate45/verilog/msim6.2g -sdftyp /iir_filterTB/UUT=../netlist/iir_filter.sdf -pli /software/synopsys/syn_current/auxx/syn/power/vpower/lib-linux/libvpower.so',
            in_path='' if run_remote else '-g/iir_filterTB/DM/IN_PATH="../../common"',
            out_path='' if run_remote else '-g/iir_filterTB/DS/OUT_PATH="../../common"'
        ))

        if not cli_mode:
            script_file.write('\n\n# restart simulation and load waves')
            script_file.write('\nrestart -force')
            script_file.write('\ndo ./wave.do')

        script_file.write('\n\n# run simulation')
        script_file.write('\nrun -all')

    print('Done.')


if __name__ == '__main__':
    # ask for where to run simulation
    print('Do you wish to run the simulation locally or on the remote server?')
    print('\t1) Locally')
    print('\t2) Remote server')
    run_remote = get_choice(range(1, 3)) - 1

    # ask if the user wants the GUI or not
    print('Do you wish to run the simulation using the GUI or the command line?')
    print('Note: waves are only available when using the GUI.')
    print('\t1) GUI')
    print('\t2) Command line')
    cli_mode = get_choice(range(1, 3)) - 1

    # ask for version to use
    print('\nWhich version do you wish to use?')
    version = get_choice(range(4))

    # ask for design to simulate
    print('\nWhich design do you wish to simulate?')
    print('\t1) Original VHDL architecture')
    print('\t2) Post-synthesis netlist')
    design_choice = get_choice(range(1, 3))

    gen_tcl(run_remote, cli_mode, version, design_choice)