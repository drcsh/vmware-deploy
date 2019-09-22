from os_customizer.os_customizer import OSCustomizer
from vmware.guest_os_interface import GuestOSCommand


class WindowsCustomizer(OSCustomizer):
    """
    Sets up Windows Server 2012/2016.

    n.b. requires an Administrator account with Windows UAC disabled, and Powershell installed or commands won't run
    properly.
    """

    def define_command_list(self):

        # Locations of common programs you'll want to run in Windows
        powershell_path = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
        cmd_path = "C:\\Windows\\System32\\cmd.exe"
        cscript_path = "C:\\Windows\\System32\\cscript.exe"

        # Name for default network. Used because it is significantly easier to change the network settings if
        # you know the network adapter /name/ and it's significantly more reliable to simply set it to a known value
        # than try to dump the name somewhere then pull it back to this script.
        # Warning: I've seen some weird issues with the adapter name. It must not contain spaces or >1 capital letter
        # Windows shouldn't care, and won't if you do it directly on the box, but it doesn't like it from the script...
        new_net_adapter_name = "virtnet"

        # Windows has a funny idea of MAC addresses
        windows_network_device_mac = self.spec.network_device_mac.upper().replace(":", "-")

        '''
            Command defs
        '''

        rename_computer = {
            'command': GuestOSCommand(
                program_path=powershell_path,
                program_command=f'-c \"Rename-Computer {self.vm_name[:15]}\"',
                description='Rename VM',
            ),
            'success_required': False,
        }

        # Note I've experienced issue with line breaks in commands sent to windows, so I keep them on one line

        disable_terminal_server_rdp_tcp_auth = {
            'command': GuestOSCommand(
                program_path=cmd_path,
                program_command="/c REG ADD \"HKLM\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp\" /v UserAuthentication /t REG_DWORD /d 0 /f",
                description='Disable Terminal Server RDP-TCP user auth',
                output_file_location='C:\\set_rdp_auth.log',
                success_outputs=['The operation completed successfully.']
            ),
            'success_required': False,  # May already be disabled
        }

        start_terminal_service_on_boot = {
            'command': GuestOSCommand(
                program_path=cmd_path,
                program_command="/c sc config TermService start=auto",
                description='Start the terminal service automatically on Windows start',
                output_file_location='C:\\term_service_auto_start.log',
                success_outputs=['[SC] ChangeServiceConfig SUCCESS']
            ),
            'success_required': False,  # May already be enabled
        }

        enable_terminal_service_encryption = {
            'command': GuestOSCommand(
                program_path=cmd_path,
                program_command="/c REG ADD \"HKLM\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp\" /v MinEncryptionLevel /t REG_DWORD /d 1 /f",
                description='Enable terminal server encryption',
                output_file_location='C:\\set_term_serv_encryption.log',
                success_outputs=['The operation completed successfully.']
            ),
            'success_required': False,  # May already be enabled
        }

        set_net_adapter_name = {
            'command': GuestOSCommand(
                program_path=powershell_path,
                program_command=f"-c \"Get-NetAdapter | where {{$_.MacAddress -eq \\\"{windows_network_device_mac}\\\"}} | rename-NetAdapter -NewName {new_net_adapter_name}\"",
                description=f'Set the NetAdapter name to {new_net_adapter_name}',
                output_file_location='C:\\set_net_adapater_name.log',
                success_outputs=['']
            ),
            'success_required': True  # May already be enabled
        }

        set_up_networking = {
            'command': GuestOSCommand(
                program_path=cmd_path,
                program_command="/c netsh interface ip set address name=\"{}\" static {} {} {}".formtat(
                    new_net_adapter_name,
                    self.spec.ip,
                    self.spec.netmask,
                    self.spec.default_gateway
                ),
                description=f'Set up networking on {new_net_adapter_name}',
                output_file_location='C:\\network_settings.log',
                success_outputs=['']
            ),
            'success_required': True
        }

        set_primary_dns = {
            'command': GuestOSCommand(
                program_path=cmd_path,
                program_command=f"/c netsh interface ip set dns name=\"{new_net_adapter_name}\" static 1.1.1.1 primary validate=no",
                description=f'Set primary DNS',
                output_file_location='C:\\dns_1.log',
                success_outputs=['']
            ),
            'success_required': True
        }

        set_secondary_dns = {
            'command': GuestOSCommand(
                program_path=cmd_path,
                program_command=f"/c netsh interface ip set dns name=\"{new_net_adapter_name}\" static 9.9.9.9 index=2 validate=no",
                description=f'Set secondary DNS',
                output_file_location='C:\\dns_2.log',
                success_outputs=['The object is already in the list.']
            ),
            'success_required': False
        }




        first_command_list = [
            rename_computer,
            disable_terminal_server_rdp_tcp_auth,
            start_terminal_service_on_boot,
            enable_terminal_service_encryption,
        ]

        # Need to reboot before doing networking, specifically Windows 2012 tends to screw up otherwise
        second_command_list = [
            set_net_adapter_name,
            set_up_networking,
            set_primary_dns,
            set_secondary_dns
        ]

        self.command_list = [
            first_command_list,
            second_command_list,
        ]
