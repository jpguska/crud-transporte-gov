# Versão Sockets — Protocolo Binário sobre TCP

Implementação do CRUD de Transporte usando **sockets TCP** com um **protocolo binário definido manualmente**. Toda a serialização é feita à mão com a biblioteca `struct` do Python.

## Como executar

```bash
# Terminal 1 — servidor
python servidor.py

# Terminal 2 — cliente
python cliente.py
```

O banco SQLite (`linha_transporte`) é criado automaticamente na primeira execução do servidor, caso ainda não exista.

## Protocolo de comunicação

Cada requisição do cliente começa com um **OpCode de 1 byte** que identifica a operação:

| OpCode | Operação | Descrição              |
|--------|----------|------------------------|
| `c`    | CREATE   | Inserção               |
| `r`    | READ     | Busca por ID           |
| `u`    | UPDATE   | Atualização            |
| `d`    | DELETE   | Remoção                |
| `s`    | SAIR     | Encerra a conexão      |

### CREATE (`c`)
Cliente → Servidor: OpCode + dados da linha. Strings são precedidas por 1 byte indicando seu tamanho; números têm tamanho fixo.

| Campo       | Tamanho | Formato        | Descrição                       |
|-------------|---------|----------------|---------------------------------|
| OpCode      | 1 byte  | char (`c`)     | Identificador da operação       |
| Tam_Rota    | 1 byte  | int            | Tamanho em bytes da rota        |
| Rota        | N bytes | UTF-8          | Código da rota                  |
| Tam_Modal   | 1 byte  | int            | Tamanho em bytes do modal       |
| Modal       | M bytes | UTF-8          | Modal escolhido                 |
| Capacidade  | 4 bytes | int            | Lotação máxima                  |
| Extensão    | 8 bytes | double (`>d`)  | Km                              |
| Tarifa      | 8 bytes | double (`>d`)  | R$                              |

Servidor → Cliente: 4 bytes com o **ID gerado** (int Big-Endian com sinal). Em caso de falha, retorna `-1`.

### READ (`r`)
Cliente → Servidor: OpCode + ID (4 bytes).
Servidor → Cliente: 1 byte de status (`1` = encontrado, `0` = não encontrado). Se encontrado, segue com a mesma estrutura de dados do CREATE.

### UPDATE (`u`)
Cliente → Servidor: OpCode + ID (4 bytes) + os mesmos dados do CREATE.
Servidor → Cliente: 1 byte booleano (`struct.pack('?')`) — `True` (atualizado) ou `False` (ID não encontrado).

### DELETE (`d`)
Cliente → Servidor: OpCode + ID (4 bytes).
Servidor → Cliente: 1 byte booleano — `True` (removido) ou `False` (ID não encontrado).

### SAIR (`s`)
Cliente envia apenas o OpCode `s`. O servidor encerra o laço da conexão e fecha o socket, sem resposta.

## Endianness

Todos os números (ID, capacidade, extensão, tarifa) trafegam em **Big-Endian**, o padrão de rede, garantindo que os dados sejam interpretados corretamente entre máquinas de arquiteturas diferentes. No código isso aparece no argumento `'big'` de `to_bytes()`/`from_bytes()` e no símbolo `>` nos formatos do `struct`.

## Dados de exemplo

| ID | Rota             | Modal             | Capacidade | Extensão (km) | Tarifa (R$) |
|----|------------------|-------------------|------------|---------------|-------------|
| 1  | L11-Coral        | Trem              | 2500       | 50.8          | 5.00        |
| 2  | L4-Amarela       | Metrô             | 1500       | 12.8          | 5.00        |
| 3  | BRT-Transoeste   | Ônibus Articulado | 160        | 32.0          | 4.30        |
| 4  | VLT-Centro L1    | VLT               | 420        | 14.0          | 4.30        |
| 5  | Travessia S-G    | Balsa             | 400        | 1.5           | 3.10        |
