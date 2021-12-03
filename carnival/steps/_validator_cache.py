"""
    Кеширование валидаторов для Steps
    Кеширует значение по Type[Step], Host, fact_id:str(задается в валидаторе)
"""

import typing

if typing.TYPE_CHECKING:
    from carnival import Host
    from carnival.steps.validators import StepValidatorBase


StepValidatorBaseT = typing.TypeVar("StepValidatorBaseT", bound="StepValidatorBase")
__vc: typing.Dict[str, typing.Optional[str]] = {}


def __build_vc_key(step_class: typing.Type[StepValidatorBaseT], host: "Host", fact_id: str) -> str:
    from carnival.utils import get_class_full_name
    return f"{get_class_full_name(step_class)}::{host.addr}::{fact_id}"


def try_get(
    step_class: typing.Type[StepValidatorBaseT],
    host: "Host",
    fact_id: str,
) -> typing.Tuple[bool, typing.Optional[str]]:
    global __vc
    cachekey = __build_vc_key(step_class=step_class, host=host, fact_id=fact_id)

    return (
        cachekey in __vc,
        __vc.get(
            __build_vc_key(step_class=step_class, host=host, fact_id=fact_id),
            None,
        )
    )


def set(step_class: typing.Type[StepValidatorBaseT], host: "Host", fact_id: str, val: typing.Optional[str]) -> None:
    global __vc
    cachekey = __build_vc_key(step_class=step_class, host=host, fact_id=fact_id)

    is_exist, *_ = try_get(step_class=step_class, host=host, fact_id=fact_id)
    if is_exist:
        raise ValueError(f"Broken cache: '{cachekey}' already exist!")

    __vc[cachekey] = val
