from typing import Protocol, TypeVar, runtime_checkable

T = TypeVar("T", covariant=True)


@runtime_checkable
class UseCaseProtocol(Protocol[T]):
    async def execute(self, *args, **kwargs) -> T | list[T]: ...
