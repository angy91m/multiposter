import asyncio
from sys import exit
import tkinter as tk
class CustomGui(tk.Tk):
    def __init__(self, loop, buttonCb, interval=1/120):
        super().__init__()
        self.loop = loop
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.tasks = []
        self.tasks.append(loop.create_task(self.updater(interval)))
        tk.Button(self, text ="Apri", command = buttonCb)
    async def updater(self, interval):
        while True:
            self.update()
            await asyncio.sleep(interval)

    def close(self):
        for task in self.tasks:
            task.cancel()
        self.loop.stop()
        self.destroy()
        exit(0)