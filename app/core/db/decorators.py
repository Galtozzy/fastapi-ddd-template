from collections.abc import Awaitable, Callable
from contextvars import ContextVar
from functools import wraps
from inspect import signature
from typing import Concatenate, ParamSpec, TypeGuard, TypeVar, cast, overload

from sqlalchemy.ext.asyncio.session import AsyncSession

from app.core.db.db_config import get_async_session_maker


P = ParamSpec('P')
R = TypeVar('R')
T = TypeVar('T')


session_var = ContextVar[AsyncSession | None]('session', default=None)


def is_method(
    func: Callable[Concatenate[AsyncSession, P], Awaitable[R]]
    | Callable[Concatenate[T, AsyncSession, P], Awaitable[R]],
) -> TypeGuard[Callable[Concatenate[T, AsyncSession, P], Awaitable[R]]]:
    sig = signature(func)
    params = list(sig.parameters.values())
    return len(params) > 0 and (params[0].name == 'self' or params[0].name == 'cls')


@overload
def provide_alchemy_session[**P, R](
    _func: Callable[Concatenate[AsyncSession, P], Awaitable[R]],
) -> Callable[P, Awaitable[R]]: ...


@overload
def provide_alchemy_session[T, **P, R](
    _func: Callable[Concatenate[T, AsyncSession, P], Awaitable[R]],
) -> Callable[Concatenate[T, P], Awaitable[R]]: ...


def provide_alchemy_session(
    _func: Callable[Concatenate[AsyncSession, P], Awaitable[R]]
    | Callable[Concatenate[T, AsyncSession, P], Awaitable[R]],
) -> Callable[P, Awaitable[R]] | Callable[Concatenate[T, P], Awaitable[R]]:
    """Provides an SQLAlchemy async session to the decorated function.

    The session parameter must be positioned according to these rules:
    1. For regular functions: session must be the first parameter
    2. For methods (instance or class): session must be the second parameter, right after self/cls

    The decorator will automatically inject the session parameter, so the decorated function
    should be called without providing it.

    Args:
        _func: An async function or method that requires an SQLAlchemy session.
              Must have AsyncSession typed parameter in the correct position.

    Returns:
        A wrapped function that automatically receives a session parameter.

    Examples:
        >>> @provide_alchemy_session
        ... async def create_user(session: AsyncSession, name: str) -> User:
        ...     user = User(name=name)
        ...     session.add(user)
        ...     return user
        ...
        >>> # Call without session parameter
        >>> user = await create_user("John")

        >>> class UserRepository:
        ...     @provide_alchemy_session
        ...     async def get_user(self, session: AsyncSession, user_id: int) -> User:
        ...         return await session.get(User, user_id)
        ...
        >>> # Call without session parameter
        >>> user = await repo.get_user(1)

    Raises:
        TypeError: If the session parameter is not in the correct position or
                  if the provided arguments don't match the function signature.
    """
    sig = signature(_func)

    if is_method(_func):
        func = _func

        @wraps(func)
        async def wrapper(self: T, *args: P.args, **kwargs: P.kwargs) -> R:
            session = session_var.get()

            if session is None:
                session_maker = get_async_session_maker()
                async with session_maker() as session:
                    async with session.begin():
                        bound_args = sig.bind(self, session, *args, **kwargs)
                        bound_args.apply_defaults()

                        session_var.set(session)
                        try:
                            return await func(*bound_args.args, **bound_args.kwargs)
                        finally:
                            session_var.set(None)
            else:
                bound_args = sig.bind(self, session, *args, **kwargs)
                bound_args.apply_defaults()
                return await func(*bound_args.args, **bound_args.kwargs)

        return cast(Callable[Concatenate[T, P], Awaitable[R]], wrapper)
    else:
        narrowed_func = cast(Callable[Concatenate[AsyncSession, P], Awaitable[R]], _func)

        @wraps(narrowed_func)
        async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            session = session_var.get()

            if session is None:
                session_maker = get_async_session_maker()
                async with session_maker() as session:
                    async with session.begin():
                        bound_args = sig.bind(session, *args, **kwargs)
                        bound_args.apply_defaults()

                        session_var.set(session)
                        try:
                            return await narrowed_func(*bound_args.args, **bound_args.kwargs)
                        finally:
                            session_var.set(None)
            else:
                bound_args = sig.bind(session, *args, **kwargs)
                bound_args.apply_defaults()
                return await narrowed_func(*bound_args.args, **bound_args.kwargs)

        return cast(Callable[P, Awaitable[R]], async_wrapper)
