from storage import Storage


def test_add_coffee_and_milk():
    db = Storage("shopping_cart_test", clear=True)
    doc = db.add_item(12345, "coffee")
    assert doc['items'] == ['coffee']
    doc = db.add_item(12345, "milk")
    assert doc['items'] == ['coffee', 'milk']
    doc = db.add_item(12345, "coffee")
    assert doc['items'] == ['coffee', 'milk']



