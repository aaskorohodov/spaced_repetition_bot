import ctypes
import os
import sys
import threading
import time

from typing import Optional
from infi.systray import SysTrayIcon, traybar

import bot_activator

from support.constants import BOT_TOKEN
from support.instance_checker import InstanceChecker
from thread_communicators.main_comm import MainComm


class Trayer(SysTrayIcon):
    def __init__(self):
        """Init"""

        self.logo_main: str     = ''
        self.logo_info: str     = ''
        self.logo_restart: str  = ''
        self._make_logos()

        self.menu_options: Optional[tuple[tuple[str, str, ()]]] = None
        self._make_menu_options()

        self.status = MainComm()

        super().__init__(self.logo_main, 'Suggestor', self.menu_options, on_quit=self._quit)
        self.start()

        self.run_bot(self)

    # Commands

    def run_bot(self, _: traybar.SysTrayIcon) -> None:
        """Launches TgBot

        Args:
            _: being provided by systray"""

        threading.Thread(target=self._async_run_bot).start()

    def show_status(self, _: traybar.SysTrayIcon) -> None:
        """Button 'Status' action.

        Args:
            _: being provided by systray"""

        threading.Thread(target=ctypes.windll.user32.MessageBoxW,
                         args=(0, self.status.bot_error, 'Status', 0),
                         daemon=True).start()

    def restart(self, _: traybar.SysTrayIcon) -> None:
        """Button 'Restart' action.

        Args:
            _: being provided by systray"""

        self.status.trayer_running = False
        self.tg_bot.stop()

        python = sys.executable
        os.execl(python, python, *sys.argv)

    # Actions

    def _async_run_bot(self) -> None:
        """Thread, that runs TgBot.

        Raises flag gui_running, so that only 1 instance on the process will run, and lowers it afterward."""

        bot_activator.__init__(BOT_TOKEN)
        from bot import TgBot

        self.tg_bot = TgBot(self.status)
        self.tg_bot.run()

    def _quit(self, _):
        """Custom action. Being called automatically by systray on exit.

        Args:
            _: Trayer (self's class), provided by systray"""

        self.status.trayer_running = False
        self.tg_bot.stop()
        time.sleep(1)

        # Killing GUI, if it exists
        InstanceChecker().kill_process('main_launcher')

    # Service

    def _make_logos(self) -> None:
        """Saves paths to icons"""

        self.logo_main = 'media/trayer/bot_logo_transparent.ico'
        self.logo_info = 'media/trayer/bot_info.ico'
        self.logo_restart = 'media/trayer/bot_restart.ico'

    def _make_menu_options(self) -> None:
        """Makes menu for Trayer"""

        # Меню в трее (вылазит по клику правой кнопкой). Содержит (текст, картинку, что вызвать по нажатию)
        self.menu_options = (
            ("Info", self.logo_info, self.show_status),
            ("Restart", self.logo_restart, self.restart)
        )
