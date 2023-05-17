import abc
import unittest


class SingleToneType(type):
    def __init__(cls, name, bases, attrs, **kwds):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwds):
        if not cls.__instance:
            cls.__instance = super().__call__(*args, **kwds)
        return cls.__instance


class Notifier(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self._log_list = []

    def notify(self, addres, subject, messages):
        self._login()
        self._send(addres, subject, messages)
        self._logout()
        self._log(addres, subject, messages)

    @abc.abstractmethod
    def _login(self):
        pass

    @abc.abstractmethod
    def _send(self, addres, subject, messages):
        pass

    @abc.abstractmethod
    def _logout(self):
        pass

    def _log(self, addres, subject, messages):
        self._log_list.append((addres, subject, messages))


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
