from behave import given, when, then
from api.petstore_client import create_pet
from ui.sauce_pages import SauceDemoPage
from config import SAUCE_USERNAME, SAUCE_PASSWORD


@given("a new pet is created in the inventory system")
def step_create_pet(context):
    context.pet = create_pet()


@when("the user logs into the storefront")
def step_login(context):
    context.sauce = SauceDemoPage(context.page)
    context.sauce.login(SAUCE_USERNAME, SAUCE_PASSWORD)


@when("the user completes a checkout using the pet data")
def step_checkout(context):
    context.sauce.complete_purchase(context.pet)


@when("the user submits checkout without a first name")
def step_missing_first_name(context):
    context.sauce.checkout_with_missing_first_name(context.pet)


@then("the order should be completed successfully")
def step_verify(context):
    assert context.sauce.is_order_successful()


@then("a validation message should be shown")
def step_validate_error(context):
    message = context.sauce.get_checkout_error_message()
    assert "First Name is required" in message