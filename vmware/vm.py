from pyVmomi import vim

class VM:
    """
    Data class to abstract away the mess of the pyvmomi API.

    Represents a VMWare VM object.
    """

    @staticmethod
    def get_vm_by_name(vSphere, name):
        """
        Builder - talks to vSphere to find the VM of the given name, creates a VM object to hold information about
        it.

        :Note: it can take a while to find the VM depending on how many VMs vSphere returns...

        :param VSphere vSphere:
        :param str name:
        :return:
        :raises VMWareObjectNotFound: if there isn't a matching VM.
        """

        vm_obj = vSphere.get_vmw_obj_by_name(vim.VirtualMachine, name)
        return VM(vm_obj)

    def __init__(self, vmware_vm_object):
        """
        :param vim.VirtualMachine vmware_vm_object:
        :raises: TypeError if the wrong sort of object was given. Use the builder!
        """

        if not isinstance(vmware_vm_object, vim.VirtualMachine):
            raise TypeError(f"VM was instantiated with a {type(vmware_vm_object)} instead of vim.VirtualMachine!")

        self.vmware_vm_obj = vmware_vm_object

    def __str__(self):
        return str(self.vmware_vm_obj)
