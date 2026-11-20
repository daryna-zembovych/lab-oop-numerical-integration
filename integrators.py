"""Модуль реалізації класів чисельного інтегрування."""


class BaseIntegrator:
    """Базовий клас для чисельного обчислення визначених інтегралів."""

    order = 1
    method_name = "Базовий метод"

    def __init__(self, func, a, b):
        """Ініціалізує підінтегральну функцію та межі інтегрування."""
        self.func = func
        self.a = a
        self.b = b

    @classmethod
    def from_dict(cls, func, params):
        """Альтернативний конструктор для створення інтегратора зі словника."""
        return cls(func, params['a'], params['b'])

    @staticmethod
    def validate_bounds(a, b):
        """Перевіряє коректність меж інтегрування."""
        return a < b

    def integrate(self, n):
        """Обчислює наближене значення інтеграла для n розбиттів."""
        raise NotImplementedError

    def adaptive_integrate(self, eps=1e-4, initial_n=2):
        """Знаходить інтеграл із заданою точністю eps за правилом Рунге."""
        if initial_n >= 2 and initial_n % 2 == 0:
            n = initial_n
        else:
            n = 2

        i_h = self.integrate(n)

        while True:
            n_2 = n * 2
            i_h2 = self.integrate(n_2)
            delta = abs(i_h2 - i_h) / (2 ** self.order - 1)

            if delta <= eps:
                i_refined = i_h2 + (i_h2 - i_h) / (2 ** self.order - 1)
                return i_refined, n_2, delta

            n = n_2
            i_h = i_h2


    def __str__(self):
        """Повертає рядкове представлення об'єкта інтегратора."""
        return (f'{self.method_name} (порядок О(h^{self.order})) на відрізку [{self.a}; {self.b}]')


class RectangleIntegrator(BaseIntegrator):
    """Обчислення інтеграла складеною формулою середніх прямокутників."""

    order = 2
    method_name = "Формула прямокутників"

    def __init__(self, func, a, b):
        super().__init__(func, a, b)

    def integrate(self, n):
        h = (self.b - self.a) / n
        suma = sum(self.func(self.a + (i+0.5)*h) for i in range(n))
        return h*suma


class TrapezoidIntegrator(BaseIntegrator):
    """Обчислення інтеграла складеною формулою трапецій."""

    order = 2
    method_name = "Формула трапецій"

    def __init__(self, func, a, b):
        super().__init__(func, a, b)

    def integrate(self, n):
        h = (self.b - self.a) / n
        inner_sum = sum(self.func(self.a + i * h) for i in range(1, n))
        return h * (0.5 * (self.func(self.a) + self.func(self.b)) + inner_sum)


class SimpsonIntegrator(BaseIntegrator):
    """Обчислення інтеграла складеною формулою Сімпсона."""

    order = 4
    method_name = "Формула Сімпсона"

    def __init__(self, func, a, b):
        super().__init__(func, a, b)

    def integrate(self, n):
        h = (self.b - self.a) / n
        odd_sum = sum(self.func(self.a + i * h) for i in range(1, n, 2))
        even_sum = sum(self.func(self.a + i * h) for i in range(2, n, 2))
        return (h / 3.0) * (self.func(self.a) + self.func(self.b) + 4.0 * odd_sum + 2.0 * even_sum)
