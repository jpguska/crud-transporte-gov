# CRUD Governamental de Transporte — Sockets vs. RMI

Sistema CRUD para gestão de infraestrutura de transporte público, implementado de **duas formas distintas de comunicação em sistemas distribuídos**:

1. **Sockets TCP** com protocolo binário definido manualmente.
2. **RMI (Remote Method Invocation)** usando o middleware Pyro5.

A aplicação, a modelagem de dados e o banco são os mesmos nas duas versões. O que muda — e é justamente o ponto deste repositório — é **como cliente e servidor conversam**. Comparar as duas implementações deixa explícito o trade-off entre controle de baixo nível e abstração via middleware.

---

## Domínio da aplicação

Um CRUD governamental para gerenciar **Linhas de Transporte** público, unificando diferentes modais (trens, metrôs, ônibus articulados, VLTs e balsas).

### Modelo de dados

Banco **SQLite3**, tabela `linha_transporte` (criada automaticamente na inicialização do servidor):

| Campo        | Tipo                  | Descrição                          |
|--------------|-----------------------|------------------------------------|
| `id`         | INTEGER PRIMARY KEY   | Autoincremento                     |
| `rota`       | TEXT                  | Código da rota                     |
| `modal`      | TEXT                  | Tipo de veículo                    |
| `capacidade` | INTEGER               | Lotação máxima de passageiros      |
| `extensao`   | REAL                  | Tamanho da rota (km)               |
| `tarifa`     | REAL                  | Valor da tarifa (R$)               |

---

## As duas abordagens, lado a lado

| Aspecto                  | Sockets (Atividade 1)                                  | RMI / Pyro5 (Atividade 2)                              |
|--------------------------|--------------------------------------------------------|--------------------------------------------------------|
| Comunicação              | Socket TCP direto                                      | Invocação remota de métodos via middleware             |
| Formato dos dados        | Protocolo binário próprio (`struct`, bytes de tamanho fixo) | Serialização de dicionários Python (serpent)       |
| Controle de baixo nível  | Total — OpCode, endianness e tamanhos definidos à mão  | Abstraído pelo Pyro5                                   |
| Endianness               | Big-Endian explícito (`>` no struct, `'big'` no to_bytes) | Tratado pelo serializador                           |
| Descoberta de serviço    | Cliente conecta direto em host:porta                   | NameServer do Pyro resolve o nome para uma URI         |
| Esforço de implementação | Maior (protocolo manual)                               | Menor (chamada parece local)                           |
| Transparência            | Baixa — o desenvolvedor "vê" os bytes                  | Alta — a rede fica invisível para quem chama           |

**Resumindo o aprendizado:** a versão por socket dá controle total sobre o que trafega na rede, ao custo de definir e manter um protocolo de bytes inteiro à mão. A versão RMI troca esse controle por produtividade: o Pyro5 faz uma chamada remota parecer uma chamada de método local, escondendo serialização, endianness e localização do objeto. É o clássico trade-off entre baixo nível e middleware em sistemas distribuídos.

---

## Estrutura do repositório

```
.
├── sockets/        Implementação com sockets TCP e protocolo binário
├── rmi-pyro5/      Implementação com RMI via Pyro5
└── docs/           Documentação e capturas de tráfego (Wireshark)
```

Cada subpasta tem seu próprio README com os detalhes técnicos da implementação e instruções de execução.

---

## Como executar

Requisitos: Python 3. A versão RMI também precisa do Pyro5 (`pip install Pyro5`).

Cada versão tem instruções específicas no README da respectiva pasta:
- [`sockets/`](./sockets/README.md)
- [`rmi-pyro5/`](./rmi-pyro5/README.md)

---

## Contexto

Trabalho prático da disciplina de Sistemas Distribuídos.
Autor: João Pedro Cunha Guska — RA 2264994.
