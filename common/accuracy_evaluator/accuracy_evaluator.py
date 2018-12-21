# import modules and functions ---------------------------------------------------------------------------

# import settings
import settings as s
# enable matlab control
import matlab.engine
# import ssh functions
from ../ import isa

# import constants and settings ---------------------------------------------------------------------------

# save server root path from settings
remote_root = s.remote_root
# set repo root path
repo_root = isa.get_root('ISA-digital-arithmetic')

# generate samples if there's the need for them ------------------------------------------------------------

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

# connect to the server ------------------------------------------------------------------------------------

print('Connecting to the server...\n')
session = isa.ssh_session('isa22', 'led-x3850-2.polito.it', 10020)
print('Connection established.\n')

print('\nCopy samples to server.')
session.copy_to('{}/common/samples.txt'.format(repo_root), '{}/common/'.format(remote_root))

# run the SW model ------------------------------------------------------------------------------------------

# compile C model if not already there and run it
with isa.cd('{}/C_filter'.format(repo_root)):
    c_exe_name = 'iir_filter.o'
    if not os.path.isfile(c_exe_name):
        print('\nNo executable for C model found. Will compile C file.')
        os.system('g++ iir_filter.c -o {}'.format(c_exe_name))
    print('\nRun C model on selected samples.')
    os.system('./{} ../common/samples.txt ../common/results-c.txt'.format(c_exe_name))
    print()

# simulate each design

# compare each design with the SW model

eng = matlab.engine.start_matlab()
for 
eng.calcErr(fSW, fHW, nargout=0)
