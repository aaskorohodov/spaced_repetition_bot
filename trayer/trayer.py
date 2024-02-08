import ctypes
import threading

from infi.systray import SysTrayIcon, traybar

from app_controller.coroutine_communicator import CoroutineCommunicator


class TrayerController(SysTrayIcon):
    def __init__(self, communicator: CoroutineCommunicator):
        """Init"""

        self._logo_main: str     = ''
        self._logo_info: str     = ''
        self._logo_restart: str  = ''
        self._make_logo_paths()

        self._menu_options: tuple[tuple[str, str, ()]] = self._make_menu_options()
        self.communicator: CoroutineCommunicator = communicator

        super().__init__(
            self._logo_main,
            'Suggestor',
            self._menu_options,
            on_quit=self._quit)
        self.start()

        threading.Thread(target=self._listen_communicator, daemon=True).start()

    # Actions

    def _show_status(self, _: traybar.SysTrayIcon) -> None:
        """Button 'Status' action.

        Args:
            _: being provided by systray"""

        threading.Thread(target=ctypes.windll.user32.MessageBoxW,
                         args=(0, self.communicator.bot_error, 'Status', 0),
                         daemon=True).start()

    def _restart_bot(self, _: traybar.SysTrayIcon) -> None:
        """Button 'Restart' action.

        Args:
            _: being provided by systray"""

        self.communicator.restart_request = True

    def _quit(self, _):
        """Custom action. Being called automatically by systray on exit.

        Args:
            _: Trayer (self's class), provided by systray"""

        self.communicator.quit_request = True

    # Service

    def _listen_communicator(self):
        if not self.communicator.app_running:
            self.shutdown()
            return

    def _make_logo_paths(self) -> None:
        """Saves paths to icons for trayer"""

        self._logo_main = 'media/trayer/bot_logo.ico'
        self._logo_info = 'media/trayer/bot_info.ico'
        self._logo_restart = 'media/trayer/bot_restart.ico'

    def _make_menu_options(self) -> tuple:
        """Makes menu for Trayer"""

        # Menu it tray (pops up with RMB). Contains ('Text', picture, callable if clicked)
        menu_options = (
            ("Info", self._logo_info, self._show_status),
            ("Restart", self._logo_restart, self._restart_bot)
        )

        return menu_options
