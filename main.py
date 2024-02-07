import asyncio

from dotenv import load_dotenv

from app_controller.app_controller import AppController


if __name__ == '__main__':
    load_dotenv()
    app_controller = AppController()
    asyncio.run(app_controller.go())
