from itertools import chain
import inspect
import os
from typing import List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from carnival.host import Host
    from carnival.step import Step


class PassAllArgs(BaseException):
    pass


def _get_arg_names(fn) -> List[str]:
    arg_names: List[str] = []
    spec = inspect.getfullargspec(fn)

    if spec.varargs is not None:
        raise ValueError("*args is not supported for autocontext")

    if spec.varkw is not None:
        # Not actual if kwargs argument exists
        raise PassAllArgs()

    arg_names += spec.args
    arg_names += spec.kwonlyargs

    if 'self' in arg_names:
        arg_names.remove('self')

    return arg_names


def build_kwargs(fn, context: Dict[str, Any]):
    try:
        arg_names: List[str] = _get_arg_names(fn)
    except PassAllArgs:
        # Pass all context if kwargs var exists
        return context.copy()

    kwargs = {}
    for context_name, context_val in context.items():
        if context_name in arg_names:
            kwargs[context_name] = context_val
    return kwargs


def build_context(step: 'Step', host: 'Host') -> Dict[str, Any]:
    run_context: Dict[str, Any] = {'host': host}

    env_prefix = "CARNIVAL_CTX_"
    # Build context from environment variables
    for env_name, env_val in os.environ.items():
        if env_name.startswith(env_prefix):
            run_context[env_name[len(env_prefix):]] = env_val

    for var_name, var_val in chain(host.context.items(), step.context.items()):
        if isinstance(var_val, context_ref):
            try:
                run_context[var_name] = run_context[var_val.context_var_name]
            except KeyError as e:
                raise KeyError(f"There is no '{var_val.context_var_name}' variable in context") from e
        else:
            run_context[var_name] = var_val

    return run_context


class context_ref:
    """
    Ссылка на другую переменную контекста

    Например, так можно передать в переменную c именем `name` `Step` другую переменную контекста с именем `dns_domain`
    >>> TestStep(
    >>>   name=context_ref('dns_domain'),
    >>> ),

    """
    def __init__(self, context_var_name: str):
        self.context_var_name = context_var_name
