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

    if host.context:
        run_context.update(host.context)
    if step.context:
        run_context.update(step.context)
    return run_context
