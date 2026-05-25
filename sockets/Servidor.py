import socket
import struct
import Banco

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
endereco = ('127.0.0.1', 50000)

bd = Banco.BD()
sock.bind(endereco)
sock.listen()

print("Servidor de Transporte Governamental rodando...")
[dados, _] = sock.accept()

while True:
    opcode = dados.recv(1)
    if not opcode:
        break
    
    opcode = opcode.decode()
    match opcode:
        case 'c':
            # Recebendo os dados na ordem do protocolo
            tam_rota = int.from_bytes(dados.recv(1), 'big')
            rota = dados.recv(tam_rota).decode()
            
            tam_modal = int.from_bytes(dados.recv(1), 'big')
            modal = dados.recv(tam_modal).decode()
            
            capacidade = int.from_bytes(dados.recv(4), 'big')
            extensao = struct.unpack('>d', dados.recv(8))[0]
            tarifa = struct.unpack('>d', dados.recv(8))[0]

            id_inserido = bd.inserir(rota, modal, capacidade, extensao, tarifa)
            if id_inserido is None:
                 id_inserido = -1

            mensagem = id_inserido.to_bytes(4, 'big', signed=True)
            dados.send(mensagem)

        case 'r':
            id_busca = int.from_bytes(dados.recv(4), 'big')
            tupla = bd.buscar(id_busca)
            
            if tupla:
                rota, modal, capacidade, extensao, tarifa = tupla[1], tupla[2], tupla[3], tupla[4], tupla[5]
                
                rota_b = rota.encode()
                modal_b = modal.encode()
                
                # Resposta começa com byte 1 (Encontrado)
                mensagem = (1).to_bytes(1, 'big')
                mensagem += len(rota_b).to_bytes(1, 'big') + rota_b
                mensagem += len(modal_b).to_bytes(1, 'big') + modal_b
                mensagem += capacidade.to_bytes(4, 'big')
                mensagem += struct.pack('>d', extensao)
                mensagem += struct.pack('>d', tarifa)
            else:
                # Resposta começa com byte 0 (Não Encontrado)
                mensagem = (0).to_bytes(1, 'big')
                
            dados.send(mensagem)

        case 'u':
            id_upd = int.from_bytes(dados.recv(4), 'big')
            
            tam_rota = int.from_bytes(dados.recv(1), 'big')
            rota = dados.recv(tam_rota).decode()
            
            tam_modal = int.from_bytes(dados.recv(1), 'big')
            modal = dados.recv(tam_modal).decode()
            
            capacidade = int.from_bytes(dados.recv(4), 'big')
            extensao = struct.unpack('>d', dados.recv(8))[0]
            tarifa = struct.unpack('>d', dados.recv(8))[0]

            sucesso = bd.atualizar(id_upd, rota, modal, capacidade, extensao, tarifa)
            dados.send(struct.pack('?', sucesso)) # Envia 1 byte booleano

        case 'd':
            id_del = int.from_bytes(dados.recv(4), 'big')
            sucesso = bd.deletar(id_del)
            dados.send(struct.pack('?', sucesso))

        case 's':
            print("Cliente encerrou a conexão.")
            break