from os_customizer.os_customizer import OSCustomizer


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

        first_command_list = [
            {  # (note: it is limited to 15 chars)
                'desc': 'Rename VM',
                'path': powershell_path,
                'cmd': '-c \"Rename-Computer {}\"'.format(self.vm_name[:15]),
                'output_redirect': True,
                'output_file': 'C:\\set_vm_name.log',
                'success_msg': '',
                'required_success': False,
            },
        ]
