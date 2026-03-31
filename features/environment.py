import logging
from playwright.sync_api import sync_playwright
from config import BROWSER_HEADLESS, DEFAULT_TIMEOUT

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s"
)

logger = logging.getLogger(__name__)


def before_all(context):
    logger.info("Starting Playwright browser session")
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=BROWSER_HEADLESS)
    context.page = context.browser.new_page()
    context.page.set_default_timeout(DEFAULT_TIMEOUT)  
    logger.info("Browser session started")


def after_all(context):
    logger.info("Closing browser session")
    context.browser.close()
    context.playwright.stop()


def after_step(context, step):
    # Capture screenshot on failure — helps debug in CI where you can't see the browser
    if step.status == "failed":
        context.page.screenshot(
            path=f"screenshots/{step.name}.png"
        )