import os
import logging
from utils import client
from dotenv import load_dotenv

load_dotenv()
api_token = os.getenv("token_inegi")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

denue_client = client.DenueClient(api_token)
buscar_info = denue_client.buscar("todos","21.85717833,-102.28487238","250") 
print(buscar_info)

ficha = denue_client.ficha("34185")
print(ficha)

nombre = denue_client.nombre("MARRIOTT", "1", "1", "10")
print(nombre)