import logging
from playwright.sync_api import Page, Locator, expect
from config import LAST_NAME_DEFAULT, SAUCE_URL

logger = logging.getLogger(__name__)


class SauceDemoPage:
    def __init__(self, page: Page):
        self.page = page

        # Login
        self.username_input: Locator = page.locator("#user-name")
        self.password_input: Locator = page.locator("#password")
        self.login_button: Locator = page.locator("#login-button")

        # Inventory / cart
        self.add_to_cart_buttons: Locator = page.locator(".btn_inventory")
        self.cart_link: Locator = page.locator(".shopping_cart_link")
        self.checkout_button: Locator = page.locator("#checkout")

        # Checkout
        self.first_name_input: Locator = page.locator("#first-name")
        self.last_name_input: Locator = page.locator("#last-name")
        self.postal_code_input: Locator = page.locator("#postal-code")
        self.continue_button: Locator = page.locator("#continue")
        self.finish_button: Locator = page.locator("#finish")

        # Results / validation
        self.order_success_header: Locator = page.locator(".complete-header")
        self.checkout_error: Locator = page.locator('[data-test="error"]')

    def login(self, username: str, password: str) -> None:
        logger.info("Logging into SauceDemo")
        self.page.goto(SAUCE_URL)
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        expect(self.page).to_have_url(f"{SAUCE_URL}inventory.html")
        logger.info("Login successful")

    def complete_purchase(self, pet: dict) -> None:
        logger.info(f"Starting purchase with pet: {pet['name']}, id: {pet['id']}")
        self._add_to_cart()
        self._fill_checkout(
            first_name=pet["name"],
            last_name=LAST_NAME_DEFAULT,
            zip_code=str(pet["id"]),
            finish=True
        )

    def _add_to_cart(self) -> None:
        logger.info("Adding first available item to cart")
        expect(self.add_to_cart_buttons.first).to_be_visible()
        self.add_to_cart_buttons.first.click()
        self.cart_link.click()
        self.checkout_button.click()

    def _fill_checkout(self, first_name: str, last_name: str, zip_code: str, finish: bool = True) -> None:
        logger.info(f"Filling checkout: {first_name} {last_name}, zip={zip_code}")
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(zip_code)
        self.continue_button.click()

        if finish:
            expect(self.finish_button).to_be_visible()
            self.finish_button.click()

    def is_order_successful(self) -> bool:
        expect(self.order_success_header).to_be_visible()
        message = self.order_success_header.inner_text().strip()
        logger.info(f"Order message received: '{message}'")
        return "THANK YOU" in message.upper()

    def checkout_with_missing_first_name(self, pet: dict) -> None:
        logger.info("Submitting checkout without first name")
        self._add_to_cart()
        self._fill_checkout(
            first_name="",
            last_name=LAST_NAME_DEFAULT,
            zip_code=str(pet["id"]),
            finish=False
        )

    def get_checkout_error_message(self) -> str:
        expect(self.checkout_error).to_be_visible()
        message = self.checkout_error.inner_text().strip()
        logger.info(f"Checkout error message: '{message}'")
        return message