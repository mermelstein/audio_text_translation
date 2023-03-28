import asyncio

class Debouncer:
    def __init__(self, delay):
        self.delay = delay
        self.callback = None
        self.timer = None

    async def debounce(self, callback, *args, **kwargs):
        if self.timer:
            self.timer.cancel()

        async def delayed_call():
            await asyncio.sleep(self.delay)
            if self.callback:
                await self.callback(*args, **kwargs)

        self.callback = callback
        self.timer = asyncio.create_task(delayed_call())
