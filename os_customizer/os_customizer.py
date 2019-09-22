from abc import ABC

from os_customizer.centos_customizer import CentOSCustomizer
from os_customizer.windows_customizer import WindowsCustomizer


class VMCustomizationSpec:
    """
    Data class for holding settings which will be applied to the VM being customized.
    """

    def __init__(self,
                 admin_username,
                 admin_password,
                 ip,
                 network_device_mac,
                 netmask="255.255.255.0",
                 default_gateway=None):
        """
        :param str admin_username: Username of the administrator account the script can log in as
        :param str admin_password: Password for the adminsitrator account
        :param str ip: IP to set on the box
        :param str network_device_mac: MAC address of the network device we're going to configure
        :param str netmask: Netmask to set on that device (defaults to 255.255.255.0)
        :param str default_gateway: (optional) defaults to .1 on the subnet of the given IP. (only works for ipv4)
        """
        self.admin_username = admin_username
        self.admin_password = admin_password
        self.ip = ip
        self.network_device_mac = network_device_mac
        self.netmask = netmask

        if default_gateway:
            self.default_gateway = default_gateway
        else:
            # Default to .1 in the last octet of the IP
            self.default_gateway = ip.rpartition(".")[0] + '.1'


class OSCustomizer(ABC):
    """
    Base class with builder, defines interfaces for the implementation classes.
    """

    command_wait_seconds = 5  # time to wait between running commands.

    @staticmethod
    def os_customizer_builder(os_type, vsphere, vm_name, spec):
        """
        Get an appropriate OS customizer instance for the given VM

        :param str os_type: Windows/CentOS
        :param vsphere vsphere:
        :param str vm_name:
        :param VMCustomizationSpec spec:
        :return:
        """

        if os_type.lower() == "windows":
            return WindowsCustomizer(vsphere, vm_name, spec)

        if os_type.lower() == 'centos':
            return CentOSCustomizer(vsphere, vm_name, spec)

        return NotImplementedError(f"No suitable customizer for OS type {os_type}")

    def __init__(self, vsphere, vm_name, spec):
        """
        Set up class variables and get an interface for talking to the guest OS

        :param VSphere vsphere:
        :param str vm_name:
        :param VMCustomizationSpec spec: settings used for customizing this VM
        """
        self.vsphere = vsphere
        self.vm_name = vm_name
        self.spec = spec

        self.os_interface = vsphere.get_guestosinterface_for_vm(self.vsphere,
                                                                self.vm_name,
                                                                self.spec.admin_username,
                                                                self.spec.admin_password)
        self._populate_command_list()

    def _populate_command_list(self):
        """
        Stub. Extended by child lists to define which commands will be run on the OS.

        :return:
        """
        self.command_list = []

    def customize(self):
        """
        Run commands (defined by the command_list) on the guest OS of the VM (specified in init)

        TODO: Maybe refactor round to specify the VM here?
        :return:
        """
        try:
            self._process_commands()
        except Exception as e:
            print(e)
            # TODO - proper handling

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
