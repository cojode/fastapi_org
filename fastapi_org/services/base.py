from typing import Any, Protocol, TypeVar, runtime_checkable

T_co = TypeVar("T_co", covariant=True)


@runtime_checkable
class UseCaseProtocol(Protocol[T_co]):

    async def execute(self, *args: Any, **kwargs: Any) -> T_co | list[T_co]: ...
