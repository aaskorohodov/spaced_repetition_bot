import asyncio
import threading
import time

from bot.bot import BotController


class AppController:
    def __init__(self):
        self.bot_controller = BotController()
        threading.Thread(target=self.thread_task).start()

    def thread_task(self):
        while True:
            print('Thread')
            time.sleep(1)

    async def go(self):
        await asyncio.gather(
            self.bot_controller.main(),
            self.continue_doing_something_else()
        )

    async def continue_doing_something_else(self):
        while True:
            # Your code to continue doing something else goes here
            print("Continuing to do something else...")
            await asyncio.sleep(1)
