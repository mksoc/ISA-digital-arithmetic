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


def gen_tcl(version, period, compile_cmd):
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
set $OLOAD [all_outputs]""")

        script_file.write("""\n\n# start synthesis
{} > ./logs/compile-log.txt""".format(compile_cmd))

        script_file.write("""\n\n# save results
report_resources > ./reports/resources-report.txt
report_timing > ./reports/timing-report.txt
report_area > ./reports/area-report.txt

# flatten hierarchy
ungroup -all -flatten

# setup Verilog name rules
change_names -hierarchy -rules verilog

# export netlist delay file
write_sdf ../netlist/iir_filter.sdf

# export netlist file
write -f verilog -hierarchy -output ../netlist/iir_filter.v

# export Synopsys Design Constraints file
write_sdc ../netlist/iir_filter.sdc

#convert lib into .saif for modelsim
read_file NangateOpenCellLibrary_typical_ecsm_nowlm.db
lib2saif -out ../saif/NangateOpenCellLibrary.saif NangateOpenCellLibrary""")

    print('Done.')


# get current working dir and set repo root path
repo_name = 'ISA-digital-arithmetic'
cwd = os.getcwd()
repo_root = cwd[0:cwd.find(repo_name) + len(repo_name)]

if __name__ == '__main__':
    # ask for version to use
    print('Which version do you wish to use?')
    version = get_choice(range(4))
    while not os.path.isfile('../HW_filter/version{}/iir_filter.vhd'.format(version)):
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

    # ask for compile command
    print('\nWhich command do you want to use?')
    print('\t1) compile')
    print('\t2) compile_ultra')
    compile_cmd = get_choice(range(1, 3))

    gen_tcl(version, period, compile_cmd)
