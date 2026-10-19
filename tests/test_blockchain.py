import unittest
from src.blockchain import criar_cadeia, validar_cadeia, recalcular_a_partir


class TestBlockchainDidatica(unittest.TestCase):
    def test_cadeia_valida(self):
        cadeia = criar_cadeia(["A->B:10", "B->C:3"])
        self.assertEqual(validar_cadeia(cadeia), (True, "cadeia válida"))

    def test_adulteracao_detectada(self):
        cadeia = criar_cadeia(["A->B:10", "B->C:3", "C->D:1"])
        cadeia[1].dados = "A->B:1000"
        ok, mensagem = validar_cadeia(cadeia)
        self.assertFalse(ok)
        self.assertIn("hash inválido", mensagem)

    def test_recalculo_local(self):
        cadeia = criar_cadeia(["A->B:10", "B->C:3", "C->D:1"])
        cadeia[1].dados = "A->B:1000"
        recalcular_a_partir(cadeia, 1)
        self.assertEqual(validar_cadeia(cadeia), (True, "cadeia válida"))


if __name__ == "__main__":
    unittest.main()
