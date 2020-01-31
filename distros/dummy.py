from recipes.common import tell_user


def dummy_fn(message=''):
    """Just a dummy function which prints a message."""
    if not message:
        message = "Hello, this is dummy module."
    tell_user(message)