from class_02.main import greet


def test_greet_returns_expected_message():
    assert greet("world") == "Hello, world!"


def test_greet_uses_given_name():
    assert greet("Ada") == "Hello, Ada!"
