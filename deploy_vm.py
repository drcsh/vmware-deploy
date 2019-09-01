from vmware.vsphere import VSphere


class ConfigurationError(Exception):
    pass


class VMDeployer(object):

    def __init__(self):
        """
        Loads up the required files, checks them and clones the VM or VM Template

        If you are aiming to integrate this with a larger system, start here :)

        :return:
        """

        print("Loading secret file and inputs...")

        try:
            self.secret = self.load_secret()
            self.inputs = self.load_inputs()
        except Exception as e:
            filename = "secret" if not self.secret else "inputs"
            print(f"Problem loading {filename}. Did you copy the same file over? Error: {str(e)}")
            exit(1)

        print("Successfully loaded secret file and inputs. Validating...")

        try:
            self.validate_secret()
            self.validate_inputs()
        except ConfigurationError as e:
            print(f"Validation Problem: {str(e)}")
            exit(1)

        print("Validated inputs and secrets.")

    def deploy(self):

        print("Connected to vSphere")

        v_sphere = VSphere(self.secret['uri'], self.secret['username'], self.secret['password'])

        print(f"Connected. Cloning. This may take some time...")

        v_sphere.clone_machine(self.inputs['template_name'],
                               self.inputs['target_vm_host'],
                               self.inputs['target_datastore'],
                               self.inputs['target_vm_folder'],
                               self.inputs['new_vm_name'],
                               )

        print("Found VM. Reconfiguring HW")

        v_sphere.configure_machine(self.inputs['new_vm_name'], self.inputs['vm_network'], self.inputs['new_vm_specs'])

        print("VM Reconfigured. Booting VM for the first time.")

        v_sphere.power_on_vm_and_wait_for_os(self.inputs['new_vm_name'])

        print("VM Booted. Passing to OS Preparation.")

        print("Completed!")

    def load_secret(self):
        """
        Just loads the SECRET dictionary. Provided to easily do your own thing.

        :return: secret vmware connection info
        :rtype dict:
        """
        from settings.secret import VMWARE_CONNECTION
        return VMWARE_CONNECTION

    def load_inputs(self):
        """
        Just loads the INPUT dictionary. Provided to easily do your own thing.

        :return: Inputs to determine what is going to be cloned where and with what specs.
        :rtype dict:
        """
        from input import INPUT
        return INPUT

    def validate_secret(self):
        """
        Make sure we have the necessary info to talk to vSphere.

        This is simple and intended to be extended.

        :return:
        """
        try:
            key = 'uri'
            uri = self.secret['uri']
            assert uri != ''

            key = 'username'
            username = self.secret['username']
            assert username != ''

            key = 'password'
            password = self.secret['password']
            assert password != ''

        except (KeyError, AssertionError) as e:
            raise ConfigurationError(f"Secret File is missing a required key {key}")

    def validate_inputs(self):
        """
        Make sure we have the necessary info to clone the VM.

        :return:
        """
        try:
            key = 'template_name'
            assert self.inputs['template_name'] != ''

            key = 'template_admin_account'
            template_admin_account = self.inputs['template_admin_account']
            assert isinstance(template_admin_account, dict)
            assert template_admin_account != {}

            key = 'template_admin_account: username'
            template_admin_account_username = template_admin_account['username']
            assert template_admin_account_username != ''

            key = 'template_admin_account: password'
            template_admin_account_password = template_admin_account['password']
            assert template_admin_account_password != ''

            key = 'template_os'
            assert self.inputs['template_os'] != ''

            key = 'target_vm_host'
            assert self.inputs['target_vm_host'] != ''

            key = 'target_datastore'
            assert self.inputs['target_vm_host'] != ''

            key = 'target_vm_folder'
            assert self.inputs['target_vm_folder'] != ''

            key = 'vm_network'
            assert self.inputs['vm_network'] != ''

            key = 'new_vm_name'
            assert self.inputs['new_vm_name'] != ''

            key = 'new_vm_specs'
            new_vm_specs = self.inputs['new_vm_specs']
            assert isinstance(new_vm_specs, dict)
            assert new_vm_specs != {}

            key = 'new_vm_specs: vcpus'
            assert isinstance(new_vm_specs['vcpus'], int)

            key = 'new_vm_specs: memory'
            assert isinstance(new_vm_specs['memory'], int)

            key = 'new_vm_specs: hdd'
            assert isinstance(new_vm_specs['hdd'], int)

            key = 'new_vm_networking'
            new_vm_networking = self.inputs['new_vm_networking']
            assert isinstance(new_vm_networking, dict)
            assert new_vm_networking != {}

            key = 'new_vm_networking: ip'
            assert new_vm_networking['ip'] != ''

            key = 'new_vm_networking: port'
            assert isinstance(new_vm_networking['port'], int)

        except (KeyError, AssertionError) as e:
            raise ConfigurationError(f"Input File is missing a required key {key}")


if __name__ == "__main__":
    vm_deployer = VMDeployer()
    vm_deployer.deploy()
