
class VMWareObjectNotFound(Exception):
    """
    When we looked for something and it wasn't in vSphere.
    """
    pass


class VMWareBadState(Exception):
    """
    Something VMWare side isn't in a state that we like the look of.
    """
    pass


class VMWareTimeout(Exception):
    """
    Something took too long to complete VMWare side.
    """
    pass


class VMWareGuestOSException(Exception):
    """
    Something went wrong when we were talking to the GuestOS
    """
    pass