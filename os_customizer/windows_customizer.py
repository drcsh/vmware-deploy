from os_customizer.os_customizer import OSCustomizer
from vmware.guest_os_interface import GuestOSCommand


class WindowsCustomizer(OSCustomizer):
    """
    Sets up Windows Server 2012/2016.

    n.b. requires an Administrator account with Windows UAC disabled, and Powershell installed or commands won't run
    properly.
    """

    def customize(self):

        powershell_path = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
        cmd_path = "C:\\Windows\\System32\\cmd.exe"
        cscript_path = "C:\\Windows\\System32\\cscript.exe"

        rename_computer = {
            'command': GuestOSCommand(
                program_path=powershell_path,
                program_command=f'-c \"Rename-Computer {self.vm_name[:15]}\"',
                description='Rename VM',
            ),
            'success_required': False,
        }
        

        first_command_list = [
            rename_computer,
        ]
