"""Головний модуль запуску чисельного інтегрування."""

import math

from integrators import (
    RectangleIntegrator,
    SimpsonIntegrator,
    TrapezoidIntegrator,
)


def target_function(x):
    """Підінтегральна функція згідно з індивідуальним варіантом."""
    return math.sin(x + x**3)


def main():
    """Точка входу програми."""
    params = {'a': 0.0, 'b': 1.0}
    eps = 0.5e-4

    integrators = [RectangleIntegrator.from_dict(target_function, params),
        TrapezoidIntegrator.from_dict(target_function, params),
        SimpsonIntegrator.from_dict(target_function, params)]

    with open('results.txt', 'w') as file:
        for e in (eps, eps*0.1):
            print(f'eps = {e}')
            print('-' * 40)
            file.write(f'eps = {e}\n')
            file.write('-' * 40 + '\n')

            for i in integrators:
                file.write(f'{i}\n')
                print(i)
                i_refined, min_n, delta = i.adaptive_integrate(e)

                n = 2
                while n <= min_n:
                    file.write(f'n = {n} -> I = {i.integrate(n):.6f}\n')
                    n *= 2
                file.write(f'Уточнений результат: {i_refined:.6f} (n_min = {min_n}, похибка = {e:.6f})\n\n')
                print(f'Уточнений результат: {i_refined:.6f} (n_min = {min_n}, похибка = {e:.6f})\n')
            file.write('='*60+'\n')
            print('='*60)

    print('Протокол ітерацій збережено та записано у файл results.txt')


if __name__ == "__main__":
    main()
