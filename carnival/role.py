class Role:
    name: str = ""

    def run(self, **kwargs):
        raise NotImplementedError
