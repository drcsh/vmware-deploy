from abc import ABC

from os_customizer.centos_customizer import CentOSCustomizer
from os_customizer.windows_customizer import WindowsCustomizer


class OSCustomizer(ABC):
    """
    Base class with builder, defines interfaces for the implementation classes.
    """

    @staticmethod
    def get_os_customizer(os_type, vsphere, vm_name, admin_account_details):

        if os_type.lower() == "windows":
            return WindowsCustomizer(vsphere, vm_name, admin_account_details)

        if os_type.lower() == 'centos':
            return CentOSCustomizer(vsphere, vm_name, admin_account_details)

        return NotImplementedError(f"No suitable customizer for OS type {os_type}")

    def __init__(self, vsphere, vm_name, admin_account_details):
        """

        :param VSphere vsphere:
        :param str vm_name:
        :param dict admin_account_details:
        """
        self.vsphere = vsphere
        self.vm_name = vm_name
        self.admin_username = admin_account_details.get('username')
        self.admin_password = admin_account_details.get('password')

    def customize(self):
        # stub, implemented by child classes
        raise NotImplementedError()

