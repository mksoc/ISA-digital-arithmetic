import os
import subprocess


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


class ssh_session:
    def __init__(self, user, host, port=22, avoidTimeout=False):
        print('\nOpen tunnel connection to server.')
        self.user_host = '{}@{}'.format(user, host)
        self.port = port
        self.socket = '~/.ssh/{}'.format(self.user_host)
        if avoidTimeout:
            option = 'serverAliveInterval=120'
        else
            option = ''
        os.system('ssh -M -f -N -o ControlPath={} {} -p {} {}'.format(self.socket, option, self.port, self.user_host))

    def __del__(self):
        print('\nClose connection.')
        os.system('ssh -S {} -O exit {}'.format(self.socket, self.user_host))

    def get_param(self):
        return 'ssh -S {} -p {} {}'.format(self.socket, self.port, self.user_host)

    def run_commands(self, cmd):
        with open('ssh_commands.sh', 'w') as cmd_file:
            cmd_file.write(cmd)
        os.system(
            'cat ssh_commands.sh | ssh -S {} -p {} {}'.format(self.socket, self.port, self.user_host))
        os.remove('ssh_commands.sh')

    def copy_to(self, source, destination):
        os.system('rsync -avz -e "ssh -o ControlPath={socket} -p {port}" {source} {server}:{dest}'.format(
            socket=self.socket,
            port=self.port,
            source=source,
            server=self.user_host,
            dest=destination
        ))

    def copy_from(self, source, destination):
        os.system('rsync -avz -e "ssh -o ControlPath={socket} -p {port}" {server}:{source} {dest}'.format(
            socket=self.socket,
            port=self.port,
            source=source,
            server=self.user_host,
            dest=destination
        ))
    def clean(self, folderPath)
        rmCmd = 'rm -r {folderPath}'.format(folderPath=folderPath)
        mkdirCmd = 'mkdir {folderPath}'.format(folderPath=folderPath)
        run_commands(rmCmd)
        run_commands(mkdirCmd)


# functions definitions
def get_root(repo_name):
    cwd = os.getcwd()
    return cwd[0:cwd.find(repo_name) + len(repo_name)]


def get_choice(options, msg='Type the number corresponding to your choice and press enter: ', str_val=False, print_menu=True):
    if type(options).__name__ == 'range':
        str_val = False
        print_menu = False

    if print_menu:
        for item in options:
            print('\t{}) {}'.format(options.index(item) + 1, item))

    choice = ''
    while True:
        choice = input(msg)
        if choice.isdigit():
            if type(options).__name__ == 'range':
                if int(choice) in options:
                    return int(choice)
                else:
                    print('Error. Invalid option. Try again.')
            elif 0 < int(choice) <= len(options):
                return int(choice)
            else:
                print('Error. Invalid option. Try again.')
        elif str_val:
            return choice
        else:
            print('Error. Invalid option. Try again.')


def ask_version(path, file_to_check):
    print('Which version do you wish to use?')
    version = get_choice(range(4))
    while not os.path.isfile('{}/version{}/{}'.format(path, version, file_to_check)):
        print('Entity for version {} is not defined (yet). Please choose another version.'.format(version))
        version = get_choice(range(4))
    return version


def bash_source(file):
    if os.path.isfile(file):
        command = 'sh -c ". {} && env"'.format(file)
        for line in subprocess.getoutput(command).split('\n'):
            if line.startswith('PATH'):
                key, value = line.split('=')
                os.environ[key] = value
    else:
        raise FileNotFoundError('File "{}" not found'.format(file))
