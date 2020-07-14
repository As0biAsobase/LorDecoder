import os
from server import Server
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
server1 = Server(os.getenv("VKAPI_KEY"), 196727308, "server1")

server1.start()
