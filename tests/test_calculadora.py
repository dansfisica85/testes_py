import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
import zipfile

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import numpy as np

from main import BhaskaraApp
import gerar_zip


class CalculadoraTests(unittest.TestCase):
    def setUp(self):
        # Os controles são simulados; cálculo e renderização Matplotlib são reais.
        self.app = BhaskaraApp.__new__(BhaskaraApp)
        self.app.entry_a = Mock()
        self.app.entry_b = Mock()
        self.app.entry_c = Mock()
        self.app.mostrar_texto = Mock()
        self.app.fig = Figure()
        self.app.ax = self.app.fig.add_subplot(111)
        self.app.canvas = FigureCanvasAgg(self.app.fig)
        self.erro = self.enterContext(patch("main.messagebox.showerror"))
        self.aviso = self.enterContext(patch("main.messagebox.showwarning"))

    def calcular(self, a, b, c):
        for entrada, valor in zip(
            (self.app.entry_a, self.app.entry_b, self.app.entry_c), (a, b, c)
        ):
            entrada.get.return_value = str(valor)
        self.app.calcular()

    def texto(self):
        return self.app.mostrar_texto.call_args.args[0]

    def test_duas_raizes_e_grafico(self):
        self.calcular(1, -5, 6)
        self.assertIn("= 3.0000", self.texto())
        self.assertIn("= 2.0000", self.texto())
        self.assertIn("Vértice V(2.50, -0.25)", self.texto())
        pontos = self.app.ax.collections[-1].get_offsets()
        np.testing.assert_allclose(pontos, [[3, 0], [2, 0]])
        curva = self.app.ax.lines[-1]
        x, y = curva.get_data()
        np.testing.assert_allclose(y, x*x - 5*x + 6)
        self.erro.assert_not_called()

    def test_raiz_dupla(self):
        self.calcular(1, -4, 4)
        self.assertIn("x₁ = x₂ = 2.0000", self.texto())
        np.testing.assert_allclose(self.app.ax.collections[-1].get_offsets(), [[2, 0]])

    def test_raizes_complexas(self):
        self.calcular(1, 0, 1)
        self.assertIn("x₁ = -0 + 1i", self.texto())
        self.assertIn("x₂ = -0 - 1i", self.texto())
        self.assertEqual(len(self.app.ax.collections), 1)

    def test_virgula_decimal(self):
        self.calcular("0,5", "-2,5", "3")
        self.assertIn("= 3.0000", self.texto())
        self.assertIn("= 2.0000", self.texto())

    def test_concavidade_negativa(self):
        self.calcular(-1, 0, 4)
        self.assertIn("Ponto de Máximo", self.texto())
        self.assertIn("Vértice V(0.00, 4.00)", self.texto())

    def test_a_zero(self):
        self.calcular(0, 1, 2)
        self.aviso.assert_called_once()
        self.app.mostrar_texto.assert_not_called()

    def test_entradas_invalidas(self):
        for coeficientes in [("", 1, 1), ("abc", 1, 1), ("nan", 1, 1),
                             (1, "inf", 1), (1, 1, "-inf"),
                             (1, "1e309", 1), (1, "1e200", 1),
                             ("1e308", 1, 1)]:
            with self.subTest(coeficientes=coeficientes):
                self.erro.reset_mock()
                self.calcular(*coeficientes)
                self.erro.assert_called_once()
        self.app.mostrar_texto.assert_not_called()

    def test_overflow_do_grafico_preserva_resultado_anterior(self):
        self.calcular(1, -5, 6)
        texto_anterior = self.texto()
        self.calcular("1e-300", 1, 0)
        self.erro.assert_called_once()
        self.assertEqual(self.texto(), texto_anterior)

    def test_limpar(self):
        with patch.object(self.app, "calcular") as calcular:
            self.app.limpar()
        for entrada, valor in zip(
            (self.app.entry_a, self.app.entry_b, self.app.entry_c), ("1", "0", "0")
        ):
            entrada.delete.assert_called_once()
            entrada.insert.assert_called_once_with(0, valor)
        calcular.assert_called_once()


class PacoteTests(unittest.TestCase):
    def test_zip_publicado_contem_fontes_atuais(self):
        raiz = Path(__file__).resolve().parents[1]
        with zipfile.ZipFile(raiz / "calculadora_bhaskara.zip") as pacote:
            self.assertIsNone(pacote.testzip())
            self.assertEqual(set(pacote.namelist()), {
                "main.py", "requirements.txt", "README.md", "iniciar_calculadora.bat"
            })
            for nome in pacote.namelist():
                self.assertEqual(
                    pacote.read(nome).replace(b"\r\n", b"\n"),
                    (raiz / nome).read_bytes().replace(b"\r\n", b"\n"), nome
                )

    def test_empacotador_nao_substitui_zip_se_faltar_arquivo(self):
        with tempfile.TemporaryDirectory() as pasta:
            destino = Path(pasta) / "calculadora_bhaskara.zip"
            destino.write_bytes(b"pacote anterior")
            with patch.object(gerar_zip, "__file__", str(Path(pasta) / "gerar_zip.py")):
                with self.assertRaises(FileNotFoundError):
                    gerar_zip.criar_pacote_zip()
            self.assertEqual(destino.read_bytes(), b"pacote anterior")

    def test_empacotador_inclui_todos_os_arquivos(self):
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            nomes = ("main.py", "requirements.txt", "README.md", "iniciar_calculadora.bat")
            for nome in nomes:
                (raiz / nome).write_text(nome, encoding="utf-8")
            with patch.object(gerar_zip, "__file__", str(raiz / "gerar_zip.py")):
                with contextlib.redirect_stdout(io.StringIO()):
                    destino = gerar_zip.criar_pacote_zip()
            with zipfile.ZipFile(destino) as pacote:
                for nome in nomes:
                    self.assertEqual(pacote.read(nome), nome.encode("utf-8"))


if __name__ == "__main__":
    unittest.main()
