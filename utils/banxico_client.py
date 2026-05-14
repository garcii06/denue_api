import time
import random
import logging
import requests
logger = logging.getLogger(__name__)

class BanxicoClient():
    def __init__(self, token:str):
        self.base_url="https://www.banxico.org.mx/SieAPIRest/service/v1/series/"
        self.token=token

    def serie(self, id_series:list[str]) -> dict:
        series = ",".join(id_series)
        url = f"{self.base_url}{series}"
        return self._make_request(url)

    def serie_datos(self, id_series:list[str]) -> dict:
        series = ",".join(id_series)
        url = f"{self.base_url}{series}/datos"
        return self._make_request(url)

    def serie_datos_oportuno(self, id_series:list[str]) -> dict:
        series = ",".join(id_series)
        url = f"{self.base_url}{series}/datos/oportuno"
        return self._make_request(url)

    def serie_datos_fechas(self, id_series:list[str], fechaIni:str, fechaFin:str) -> dict:
        series = ",".join(id_series)
        url = f"{self.base_url}{series}/datos/{fechaIni}/{fechaFin}"
        return self._make_request(url)

    def _make_request(self, url:str, retries: int = 5) -> dict:
        self.headers={
            "User-Agent": "Mozilla/5.0",
            "Connection": "close",
        }

        self.params={
            "token": self.token,
            "mediaType": "json",
            "locale": "es"
        }

        for attempt in range(retries):
            try:
                logger.info(f"Request attempt {attempt + 1}/{retries}: {url}")
                response = requests.get(url, headers=self.headers, params=self.params)
                response.raise_for_status()
                logger.info(f"Request successful with status code: {response.status_code}")
                data = response.json()

                if not data:
                    logger.warning(f"Request for url {url} returned empty dict.")
                    return {}
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