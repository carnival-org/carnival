from carnival.core.host import HostBase


class Host(HostBase):
    def __init__(self, addr: str, **context):
        """
        Defined host to operate in
        :param addr: user@host, host, ip for remote, one if LOCAL_ADDRS for local execution
        :param context: Some context vars for use in runtime
        """
        self.addr = addr
        self.context = context
