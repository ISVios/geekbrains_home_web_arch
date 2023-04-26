class FrameWorkError(Exception):
    pass


class NoNameSpaceFound(FrameWorkError):
    namespace: str

    def __init__(self, namespace: str, *args) -> None:
        self.namespace = namespace
        super().__init__(*args)


class DuplicateNameSpace(FrameWorkError):
    namespace: str

    def __init__(self, namespace: str, *args) -> None:
        self.namespace = namespace
        super().__init__(*args)


# ToDo: VVVVVVVVVVVVVVVVVVVVVVVV
class NoCorrectViewReturnType(FrameWorkError):
    # by code 100-600
    # by text
    pass


class NoFoundPathToTemplate(FrameWorkError):
    pass


class JijaError(FrameWorkError):
    # NoFoundPathToTemplate - is children
    pass
