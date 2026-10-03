"""Módulo 10 - os mesmos tipos de teste com unittest, que já vem com o Python.

O pytest também executa testes escritos com unittest, então este arquivo
roda junto com os demais em ``make test``. Sem pytest, rode:
    uv run python -m unittest tests.unit.test_10_testes_unittest -v

Fonte: https://docs.python.org/pt-br/3/library/unittest.html
"""

from __future__ import annotations

import unittest

from tests._helpers import carregar_exemplo


class TestCalculadora(unittest.TestCase):
    def setUp(self) -> None:
        # setUp roda antes de CADA teste (o papel da fixture no pytest).
        self.calc = carregar_exemplo("10_testes", "calculadora")

    def test_somar(self) -> None:
        self.assertEqual(self.calc.somar(2, 3), 5)

    def test_somar_floats(self) -> None:
        self.assertAlmostEqual(self.calc.somar(0.1, 0.2), 0.3)

    def test_dividir_por_zero(self) -> None:
        with self.assertRaises(ZeroDivisionError):
            self.calc.dividir(1, 0)

    def test_situacao(self) -> None:
        # subTest: como o parametrize do pytest; cada caso é relatado separadamente.
        for nota, esperado in [(4.99, "reprovado"), (5, "recuperação"), (7, "aprovado")]:
            with self.subTest(nota=nota):
                self.assertEqual(self.calc.situacao(nota), esperado)


if __name__ == "__main__":
    unittest.main()
