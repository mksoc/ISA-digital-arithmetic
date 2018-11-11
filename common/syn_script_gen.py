#! /usr/bin/python3
import datetime
import os


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


def gen_tcl(version, period, adder=None, multiplier=None, compile_cmd='compile'):
    print('\nGenerating TCL script...')
    with open('py-syn-script.tcl', 'w') as script_file:
        script_file.write("""# =================================================================
# *****************************************************************
# *************** GENERATED USING syn_script_gen.py ***************
# ************           {date}           ************
# *****************************************************************
# The script was generated starting from these values of variables:
# version = {version}
# clock period = {period}
# compile command = {cmd}
# =================================================================\n""".format(
            date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            version=version,
            period=period,
            cmd=compile_cmd
        ))

        script_file.write('\n# compile source files')
        src_files = [f for f in os.listdir('{}/HW_filter/src'.format(repo_root)) if os.path.isfile(os.path.join('{}/HW_filter/src'.format(repo_root), f))]
        ver_files = [f for f in os.listdir('{}/HW_filter/version{}'.format(repo_root, version)) if os.path.isfile(os.path.join('{}/HW_filter/version{}'.format(repo_root, version), f)) and '.vhd' in f]
        if 'filter_pkg.vhd' in src_files:
            script_file.write('\nanalyze -f vhdl -lib WORK ../src/filter_pkg.vhd')
            src_files.remove('filter_pkg.vhd')
        for f in src_files:
            script_file.write('\nanalyze -f vhdl -lib WORK ../src/{}'.format(f))
        for f in ver_files:
            script_file.write('\nanalyze -f vhdl -lib WORK ../version{}/{}'.format(version, f))

        script_file.write("""\n\n# preserve RTL names
set power_preserve_rtl_hier_names true

# elaborate design
elaborate iir_filter -arch structure -lib WORK > ./logs/elaborate-log.txt
uniquify
link""")

        script_file.write("""\n\n# create symbolic clock signal
create_clock -name CLOCK -period {} clk
set_dont_touch_network CLOCK
set_clock_uncertainty 0.07 [get_clocks CLOCK]""".format(period))

        script_file.write("""\n\n# set input/output delays
set_input_delay 0.5 -max -clock CLOCK [remove_from_collection [all_inputs] CLOCK]
set_output_delay 0.5 -max -clock CLOCK [all_outputs]

# set output load capacitance
set OLOAD [load_of NangateOpenCellLibrary/BUF_X4/A]
set $OLOAD [all_outputs]

# flatten hierarchy
ungroup -all -flatten""")

        if adder is not None or multiplier is not None:
            script_file.write('\n\n# set implementations')        

            if adder == 1:
                script_file.write('\nset_implementation DW01_add/rpl [find cell *add_*]')
                script_file.write('\nset_implementation DW01_sub/rpl [find cell *sub_*]')
            elif adder == 2:
                script_file.write('\nset_implementation DW01_add/cla [find cell *add_*]')
                script_file.write('\nset_implementation DW01_sub/cla [find cell *sub_*]')
            elif adder == 3:
                script_file.write('\nset_implementation DW01_add/pparch [find cell *add_*]')
                script_file.write('\nset_implementation DW01_sub/pparch [find cell *sub_*]')

            if multiplier == 1:
                script_file.write('\nset_implementation DW02_mult/csa [find cell *mult_*]')
            elif multiplier == 2:
                script_file.write('\nset_implementation DW02_mult/pparch [find cell *mult_*]')

        script_file.write("""\n\n# start synthesis
{} > ./logs/compile-log.txt""".format('compile' if compile_cmd == 1 else 'compile-ultra'))

        script_file.write("""\n\n# save results
report_resources > ./reports/resources-report.txt
report_timing > ./reports/timing-report.txt
report_area > ./reports/area-report.txt

# setup Verilog name rules
change_names -hierarchy -rules verilog

# export netlist delay file
write_sdf ./netlist/iir_filter.sdf

# export netlist file
write -f verilog -hierarchy -output ./netlist/iir_filter.v

# export Synopsys Design Constraints file
write_sdc ./netlist/iir_filter.sdc

# convert lib into .saif for modelsim
read_file NangateOpenCellLibrary_typical_ecsm_nowlm.db
lib2saif -out ./saif/NangateOpenCellLibrary.saif NangateOpenCellLibrary

quit""")

    print('Done.')


def setup_param():
    # ask for version to use
    print('Which version do you wish to use?')
    version = get_choice(range(4))
    while not os.path.isfile('{}/HW_filter/version{}/iir_filter.vhd'.format(repo_root, version)):
        print('Entity for version {} is not defined (yet). Please choose another version.'.format(version))
        version = get_choice(range(4))

    # ask for clock period
    while True:
        try:
            period = float(input('\nType the desired clock period and press enter (0 for minimum): '))
        except ValueError:
            print('Error. Invalid value. Try again.')
        else:
            break

    # ask for forcing components from DW    
    while True:
        add_choice = input('\nDo you want to instantiate special implementations for adders? (y/n): ')
        if add_choice == 'y':
            print('Which one?')
            print('\t1) Ripple carry')
            print('\t2) Carry lookahead')
            print('\t3) Parallel prefix')
            adder = get_choice(range(1, 4))
            break
        elif add_choice == 'n':
            adder = None
            break
        else:
            print('Please type "y" or "n" and press enter.')

    while True:
        mult_choice = input('\nDo you want to instantiate special implementations for multipliers? (y/n): ')
        if mult_choice == 'y':
            print('Which one?')
            print('\t1) Carry save')
            print('\t2) Parallel prefix')
            multiplier = get_choice(range(1, 3))
            break
        elif mult_choice == 'n':
            multiplier = None
            break
        else:
            print('Please type "y" or "n" and press enter.')

    # ask for compile command
    print('\nWhich command do you want to use?')
    print('\t1) compile')
    print('\t2) compile_ultra')
    compile_cmd = get_choice(range(1, 3))

    gen_tcl(version, period, adder, multiplier, compile_cmd)
    return version


# get current working dir and set repo root path
repo_name = 'ISA-digital-arithmetic'
cwd = os.getcwd()
repo_root = cwd[0:cwd.find(repo_name) + len(repo_name)]

if __name__ == "__main__":
    setup_param()