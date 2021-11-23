import inspect
import os
from typing import Any, Callable, Dict, List


class ContextBuilderError(BaseException):
    pass


class PassAllArgs(BaseException):
    pass


def _get_arg_names(fn: Callable[..., Any]) -> List[str]:
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


def build_kwargs(fn: Callable[..., Any], context: Dict[str, Any]) -> Dict[str, Any]:
    try:
        arg_names: List[str] = _get_arg_names(fn)
    except PassAllArgs:
        # Pass all context if kwargs var exists
        return context.copy()

    kwargs = {}
    for arg_name in arg_names:
        # TODO: check if variable has default value
        # if arg_name not in context:
        #     raise ContextBuilderError("Required context var '{arg_name}' is not present in context.")

        if arg_name in context:
            kwargs[arg_name] = context[arg_name]
    return kwargs


def build_context(*context_chain: Dict[str, Any]) -> Dict[str, Any]:
    run_context: Dict[str, Any] = {}

    env_prefix = "CARNIVAL_CTX_"
    # Build context from environment variables
    for env_name, env_val in os.environ.items():
        if env_name.startswith(env_prefix):
            run_context[env_name[len(env_prefix):]] = env_val

    for context_item in context_chain:
        for var_name, var_val in context_item.items():
            if isinstance(var_val, context_ref):
                try:
                    run_context[var_name] = run_context[var_val.context_var_name]
                except KeyError as e:
                    raise ContextBuilderError(f"There is no '{var_val.context_var_name}' variable in context") from e
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
