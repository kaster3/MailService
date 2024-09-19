import os

from dotenv import load_dotenv

bind = "0.0.0.0:8001"
# по максимуму использовать процесс это кол-во логических ядер умножить на 2 и + 1
workers = 1

env = os.path.join(os.getcwd(), f".env")

if os.path.exists(env):
    print(env)
    load_dotenv(env)


