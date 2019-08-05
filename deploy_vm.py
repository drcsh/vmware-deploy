from vmware import vm
from vmware.vsphere import VSphere


class ConfigurationError(Exception):
    pass


def __main__():
    vm_deployer = VMDeployer()
    vm_deployer.deploy()

class VMDeployer:

    def __init__(self):
        """
        Loads up the required files, checks them and clones the VM or VM Template
        :return:
        """

        print("Loading secret file and inputs...")

        try:
            self.secret = self.load_secret()
            self.inputs = self.load_inputs()
        except Exception as e:
            # todo
            pass

        print("Successfully loaded secret file and inputs. Validating.")

        try:
            self.validate_secret()
            self.validate_inputs()
        except ConfigurationError as e:
            print(f"Input Error: {str(e)}")
            exit(1)

        print("Inputs Validated.")

    def deploy(self):

        print("Connected to vSphere")

        vsphere = VSphere(self.secret['uri'], self.secret['username'], self.secret['password'])

        print(f"Connected. Fetching template ")

        template = vm.get_vm_by_name(self.inputs['template_name'])

        print(f"Template Found. Cloning. This may take some time...")

        vsphere.clone_machine(template, self.inputs['target_vm_host'], self.inputs['new_vm_name'])

        print(f"Cloning finished. Looking for new VM {inputs['new_vm_name']}")

        new_vm = vm.get_vm_by_name(vsphere, self.inputs['new_vm_name'])

        print("Found VM. Reconfiguring HW")

        vsphere.configure_machine(new_vm, self.inputs['vm_network'], self.inputs['new_vm_specs'])

        print("VM Reconfigured. Booting VM for the first time.")

        print("VM Booted. Passing to OS Preparation.")

        print("Completed!")

    def load_secret(self):
        pass

    def load_inputs(self):
        pass

    def validate_secret(self):
        pass

    def validate_inputs(self):
        pass
