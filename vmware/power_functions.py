import time

from pyVmomi import vim, vmodl

from vmware import task_functions
from vmware.exceptions import VMWareTimeout


def power_on_vm_and_wait_for_os(v_sphere, vmw_vm):
    """
    Does the actual work of powering on a VM, i.e. starting the task, checking it finishes correctly, and then checking
    for vmware tools to become available which means that the os is ready.

    :param v_sphere:
    :param vmw_vm:
    :return:
    """

    print(f"Trying to power on {vmw_vm}")

    task = vmw_vm.PowerOn()
    task_functions.wait_for_task_complete(task, timeout_seconds=60)

    wait_for_vmware_tools_response(v_sphere, vmw_vm)


def wait_for_vmware_tools_response(v_sphere, vmw_vm):
    """
    Function that pokes the given vmware vm until VMWare guest tools are running or 20 minutes pass.

    Tries to work around a bug in either pyvmomi or the vsphere API where *sometimes* the vmware tools status is not
    updated on change. To do this we take the service instance itself and after waiting 2 minutes for tools, we get
    a 'fresh' managed object of the VM and ask it what it's tools status is.

    USAGE: Use this after rebooting or powering on a VM when it's important that you know when VMWare tools is back.

    :raises Exception: when vmware tools did not come up.
    :param VSphere v_sphere:
    :param vim.VirtualMachine vmw_vm:
    :return: vim.VirtualMachine: the refreshed managed object
    :rtype bool:
    """

    print("Waiting for VMWare Tools")
    wait_count = 0
    refreshes = 0
    while vmw_vm.guest.toolsRunningStatus != "guestToolsRunning":
        time.sleep(5)
        print("Still waiting for tools, current status {}".format(vmw_vm.guest.toolsRunningStatus))
        wait_count += 1

        # If we waited 2 minutes, try to get a new Managed Object from the Service Instance
        if wait_count > 24:
            # If we've already done this 10 times, give up
            if refreshes >= 10:
                msg = "  !! Reboot command issued but VMWare Tools did not come up within 20 minutes! Help!"
                print(msg)
                raise VMWareTimeout(msg)

            print("Waited 2 minutes for tools. Refreshing VM Object from Service Instance. Might be bugged.")
            vmw_vm = v_sphere.load_vmw_obj_by_name(vim.VirtualMachine, vmw_vm.config.name)
            refreshes += 1
