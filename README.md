# Simulador de Fila em um Posto Bancário

## Ambiente

- Crie um venv: `python -m venv venv`
- Ative o venv: `source ./venv/bin/activate` (Linux) ou `.\venv\Scripts\activate.bat` (Windows)
- Instale as dependências: `pip install -r requirements.txt`

## Configuração

Caso desejado, altere os parâmetros de simulação no arquivo `simulacao.py`, os parâmetros padrão são:

```python
SEED = 57  # seed para gerar seeds para as simulações
NUM_CAIXAS = 4  # número de caixas no banco
NUM_SIMS = 1000  # número de simulações
TEMPO_MAX = 18000  # 10h às 15h, em segundos
```

## Execução

- `python simulacao_single.py` para rodar a uma única simulação de fila
- `python simulacao.py` para rodar múltiplas simulações de fila e obter a média dos resultados
