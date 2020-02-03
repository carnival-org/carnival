from io import StringIO

from fabric.transfer import Transfer, Result  # type:ignore
from patchwork import transfers  # type:ignore

from carnival import global_context
from carnival.templates import render


def rsync(source, target, exclude=(), delete=False, strict_host_keys=True, rsync_opts="--progress -pthrvz", ssh_opts=''):
    # https://fabric-patchwork.readthedocs.io/en/latest/api/transfers.html#patchwork.transfers.rsync
    return transfers.rsync(
        c=global_context.conn,
        source=source,
        target=target,
        exclude=exclude,
        delete=delete,
        strict_host_keys=strict_host_keys,
        rsync_opts=rsync_opts,
        ssh_opts=ssh_opts,
    )


def get(remote: str, local: str, preserve_mode: bool = True) -> Result:
    # http://docs.fabfile.org/en/2.5/api/transfer.html#fabric.transfer.Transfer.get
    t = Transfer(global_context.conn)
    return t.get(remote=remote, local=local, preserve_mode=preserve_mode)


def put(local: str, remote: str, preserve_mode: bool = True) -> Result:
    # http://docs.fabfile.org/en/2.5/api/transfer.html#fabric.transfer.Transfer.put
    t = Transfer(global_context.conn)
    return t.put(local=local, remote=remote, preserve_mode=preserve_mode)


def put_template(template_path: str, remote: str, **context) -> Result:
    filestr = render(template_path=template_path, **context)
    t = Transfer(global_context.conn)
    return t.put(local=StringIO(filestr), remote=remote, preserve_mode=False)
