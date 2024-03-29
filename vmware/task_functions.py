import time

from pyVmomi import vim, vmodl

from vmware.exceptions import VMWareTimeout


def wait_for_task_complete(task, timeout_seconds=None):
    """
    Helper function, when we've triggered a VMWare task and need to sit and wait for it to be done.

    Optionally takes a maximum amount of time to wait. Default is no timeout.

    :note: With no timeout set this may never end.

    :param task:
    :param int timeout_seconds: (optional) the maximum number of seconds to wait before deciding it's a lost cause
    :return: whether the task was successful
    :rtype bool:
    """
    seconds_waited = 0
    while task.info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
        print(f" VSphere: Waiting for {task} to complete.")
        time.sleep(10)
        seconds_waited += 10
        if timeout_seconds and timeout_seconds < seconds_waited:
            raise VMWareTimeout(f"Waited {seconds_waited} seconds for {task} to complete and it didn't!")

    if task.info.state == vim.TaskInfo.State.success:
        return True

    return False