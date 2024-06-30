import os


def is_feature_enable(name: str):
    return True if name in os.environ and os.environ[name] == "True" else False
