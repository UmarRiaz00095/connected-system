import logging
from playwright.sync_api import Page, expect
from config import LAST_NAME_DEFAULT , SAUCE_URL

logger = logging.getLogger(__name__)


class SauceDemoPage:

    def __init__(self, page: Page):
        self.page = page

    def login(self, username: str, password: str) -> None:
        logger.info(f"Logging in as '{username}'")
        self.page.goto(SAUCE_URL)
        self.page.fill("#user-name", username)
        self.page.fill("#password", password)
        self.page.click("#login-button")
        # Verify we actually landed on inventory before continuing
        expect(self.page).to_have_url(f"{SAUCE_URL}inventory.html")
        logger.info("Login successful")

    
    def complete_purchase(self, pet: dict) -> None:
        logger.info(f"Starting purchase with pet: {pet['name']}, id: {pet['id']}")
        self._add_to_cart()
        self._fill_checkout(
            first_name=pet["name"],
            last_name=LAST_NAME_DEFAULT, 
            zip_code=str(pet["id"])
        )

    
    def _add_to_cart(self) -> None:
        # Grab first available item 
        self.page.click(".btn_inventory")
        self.page.click(".shopping_cart_link")
        self.page.click("#checkout")

   
    def _fill_checkout(self, first_name: str, last_name: str, zip_code: str) -> None:
        logger.info(f"Filling checkout: {first_name} {last_name}, zip={zip_code}")
        self.page.fill("#first-name", first_name)
        self.page.fill("#last-name", last_name)
        self.page.fill("#postal-code", zip_code)
        self.page.click("#continue")
        self.page.click("#finish")

   
    def is_order_successful(self) -> bool:
        message = self.page.inner_text(".complete-header")
        logger.info(f"Order message received: '{message}'")
        return "THANK YOU" in message.upper()