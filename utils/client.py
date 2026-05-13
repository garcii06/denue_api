import requests
import logging
logger = logging.getLogger(__name__)

class DenueClient():
    def __init__(self, token:str):
        self.base_url="https://www.inegi.org.mx/app/api/denue/v1/consulta"
        self.token=token

    def buscar(self, condicion:str, coordenadas:str, distancia:str) -> dict:
        url = f"{self.base_url}/Buscar/{condicion}/{coordenadas}/{distancia}/{self.token}"
        return self._make_request(url)
    
    def ficha(self, id:str) -> dict:
        url = f"{self.base_url}/Ficha/{id}/{self.token}"
        return self._make_request(url)

    def nombre(self, nombre_o_razon:str, entidad_federativa:str, registro_inicial:str, registro_final:str) -> dict:
        url = f"{self.base_url}/Nombre/{nombre_o_razon}/{entidad_federativa}/{registro_inicial}/{registro_final}/{self.token}"
        return self._make_request(url)

    def _make_request(self, url:str) -> dict:
        try:
            logger.info(f"Starting request to the following url:{url}")
            response = requests.get(url, timeout=3)
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

        except requests.exceptions.RequestException as e:
            logger.error(f"Request error for url {url}: {e}")
            raise