
from pyVmomi import vim, vmodl

from vmware.exceptions import VMWareGuestOSException


class GuestOSInterface:
    """
        Interface for talking to the guest OS. Masks the complicated inner workings of VMWare.
    """

    def __init__(self, vsphere, vmname, username, password):
        self.vsphere = vsphere
        self.vmname = vmname
        self.vm_obj = vsphere.get_vmw_obj_by_name(vim.VirtualMachine, vmname)
        self.process_manager = vsphere.get_process_manager()
        self.login_credentials = vim.vm.guest.NamePasswordAuthentication(
            username=username, password=password
        )

    def run_command(self, path, command, output_file_location=''):
        """
        Execute a command in the shell/command line of the target OS.

        :param str path: The location of the program to execute. E.g. the path to bash or cmd.exe/powershell
        :param str command: The command to run
        :param str output_file_location: (optional) if you want the output to be captured for checking, set a path.
        :return: the Process ID of the process in the guest OS
        :rtype int:
        """

        if output_file_location:
            command = f"{command} > {output_file_location}"

        print(f"Running {path} {command}")

        program_spec = vim.vm.guest.ProcessManager.ProgramSpec(
            programPath=path,
            arguments=command
        )

        try:
            pid = self.process_manager.StartProgramInGuest(self.vm_obj, self.login_credentials, program_spec)
        except Exception as e:
            raise VMWareGuestOSException(f"Could not run command in guest: '{command}' Exception: {str(e)}")

        print(f"Command sent to {self.vmname} and returned PID {pid}")

        return pid