# Relatório técnico — AP6: Exploração de integridade, replicação e consenso

## 1. Objetivo

O objetivo é observar o papel do hash criptográfico no encadeamento de blocos, verificar como alterações podem ser detectadas e simular divergência entre réplicas. O experimento também destaca que validar uma cadeia isoladamente não equivale a alcançar consenso entre participantes.

## 2. Procedimento experimental

A implementação utiliza SHA-256 para calcular o hash de cada bloco a partir do índice, dos dados e do hash anterior. A cadeia contém um bloco gênesis e pelo menos 24 blocos com dados gerados usando uma semente fixa, permitindo repetir o experimento. Os resultados completos são registrados em arquivos CSV e TXT na pasta `evidencias/`.

Foram executados os seguintes cenários:

1. criação e validação da cadeia original;
2. alteração de um caractere em uma mensagem e comparação dos hashes;
3. alteração dos dados de um bloco intermediário sem atualizar seu hash;
4. recálculo do hash do bloco alterado e dos blocos posteriores;
5. criação de duas réplicas que recebem dados distintos na mesma posição;
6. avaliação de uma regra de reconciliação baseada na cadeia válida mais longa.

## 3. Resultados e análise

Os resultados numéricos devem ser consultados em `evidencias/resultados_experimentos.csv` e `evidencias/execucao.txt`, gerados pelo programa. Essa abordagem evita registrar como observação um valor que não tenha sido produzido pela execução.

### 3.1 Efeito avalanche

O SHA-256 sempre produz uma saída de 256 bits. Ao alterar um caractere da entrada, espera-se uma saída muito diferente da original. O programa calcula a quantidade de bits e bytes diferentes entre os dois hashes. Isso ilustra o efeito avalanche: uma pequena mudança na mensagem não resulta em uma pequena mudança previsível no resumo criptográfico.

### 3.2 Adulteração de bloco intermediário

O hash armazenado é comparado ao hash recalculado a partir do conteúdo atual. Quando o conteúdo é alterado sem atualizar o hash, a validação identifica a inconsistência. Como cada bloco referencia o hash anterior, a alteração também pode romper a ligação com o bloco seguinte.

### 3.3 Por que recalcular os hashes pode “consertar” a cadeia localmente?

O hash demonstra coerência entre os dados atuais e os resumos armazenados, não a veracidade dos dados. Um participante que consiga editar sua cópia pode recalcular o hash do bloco adulterado e atualizar as referências dos blocos posteriores. A cópia pode passar na validação estrutural, embora seu histórico tenha sido reescrito. Portanto, a validação local sozinha não permite concluir que os outros participantes aceitarão essa versão.

### 3.4 Réplicas divergentes e fork

As réplicas começam com o mesmo prefixo e recebem transações diferentes na próxima posição. Ambas podem ser internamente válidas, mas seus hashes finais diferem. Essa divergência é um fork didático e demonstra que integridade estrutural não escolhe, por si só, qual histórico deve prevalecer.

### 3.5 Regra de reconciliação e limitações

A regra proposta escolhe a cadeia válida mais longa. É simples de implementar e ajuda a discutir uma política de seleção, mas apresenta limitações: cadeias de mesmo tamanho geram empate; comprimento não prova legitimidade; e um atacante pode tentar construir uma cadeia artificialmente longa. Protocolos reais precisam considerar regras de consenso, participantes, validação de transações, modelo de falhas e, conforme o protocolo, trabalho acumulado, stake ou finalidade.

## 4. Respostas às questões da atividade

**1. Por que recalcular todos os hashes pode “consertar” localmente uma cadeia adulterada?**  
Porque os hashes são calculados a partir dos dados atuais. Se o participante altera o bloco e recalcula seu hash e os hashes posteriores, as referências podem voltar a ser coerentes. Isso não restaura a história original nem prova que os dados são verdadeiros.

**2. O que impede um participante de distribuir sua versão adulterada em uma rede real?**  
Não é o hash isoladamente. A aceitação depende das regras de validação e do protocolo de consenso adotado pela rede. Outros nós verificam transações e blocos segundo regras comuns e não precisam aceitar uma cópia apenas porque seus hashes são coerentes. A segurança efetiva depende do protocolo, de suas hipóteses e da distribuição de poder entre participantes.

**3. Que informação adicional um protocolo de consenso precisa considerar?**  
Precisa definir quais blocos e transações são válidos, como ordenar propostas concorrentes, como escolher entre históricos válidos, como lidar com mensagens atrasadas e falhas e quais condições tornam uma decisão aceita ou final. Os detalhes variam conforme o mecanismo de consenso.

**4. Qual relação existe entre fork e concorrência de eventos?**  
Um fork pode surgir quando participantes propõem ou recebem blocos diferentes antes de conhecer a mesma sequência de eventos. A concorrência e os atrasos de comunicação fazem com que réplicas observem ordens diferentes. O protocolo de consenso determina como resolver ou tolerar essa divergência.

## 5. Conclusão

O experimento demonstra que hashes e encadeamento ajudam a detectar alterações quando os resumos armazenados deixam de corresponder aos dados. Entretanto, uma cadeia pode ser reescrita localmente e recalculada, de modo que a consistência interna não comprova a autenticidade do histórico. A simulação de réplicas evidencia que cópias válidas podem divergir. Assim, **hash não é consenso**: hashes oferecem uma ferramenta de integridade, enquanto consenso é o mecanismo distribuído que define como participantes coordenam a aceitação de um histórico.

## 6. Reprodutibilidade

Execute `python main.py` para gerar os resultados e `python -m unittest discover -s tests -v` para executar os testes. Os valores quantitativos apresentados devem ser conferidos nos arquivos de evidência gerados.
