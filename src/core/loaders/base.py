class LoaderError(Exception):
    pass


class Loader:

    def load(self):
        raise NotImplementedError
