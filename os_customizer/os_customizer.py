
class OSCustomizer:

    @staticmethod
    def get_os_customizer(os_type, vsphere, vm_obj):

        if os_type.lower() == "windows":
            return WindowsCustomizer(vsphere, vm_obj)

        if os_type.lower() == 'centos':
            return CentOSCustomizer(vsphere, vm_obj)

    def __init__(self, vsphere, vm_obj):
        self.vsphere = vsphere
        self.vm = vm_obj

    def customize(self):
        # stub, implemented by child classes
        raise NotImplementedError()


class WindowsCustomizer(OSCustomizer):

    def customize(self):
        pass


class CentOSCustomizer(OSCustomizer):

    def customize(self):
        pass

