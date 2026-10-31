"""Lesson 3: prove async behaviour with tests, not just claims."""

import asyncio
import time
from collections.abc import Awaitable, Callable

import pytest


async def fake_send(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{name} sent"


@pytest.mark.asyncio
async def test_calling_coroutine_function_returns_coroutine_not_result() -> None:
    coro = fake_send("email", 0.01)
    assert asyncio.iscoroutine(coro)
    assert await coro == "email sent"


@pytest.mark.asyncio
async def test_sequential_awaits_add_up() -> None:
    start = time.perf_counter()
    await fake_send("email", 0.3)
    await fake_send("sms", 0.3)
    assert time.perf_counter() - start >= 0.6


@pytest.mark.asyncio
async def test_gather_runs_concurrently() -> None:
    start = time.perf_counter()
    results = await asyncio.gather(
        fake_send("email", 0.3),
        fake_send("sms", 0.3),
        fake_send("push", 0.3),
    )
    elapsed = time.perf_counter() - start
    assert list(results) == ["email sent", "sms sent", "push sent"]
    assert elapsed < 0.7  # three 0.3s waits overlap, far below 0.9s


async def _heartbeat(stop: asyncio.Event) -> int:
    """Count how often the event loop gets to run this task."""
    ticks = 0
    while not stop.is_set():
        await asyncio.sleep(0.01)
        ticks += 1
    return ticks


async def _ticks_during(work: Callable[[], Awaitable[None]]) -> int:
    stop = asyncio.Event()
    heartbeat = asyncio.create_task(_heartbeat(stop))
    await asyncio.sleep(0)  # let heartbeat start
    await work()
    stop.set()
    return await heartbeat


async def _non_blocking_wait() -> None:
    await asyncio.sleep(0.2)


async def _blocking_wait() -> None:
    time.sleep(0.2)  # noqa: ASYNC251  # BAD on purpose: blocks the whole event loop


@pytest.mark.asyncio
async def test_non_blocking_wait_lets_other_tasks_run() -> None:
    assert await _ticks_during(_non_blocking_wait) >= 5


@pytest.mark.asyncio
async def test_blocking_call_freezes_event_loop() -> None:
    assert await _ticks_during(_blocking_wait) <= 2
