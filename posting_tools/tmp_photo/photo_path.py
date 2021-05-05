def get_filepath() -> str:
    path = str(__file__).split('/')[0:-1]
    return '/'.join(path)
