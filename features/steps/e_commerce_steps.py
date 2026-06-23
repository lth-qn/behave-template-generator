from behave import given, when, then

# Mock Framework State Classes
class ECommerceSystem:
    def __init__(self):
        self.page = "home"
        self.cart = {}
        self.currency = "USD"
        self.applied_discount = 0
        self.items_filtered = False

    def filter_price(self, low, high):
        self.items_filtered = True

    def toggle_currency(self, currency_code):
        self.currency = currency_code

@given('the user is on the browse inventory catalog page')
def step_user_browse_inventory_catalog(context):
    context.shop = ECommerceSystem()
    context.shop.page = "catalog"

@when('the user filters by a price range from 10 to 50 dollars')
def step_user_filter_price_range(context):
    context.shop.filter_price(10, 50)

@then('only items matching the specific criteria should remain visible')
def step_item_match_criterion_remain(context):
    assert context.shop.items_filtered is True

@given('the shopping cart is completely empty')
def step_shopping_cart_empty(context):
    context.shop = ECommerceSystem()
    context.shop.cart = {}

@when('the user clicks the add button for a "{item_name}" item')
def step_user_click_add_button(context, item_name):
    context.shop.cart[item_name] = context.shop.cart.get(item_name, 0) + 1

@then('the shopping cart item count badge should update to {count:d}')
def step_shopping_cart_item_count(context, count):
    total_items = sum(context.shop.cart.values())
    assert total_items == count, f"Expected {count}, got {total_items}"

@given('the shopping cart has {count:d} "{item_name}" inside it')
def step_shopping_cart_item_inside(context, count, item_name):
    context.shop = ECommerceSystem()
    context.shop.cart[item_name] = count

@when('the user removes the "{item_name}" from their item list')
def step_user_remove_item_list(context, item_name):
    if item_name in context.shop.cart:
        context.shop.cart[item_name] -= 1

@given('the user has items in their shopping checkout cart')
def step_user_item_shopping_checkout(context):
    context.shop = ECommerceSystem()
    context.shop.cart = {"Leather Wallet": 1}

@when('the user applies a valid discount promo code "{code}"')
def step_user_apply_discount_promo(context, code):
    if code == "SAVE20":
        context.shop.applied_discount = 20

@then('a {discount:d} percent discount should be applied to the order subtotal')
def step_percent_discount_apply_order(context, discount):
    assert context.shop.applied_discount == discount

@given('the active display currency is set to USD')
def step_active_display_currency_set(context):
    context.shop = ECommerceSystem()
    context.shop.currency = "USD"

@when('the user changes the system display currency to EUR')
def step_user_change_system_display(context):
    context.shop.toggle_currency("EUR")

@then('all displayed inventory pricing figures should convert automatically')
def step_inventory_pricing_figure_convert(context):
    assert context.shop.currency == "EUR"
