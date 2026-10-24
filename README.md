# Calculadora Desktop de Equações do 2º Grau

Aplicação desktop em Python (**Tkinter** + **Matplotlib**) com design moderno em modo escuro para resolução completa de equações do 2º grau ($ax^2 + bx + c = 0$).

---

## ✨ Funcionalidades

- **Cálculo Completo de Bhaskara:**
  - Discriminante ($\Delta$) com fórmula detalhada.
  - Raízes reais distintas ($\Delta > 0$), raiz real única ($\Delta = 0$) ou raízes complexas ($\Delta < 0$).
  - Coordenadas do Vértice da parábola ($X_v, Y_v$) e análise de concavidade (ponto de máximo ou mínimo).
- **Gráfico Interativo da Parábola:**
  - Plotagem dinâmica via Matplotlib integrada ao Tkinter.
  - Destaque para o vértice e marcação visual das raízes reais nos eixos.
- **Interface Gráfica Moderna:**
  - Tema escuro personalizado.
  - Painel de resolução passo a passo formatado.
  - Validação de entradas (suporte a vírgula ou ponto decimal).

---

## 🚀 Como Executar

### Opção 1: Atalho Rápido (Recomendado no Windows)
Basta dar um duplo clique no arquivo:
```
iniciar_calculadora.bat
```

### Opção 2: Pelo Terminal / Prompt de Comando
Com o ambiente virtual ativado:
```bash
.venv\Scripts\python.exe main.py
```
Ou ativando o venv:
```bash
.venv\Scripts\activate
python main.py
```

---

## 📦 Dependências

As dependências estão listadas em `requirements.txt`:
- `matplotlib`
- `numpy`
