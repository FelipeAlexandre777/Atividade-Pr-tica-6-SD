# Diagrama — réplicas divergentes

```mermaid
flowchart TD
    G["Prefixo comum de blocos"] --> A["Réplica A"]
    G --> B["Réplica B"]
    A --> A1["Bloco N: Ana → Bruno"]
    B --> B1["Bloco N: Carla → Diego"]
    A1 --> VA["Validação local: válida"]
    B1 --> VB["Validação local: válida"]
    VA --> R["Regra didática: cadeia válida mais longa"]
    VB --> R
    R --> D{"Tamanhos diferentes?"}
    D -- "Sim" --> E["Seleciona a mais longa (regra simplificada)"]
    D -- "Não" --> F["Empate: regra não decide"]
```

O diagrama mostra que duas réplicas podem ter um prefixo comum e depois divergir. A validade local não resolve a divergência. A regra da cadeia mais longa é usada apenas para discussão; não constitui, isoladamente, um protocolo seguro de consenso.
