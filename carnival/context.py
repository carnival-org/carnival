import inspect
import os
import typing

from carnival.exceptions import ContextBuilderError, ContextBuilderPassAllArgs


def _get_arg_names(fn: typing.Callable[..., typing.Any]) -> typing.Dict[str, bool]:
    arg_names: typing.Dict[str, bool] = {}

    for arg_name, arg_parameter in inspect.signature(fn).parameters.items():
        if arg_parameter.kind not in [
            arg_parameter.KEYWORD_ONLY,
            arg_parameter.POSITIONAL_OR_KEYWORD,
            arg_parameter.VAR_KEYWORD,
        ]:
            raise ContextBuilderError("only keyword parameters required for autocontext")

        if arg_parameter.kind == arg_parameter.VAR_KEYWORD:
            raise ContextBuilderPassAllArgs()

        arg_names[arg_name] = arg_parameter.default == arg_parameter.empty

    if 'self' in arg_names:
        arg_names.pop('self')

    return arg_names


def build_kwargs(
    fn: typing.Callable[..., typing.Any],
    context: typing.Dict[str, typing.Any],
) -> typing.Dict[str, typing.Any]:
    try:
        arg_names: typing.Dict[str, bool] = _get_arg_names(fn)
    except ContextBuilderPassAllArgs:
        # Pass all context if kwargs var exists
        return context.copy()

    kwargs = {}
    for arg_name, is_arg_required in arg_names.items():
        if arg_name not in context and is_arg_required:
            raise ContextBuilderError(f"Variable '{arg_name}', is not present in context.")

        if arg_name in context:
            kwargs[arg_name] = context[arg_name]
    return kwargs


def build_context(*context_chain: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    run_context: typing.Dict[str, typing.Any] = {}

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
