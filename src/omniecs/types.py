from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Protocol, TypeVar, TypeVarTuple


@dataclass(slots=True, frozen=True)
class EntityId:
    value: int


class Component: ...


class Bundle(Protocol):
    def components(self) -> Iterable[Component]: ...

    
class ExecutionStage(Enum):
    reset = 0
    update = 1
    cleanup = 2


class Resource: ...


class Event: ...


@dataclass(kw_only=True)
class DrawCommand:
    global_layer: int
    local_layer: int = 0


R = TypeVar("R", bound=Resource)
Cs = TypeVarTuple("Cs")
