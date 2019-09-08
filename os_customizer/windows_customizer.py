from os_customizer.os_customizer import OSCustomizer


class WindowsCustomizer(OSCustomizer):
    """
    Sets up Windows Server 2012/2016.

    n.b. requires an Administrator account with Windows UAC disabled, and Powershell installed or commands won't run
    properly.
    """

    def customize(self):
        pass
