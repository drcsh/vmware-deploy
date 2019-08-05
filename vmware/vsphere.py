
from pyVmomi import vmodl
from pyVmomi import vim


class VSphere:
    """
        Wrapper class for talking to VMWare vSphere
    """

    def __init__(self, uri, username, password):
        self.uri = uri
        self._username = username
        self._password = password

    def connect(self):
        """
        Connect to vSphere
        :return:
        """
        pass

    def clone_machine(self, vm_obj, vm_host_name, new_vm_name):
        pass

    def configure_machine(self, vm_obj, vm_network_name, hardware_specs):
        pass
