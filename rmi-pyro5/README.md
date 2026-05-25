# Versão RMI — Pyro5

Implementação do mesmo CRUD de Transporte usando **RMI (Remote Method Invocation)** com o middleware **Pyro5**. Em vez de um protocolo de bytes manual, o cliente invoca métodos do servidor como se fossem locais, e o Pyro5 cuida de serialização, transporte e localização do objeto.

## Como executar

Requisito: `pip install Pyro5`

```bash
# Terminal 1 — serviço de nomes do Pyro
python -m Pyro5.nameserver

# Terminal 2 — servidor (registra o objeto remoto no NameServer)
python servidor.py

# Terminal 3 — cliente
python cliente.py
```

O banco SQLite (`linha_transporte`) é criado automaticamente na inicialização do servidor.

## Arquitetura

O servidor expõe um **objeto remoto** contendo a lógica de negócio do CRUD, registrado no **NameServer** do Pyro sob um nome lógico (`joaoguska.CRUD`). O cliente faz um *lookup* desse nome para obter a URI do objeto e, a partir daí, chama os métodos remotamente.

A transferência de dados é feita por **serialização de dicionários Python**, sem necessidade de definir protocolos de bytes fixos. O serializador usado é o **serpent**, que converte os objetos em um formato textual seguro para tráfego TCP. Isso é a principal diferença em relação à versão por socket: aqui a camada de transporte fica abstraída pelo middleware.

## Análise de tráfego (Wireshark)

A comunicação foi capturada na interface de *loopback* com `tcpdump` (Linux/WSL) e inspecionada no Wireshark. As capturas estão em [`../docs/wireshark/`](../docs/wireshark/).

As etapas observadas:

1. **Handshake** — three-way handshake TCP (SYN, SYN-ACK, ACK) seguido do pacote `hello` do Pyro. O servidor responde com os dados da interface, expondo os métodos remotos disponíveis. O NameServer opera por padrão na porta **9090**.
2. **Resolução de nomes** — o cliente invoca `lookup` solicitando o endereço associado a `joaoguska.CRUD`. O NameServer retorna a URI completa, indicando o objeto remoto no `localhost` em uma porta dinâmica (ex.: 33813).
3. **Invocação do método** — na chamada de `inserir`, o payload do pacote TCP contém o identificador do método e os parâmetros serializados em serpent (ex.: rota `R4-Vermelha`, modal `Trem`, capacidade `1200`), demonstrando a abstração de transporte do middleware.

## Operações do CRUD

| Método      | Operação | Descrição                          |
|-------------|----------|------------------------------------|
| `inserir`   | CREATE   | Insere uma linha e retorna o ID    |
| `buscar`    | READ     | Retorna os dados de uma linha      |
| `atualizar` | UPDATE   | Atualiza os dados de uma linha     |
| `remover`   | DELETE   | Remove uma linha pelo ID           |

> Ajuste os nomes dos métodos acima caso no seu código eles estejam diferentes.
