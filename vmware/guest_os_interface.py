import time

import requests
from pyVmomi import vim, vmodl

from vmware.exceptions import VMWareGuestOSException, VMWareGuestOSTimeoutException, \
    VMWareGuestOSProcessUnknownException, VMWareBadState, VMWareGuestOSProcessAmbiguousResultException, \
    VMWareGuestOSProcessBadOutputException


class GuestOSCommand:

    def __init__(self,
                 path,
                 command,
                 output_file_location='',
                 command_timeout_seconds=120,
    ):
        pass # maybe required maybe not


class GuestOSInterface:
    """
        Interface for talking to the guest OS. Masks the complicated inner workings of VMWare.
    """

    def __init__(self, vsphere, vmname, username, password):
        self.vsphere = vsphere
        self.vmname = vmname
        self.vm_obj = vsphere.get_vmw_obj_by_name(vim.VirtualMachine, vmname)
        self.process_manager = vsphere.get_process_manager()
        self.file_manager = vsphere.get_file_manager()
        self.login_credentials = vim.vm.guest.NamePasswordAuthentication(
            username=username, password=password
        )

    def run_command_and_check_result(self,
                                     path,
                                     command,
                                     output_file_location='',
                                     expected_outputs=list,
                                     command_timeout_seconds=60):
        """
        Run a command on the GuestOS and

        :param str path:
        :param str command:
        :param str output_file_location:
        :param list expected_outputs:
        :param int command_timeout_seconds:
        :return:
        """
        pid = self.run_command(path, command, output_file_location='')

        command_running = True
        check_output = False

        if pid == 0:
            raise VMWareGuestOSException(f"No Process ID returned running command {command}")

        '''
            Make sure that the command has finished before we move on to the next one
        '''
        timeout_counter = 0
        while command_running:

            # Default to breaking the loop as there are several exit conditions and only 1 continue.
            command_running = False

            process_list = self.process_manager.ListProcessesInGuest(self.vm_obj,
                                                                     self.login_credentials,
                                                                     [pid])

            # It is possible that we don't get any info back, in this case, we give up looking and check output
            if len(process_list) == 0:
                raise VMWareGuestOSException("No process info returned by the GuestOS. Can't check status!")

            process_info = process_list.pop()

            # Here we look for an exit code. If there isn't one, the process is running
            if process_info.exitCode is not None:

                # 0 is the "all good" response.
                if process_info.exitCode == 0:
                    return

            elif timeout_counter > command_timeout_seconds:
                raise VMWareGuestOSTimeoutException(f"Command did not finish in < {command_timeout_seconds}s")

            # If there's no exit code, and we didn't time out, keep waiting.
            timeout_counter += 5
            time.sleep(5)

        '''
            If we didn't return earlier, something went wrong. We now try to check the output of the process, this
            relies on the output being redirected to file.
        '''
        # If we've flagged the command for a check but we have no output redirect, we'll need to note this...
        if not output_file_location:
            raise VMWareGuestOSProcessUnknownException(
                "The process did not complete successfully but no output file was specified, so the output was not " 
                "recorded."
            )

        # Unfortunately the way vSphere gives us access to files is to host them on a webserver on the vm host (!!!)
        # We therefore have to get-request it. I assume there are various reasons that the file won't be there etc, but
        # the documentation is not clear...
        vmw_file_transfer_obj = self.file_manager.InitiateFileTransferFromGuest(
            self.vm_obj,
            self.login_credentials,
            output_file_location
        )

        url = vmw_file_transfer_obj.url

        if not url:
            # I assume this is possible...
            raise FileNotFoundError(f"Couldn't locate file {output_file_location} - VMWare didn't return a URL")

        resp = requests.get(url, verify=False)

        if not resp.status_code == 200:
            raise VMWareBadState(f"Didn't receive an appropriate response from VMWare when attempting to retrieve "
                                 f"the output file {output_file_location}. Expected an HTTP 200 response, but"
                                 f"received a {resp.status_code}: {resp.reason}")

        # The cmd output adds new lines etc. So we strip them out to avoid issues.
        file_contents = resp.text.replace("\r", "").replace("\n", "").strip(" ")

        # If we got the file, check it's an expected output. If it isn't, append an error.
        # This is complicated by blank results (sometimes expected) and complex results which we want to
        # look for the success message contained in.

        # Check for expected blank output
        if file_contents.strip() == '' and '' in expected_outputs:
            raise VMWareGuestOSProcessAmbiguousResultException(
                "Command did not exit successfully, but a blank output was found, and a blank output "
                "can be expected. This could mean that the command failed silently."
            )

        # Deal with text output
        for expected_result in expected_outputs:
            if expected_result in file_contents:
                return  # success

        raise VMWareGuestOSProcessBadOutputException(
            f"This command did not exit successfully, and an unexpected result was recorded in the output file: "
            f"{file_contents}"
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
