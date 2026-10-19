# AP6 — Blockchain Didática: Integridade, Replicação e Consenso

**Disciplina:** Sistemas Distribuídos — OBBGSIN.037  
**Atividade:** AP6 — páginas 37 a 41 da apostila da disciplina  
**Ambiente:** Windows, Python 3.10+ e Visual Studio Code

## Objetivo

Investigar experimentalmente como o SHA-256 e o encadeamento de hashes permitem detectar adulterações, simular duas réplicas divergentes e discutir a diferença entre validação local e consenso distribuído.

## Requisitos atendidos

- [x] Criação de cadeia com mais de 20 blocos gerados de forma reproduzível.
- [x] Registro dos hashes de referência.
- [x] Alteração de um caractere e comparação dos hashes SHA-256.
- [x] Adulteração de bloco intermediário e validação da cadeia.
- [x] Recálculo local dos hashes posteriores para observar o limite da validação isolada.
- [x] Duas réplicas que recebem transações diferentes no mesmo índice.
- [x] Regra simples de reconciliação e discussão de suas limitações.
- [x] Tabela CSV, log de execução, testes automatizados e diagrama.

## 1. Preparar no Windows

Instale Python 3.10 ou superior e o VS Code. Ao instalar o Python, marque a opção **Add Python to PATH**.

1. Extraia a pasta do projeto.
2. Abra o VS Code.
3. Selecione **File > Open Folder** e abra `AP6_Blockchain_Didatica`.
4. Abra **Terminal > New Terminal**.

Confira o Python:

```powershell
python --version
```

Crie e ative um ambiente virtual (recomendado):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação, você pode usar o interpretador diretamente sem ativar o ambiente:

```powershell
.\.venv\Scripts\python.exe --version
```

O projeto usa apenas a biblioteca padrão do Python; não precisa instalar pacotes externos.

## 2. Executar os experimentos

Na raiz do projeto:

```powershell
python main.py
```

O programa cria a pasta `evidencias` com:

- `hashes_referencia.csv`: dados, hash anterior e hash de cada bloco.
- `resultados_experimentos.csv`: procedimento, objetivo e resultado de cada experimento.
- `execucao.txt`: log textual da execução.

Os dados usam uma semente fixa para facilitar a reprodução. O valor de hash é determinístico para os mesmos dados e a mesma serialização.

## 3. Executar os testes automatizados

```powershell
python -m unittest discover -s tests -v
```

Os testes verificam a cadeia válida, a detecção de adulteração e o efeito do recálculo local.

## 4. Como interpretar

1. **Efeito avalanche:** uma mudança pequena na entrada deve produzir um hash SHA-256 muito diferente. O programa mede quantos bits e bytes diferem; não presume um número exato antes de executar.
2. **Adulteração:** modificar os dados sem recalcular o hash invalida o bloco. Os blocos seguintes também podem apresentar problemas de ligação.
3. **Recálculo local:** quem controla uma cópia pode recalcular o bloco alterado e os seguintes. A cadeia pode voltar a ser internamente válida, mas isso não torna a transação verdadeira nem obriga outros participantes a aceitá-la.
4. **Réplicas divergentes:** duas cópias podem ser localmente válidas e ainda conter blocos diferentes.
5. **Reconciliação:** o exemplo usa a regra didática de escolher a cadeia válida mais longa. Se ambas tiverem o mesmo tamanho, ocorre empate. Mesmo quando uma é maior, comprimento isolado não oferece proteção suficiente contra um atacante nem substitui um protocolo de consenso.

## 5. Diagrama

O arquivo `diagrama.md` contém o diagrama Mermaid das réplicas divergentes e da decisão de reconciliação.

## 6. Git e GitHub

No terminal do VS Code:

```powershell
git init
git add .
git commit -m "Implementa AP6 de blockchain didatica"
```

Crie um repositório vazio no GitHub. Depois use a URL do seu próprio repositório:

```powershell
git branch -M main
git remote add origin URL_DO_SEU_REPOSITORIO
git push -u origin main
```

Substitua `URL_DO_SEU_REPOSITORIO` pela URL real apresentada pelo GitHub. Não inclua senhas, tokens ou credenciais no projeto.

## Entrega sugerida

Envie o link do repositório e, se o professor solicitar arquivo compactado, envie o ZIP do projeto. Mantenha as evidências geradas em `evidencias/` depois de executar os experimentos.

## Limitações

Este é um modelo didático executado em um único computador. Ele não implementa rede P2P, assinaturas digitais, mineração, Proof of Work, Proof of Stake ou consenso real. A simulação demonstra conceitos, mas não deve ser apresentada como uma blockchain de produção.
