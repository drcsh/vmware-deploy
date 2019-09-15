from abc import ABC

from os_customizer.centos_customizer import CentOSCustomizer
from os_customizer.windows_customizer import WindowsCustomizer


class OSCustomizer(ABC):
    """
    Base class with builder, defines interfaces for the implementation classes.
    """

    @staticmethod
    def os_customizer_builder(os_type, vsphere, vm_name, admin_account_details):
        """
        Get an appropriate OS customizer instance for the given VM

        :param str os_type: Windows/CentOS
        :param vsphere vsphere:
        :param str vm_name:
        :param dict admin_account_details: Should contain 'username' and 'password' keys for logging in to the OS
        :return:
        """

        if os_type.lower() == "windows":
            return WindowsCustomizer(vsphere, vm_name, admin_account_details)

        if os_type.lower() == 'centos':
            return CentOSCustomizer(vsphere, vm_name, admin_account_details)

        return NotImplementedError(f"No suitable customizer for OS type {os_type}")

    def __init__(self, vsphere, vm_name, admin_account_details):
        """
        Set up class variables and get an interface for talking to the guest OS

        :param VSphere vsphere:
        :param str vm_name:
        :param dict admin_account_details:
        """
        self.vsphere = vsphere
        self.vm_name = vm_name
        self.admin_username = admin_account_details.get('username')
        self.admin_password = admin_account_details.get('password')

        self.os_interface = vsphere.get_guestosinterface_for_vm(self.vsphere,
                                                                self.vm_name,
                                                                self.admin_username,
                                                                self.admin_password)
        self.command_list = []

    def customize(self):
        # stub, implemented by child classes
        raise NotImplementedError()

    def _process_commands(self):
        """
        The customizer will define a command_list, which will be a list of lists. Each sub-list will contain commands
        to be run on the VM, and the VM will be restarted between lists.

        This is to facilitate the situation where the OS needs to be restarted to implement some changes which later
        commands rely upon.

        :return:
        """

        for command_sub_list in self.command_list:
            for command in command_sub_list:
                pass  # TODO

            # TODO restart VM
