import time
import random
import logging
import requests
logger = logging.getLogger(__name__)

class DenueClient():
    def __init__(self, token:str):
        self.base_url="https://www.inegi.org.mx/app/api/denue/v1/consulta"
        self.token=token

    def buscar(self, condicion:str, coordenadas:str, distancia:str) -> dict:
        logger.info(f"Starting buscar.")
        url = f"{self.base_url}/Buscar/{condicion}/{coordenadas}/{distancia}/{self.token}"
        return self._make_request(url)
    
    def ficha(self, id:str) -> dict:
        logger.info("Starting ficha.")
        url = f"{self.base_url}/Ficha/{id}/{self.token}"
        return self._make_request(url)

    def nombre(self, nombre_o_razon:str, entidad_federativa:str, registro_inicial:str, registro_final:str) -> dict:
        logger.info("Starting nombre.")
        url = f"{self.base_url}/Nombre/{nombre_o_razon}/{entidad_federativa}/{registro_inicial}/{registro_final}/{self.token}"
        return self._make_request(url)

    def _make_request(self, url:str, retries: int = 5) -> dict:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Connection": "close",
        }

        for attempt in range(retries):
            try:
                logger.info(f"Request attempt {attempt + 1}/{retries}: {url}")
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                logger.info(f"Request successful with status code: {response.status_code}")
                data = response.json()

                if not data:
                    logger.warning(f"Request for url {url} returned empty list.")
                    return []
                return data
            
            except requests.exceptions.HTTPError as e:
                logger.error(f"HTTP error for url {url}: {e}")
                raise
                #pass

            except requests.exceptions.ConnectionError as e:
                if attempt == retries - 1:
                    logger.error(f"All {retries} attempts failed for {url}: {e}")
                    raise
                wait = (2 ** attempt) + random.uniform(0, 1)
                logger.warning(f"ConnectionError (attempt {attempt + 1}/{retries}): {e}")
                time.sleep(wait)

            except requests.exceptions.Timeout as e:
                if attempt == retries - 1:
                    logger.error(f"All {retries} attempts timed out for {url}: {e}")
                    raise
                wait = (2 ** attempt) + random.uniform(0, 1)
                logger.warning(f"Timeout (attempt {attempt + 1}/{retries}): {e}")
                time.sleep(wait)


            except requests.exceptions.RequestException as e:
                logger.error(f"Request error for url {url}: {e}")
                raise