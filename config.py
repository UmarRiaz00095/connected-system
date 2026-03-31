
# NOTE: For demo purposes only — in production these would be
# loaded from a .env file using os.getenv() and never committed to Git.
SAUCE_USERNAME = "standard_user"
SAUCE_PASSWORD = "secret_sauce"




# API config
PETSTORE_BASE_URL = "https://petstore.swagger.io/v2"
MAX_RETRIES = 3
RETRY_DELAY = 1
API_TIMEOUT = 5

# UI config
SAUCE_URL = "https://www.saucedemo.com/"
BROWSER_HEADLESS = True
DEFAULT_TIMEOUT = 10000

# Test data defaults
LAST_NAME_DEFAULT = "API_User"