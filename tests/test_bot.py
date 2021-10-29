from bot import get_text

def test_get_text():
    assert get_text("Random Text!") == "Random Text!"
    assert get_text("not_cat") == "That's not an existing category (warning: categories are CaSe SeNsItIvE)"
    assert get_text("am_success", 456, "Squid Game") == "456 added to Squid Game"
    assert get_text("Random Text!", wait=False) == "Random Text!"
    assert get_text("not_cat", wait=False) == "That's not an existing category (warning: categories are CaSe SeNsItIvE)"
    assert get_text("am_success", 456, "Squid Game", wait=False) == "456 added to Squid Game"
    