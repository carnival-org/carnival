import inspect
from typing import List, Dict, Any

from carnival.host import Host

from carnival.secrets_manager import secrets_storage


def _get_arg_names(fn) -> List[str]:
    arg_names: List[str] = []
    spec = inspect.getfullargspec(fn)
    arg_names += spec.args
    arg_names += spec.kwonlyargs
    return arg_names


def _build_kwargs(fn, context: Dict[str, Any]):
    arg_names: List[str] = _get_arg_names(fn)
    kwargs = {}

    for context_name, context_val in context.items():
        if context_name in arg_names:
            kwargs[context_name] = context_val
    return kwargs


class Step:
    def __init__(self, **context):
        self.context = context

    def _build_context(self, host: Host) -> Dict[str, Any]:
        run_context = {'secrets': secrets_storage, 'host': host}
        if host.context:
            run_context.update(host.context)
        if self.context:
            run_context.update(self.context)
        return run_context

    def run_with_context(self, host: Host):
        context = self._build_context(host)
        kwargs = _build_kwargs(self.run, context)
        return self.run(**kwargs)

    def run(self, **kwargs):
        raise NotImplementedError
