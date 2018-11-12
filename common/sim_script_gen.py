#! /usr/bin/python3
import datetime
from common import isa


def gen_tcl(run_remote, cli_mode, version, design):
    print('\nGenerating TCL script...')
    with open('py-sim-script.tcl', 'w') as script_file:
        script_file.write("""# =================================================================
# *****************************************************************
# *************** GENERATED USING sim_script_gen.py ***************
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

        script_file.write('\n{}'.format(
            'puts "Running in command line mode. No waveforms will be available."' if cli_mode else 'puts "Running in GUI mode."'))

        script_file.write('\n\n# compile source files')
        script_file.write(
            '\nvcom -93 -work ./work ../src/{}.vhd'.format('*' if design == 1 else 'filter_pkg'
                                                           ))
        if design == 1:
            script_file.write(
                '\nvcom -93 -work ./work ../version{}/*.vhd'.format(version))
        elif design == 2:
            script_file.write(
                '\nvlog -work ./work ../version{}/*.v'.format(version))

        script_file.write('\n\n# compile testbench')
        script_file.write('\nvcom -93 -work ./work ../tb/*.vhd')
        script_file.write('\nvlog -work ./work {define}{syn}{no_gui} ../tb/iir_filterTB.v'.format(
            define='+define' if (cli_mode or design == 2) else '',
            syn='+SYN=1' if design == 2 else '',
            no_gui='+NO_GUI=1' if cli_mode else ''
        ))

        script_file.write('\n\n# load design')
        script_file.write('\nvsim {library} {in_path} {out_path} work.iir_filterTB'.format(
            library='' if design == 1 else '-L /software/dk/nangate45/verilog/msim6.2g -sdftyp /iir_filterTB/UUT=../version{ver}/iir_filter.sdf -pli /software/synopsys/syn_current/auxx/syn/power/vpower/lib-linux/libvpower.so'.format(ver=version),
            in_path='' if run_remote else '-g/iir_filterTB/DM/IN_PATH="{}/common"'.format(
                repo_root),
            out_path='' if run_remote else '-g/iir_filterTB/DS/OUT_PATH="{}/common"'.format(
                repo_root)
        ))

        if not cli_mode:
            script_file.write('\n\n# restart simulation and load waves')
            script_file.write('\nrestart -force')
            script_file.write('\ndo ./wave.do')

        script_file.write('\n\n# run simulation')
        script_file.write('\nrun -all')

    print('Done.')


# set repo root path
repo_root = isa.get_root('ISA-digital-arithmetic')

if __name__ == '__main__':
    # ask for where to run simulation
    print('Do you wish to run the simulation locally or on the remote server?')
    run_remote = isa.get_choice(['Locally', 'Remote server']) - 1

    # ask if the user wants the GUI or not
    print('Do you wish to run the simulation using the GUI or the command line?')
    print('Note: waves are only available when using the GUI.')
    cli_mode = isa.get_choice(['GUI', 'Command line']) - 1

    # ask for version to use
    version = isa.ask_version('{}/HW_filter'.format(repo_root), 'iir_filter.vhd')

    # ask for design to simulate
    print('\nWhich design do you wish to simulate?')
    design_choice = isa.get_choice(['Original VHDL architecture', 'Post-synthesis netlist'])

    gen_tcl(run_remote, cli_mode, version, design_choice)
