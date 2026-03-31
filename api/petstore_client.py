import requests
import random , time
import logging
from config import PETSTORE_BASE_URL, MAX_RETRIES, RETRY_DELAY, API_TIMEOUT

logger = logging.getLogger(__name__)


def create_pet() -> dict:
    # Build a random pet so we're not hitting the API with the same data every run
    payload = {
        "id": random.randint(10000, 99999),
        "name": f"Pet_{random.randint(1000, 9999)}",
        "status": "available"
    }

    logger.info(f"Attempting to create pet: {payload}")

    # Public API can be flaky, retry a few times before giving up
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(
                f"{PETSTORE_BASE_URL}/pet",
                json=payload,
                timeout=API_TIMEOUT
            )
            if response.status_code == 200:
                pet = response.json()
                logger.info(f"Pet created successfully: id={pet['id']}, name={pet['name']}")
                _verify_pet_created(pet, payload)
                return pet
            else:
                logger.warning(f"Attempt {attempt}: Unexpected status {response.status_code}")
        except requests.exceptions.RequestException as e:
            # Network issues, timeouts etc log and retry
            logger.warning(f"Attempt {attempt}: Request failed — {e}")

        time.sleep(RETRY_DELAY)

    raise RuntimeError("Petstore API is unavailable after retries")


def _verify_pet_created(pet: dict, payload: dict) -> None:
    # make sure what came back matches what we sent
    assert pet["id"] == payload["id"], f"ID mismatch: {pet['id']} != {payload['id']}"
    assert pet["name"] == payload["name"], f"Name mismatch: {pet['name']} != {payload['name']}"
    logger.info("Pet creation verified successfully")