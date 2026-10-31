"""Lesson 3 demo: sequential awaits vs asyncio.gather."""

import asyncio
import time


async def fake_send(name: str, delay: float) -> str:
    await asyncio.sleep(delay)  # pretend network wait
    return f"{name} sent"


async def sequential() -> None:
    start = time.perf_counter()
    print(await fake_send("email", 1))
    print(await fake_send("sms", 1))
    print(f"sequential: {time.perf_counter() - start:.1f}s")


async def concurrent() -> None:
    start = time.perf_counter()
    results = await asyncio.gather(fake_send("email", 1), fake_send("sms", 1))
    print(results)
    print(f"concurrent: {time.perf_counter() - start:.1f}s")


if __name__ == "__main__":
    asyncio.run(sequential())
    asyncio.run(concurrent())
