from dataclasses import dataclass


@dataclass
class StatResult:
    st_mode: int
    st_size: int
    st_uid: int
    st_gid: int
    st_atime: float
