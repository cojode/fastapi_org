from typing import Protocol, runtime_checkable, TypeVar

T = TypeVar("T", covariant=True)


@runtime_checkable
class UseCaseProtocol(Protocol[T]):
    async def execute(self, *args, **kwargs) -> T | list[T]: ...
