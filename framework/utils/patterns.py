import unittest


class SingleToneType(type):
    def __init__(cls, name, bases, attrs, **kwds):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwds):
        if not cls.__instance:
            cls.__instance = super().__call__(*args, **kwds)
        return cls.__instance


if __name__ == "__main__":

    class A(metaclass=SingleToneType):
        a: int

        def __init__(self) -> None:
            pass

    class SingleToneTest(unittest.TestCase):
        def test__main(self):
            a = A()
            b = A()

            self.assertEqual(a, b)

    unittest.main()
