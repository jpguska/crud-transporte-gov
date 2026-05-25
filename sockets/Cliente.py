import socket
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
endereco = ('127.0.0.1', 50000)
sock.connect(endereco)

def empacotar_dados_linha(rota, modal, capacidade, extensao, tarifa):
    rota_b = rota.encode()
    modal_b = modal.encode()
    
    msg = len(rota_b).to_bytes(1, 'big') + rota_b
    msg += len(modal_b).to_bytes(1, 'big') + modal_b
    msg += capacidade.to_bytes(4, 'big')
    msg += struct.pack('>d', extensao)
    msg += struct.pack('>d', tarifa)
    return msg

def ler_inteiro(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("[ERRO] Por favor, digite apenas números inteiros válidos.")

def ler_float(mensagem):
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("[ERRO] Por favor, digite um número válido (use PONTO para decimais).")

def escolher_modal():
    opcoes = {
        '1': 'Trem',
        '2': 'Metrô',
        '3': 'Ônibus Articulado',
        '4': 'VLT',
        '5': 'Balsa'
    }
    while True:
        print("\nEscolha o Modo de Transporte (Modal):")
        for chave, valor in opcoes.items():
            print(f"  [{chave}] {valor}")
        escolha = input("Digite o número do modal (1-5): ")
        
        if escolha in opcoes:
            return opcoes[escolha]
        print("[ERRO] Opção inválida! Escolha um número de 1 a 5.")

while True:
    print("\n" + "="*50)
    print("           SISTEMA GOVERNAMENTAL DE TRANSPORTE  ")
    print("="*50)
    opcao = input('Escolha uma opção: (c)reate, (r)ead, (u)pdate, (d)elete ou (s)air? ').lower()

    match opcao:
        case 'c':
            print("\n--- NOVO CADASTRO ---")
            rota = input('Código da Rota (Ex: L7-Rubi): ')
            
            modal = escolher_modal()
            
            capacidade = ler_inteiro('Capacidade Máxima de Passageiros (Ex: 1200): ')
            extensao = ler_float('Extensão da Rota em km (use PONTO, ex: 38.5): ')
            tarifa = ler_float('Tarifa em R$ (use PONTO, ex: 5.00): ')
            
            mensagem = opcao.encode() + empacotar_dados_linha(rota, modal, capacidade, extensao, tarifa)
            sock.send(mensagem)

            id_b = sock.recv(4)
            id_recebido = int.from_bytes(id_b, 'big', signed=True)
            if id_recebido == -1:
                print('[ERRO] Falha ao cadastrar linha.')
            else:
                print(f'Linha cadastrada. ID gerado: {id_recebido}')

        case 'r':
            print("\n--- BUSCAR LINHA ---")
            id_busca = ler_inteiro('Digite o ID da linha para buscar: ')
            mensagem = opcao.encode() + id_busca.to_bytes(4, 'big')
            sock.send(mensagem)

            status = int.from_bytes(sock.recv(1), 'big')
            if status == 1:
                tam_rota = int.from_bytes(sock.recv(1), 'big')
                rota = sock.recv(tam_rota).decode()
                
                tam_modal = int.from_bytes(sock.recv(1), 'big')
                modal = sock.recv(tam_modal).decode()
                
                capacidade = int.from_bytes(sock.recv(4), 'big')
                extensao = struct.unpack('>d', sock.recv(8))[0]
                tarifa = struct.unpack('>d', sock.recv(8))[0]

                print(f"\n[DADOS DA LINHA {id_busca}]")
                print(f"   Rota.......: {rota}")
                print(f"   Modal......: {modal}")
                print(f"   Capacidade.: {capacidade} passageiros")
                print(f"   Extensão...: {extensao:.1f} km") 
                print(f"   Tarifa.....: R$ {tarifa:.2f}")
            else:
                print("[ERRO] Linha não encontrada no sistema.")

        case 'u':
            print("\n--- ATUALIZAR LINHA ---")
            id_upd = ler_inteiro('Digite o ID da linha a ser atualizada: ')
            rota = input('Nova Rota: ')
            modal = escolher_modal()
            capacidade = ler_inteiro('Nova Capacidade: ')
            extensao = ler_float('Nova Extensão em km (usando PONTO): ')
            tarifa = ler_float('Nova Tarifa em R$ (usando PONTO): ')
            
            mensagem = opcao.encode() + id_upd.to_bytes(4, 'big') + empacotar_dados_linha(rota, modal, capacidade, extensao, tarifa)
            sock.send(mensagem)
            
            sucesso = struct.unpack('?', sock.recv(1))[0]
            if sucesso:
                print('Linha atualizada.')
            else:
                print('[ERRO] ID não encontrado.')

        case 'd':
            print("\n--- DELETAR LINHA ---")
            id_del = ler_inteiro('Digite o ID da linha para deletar: ')
            mensagem = opcao.encode() + id_del.to_bytes(4, 'big')
            sock.send(mensagem)
            
            sucesso = struct.unpack('?', sock.recv(1))[0]
            if sucesso:
                print('Linha deletada.')
            else:
                print('[ERRO] ID não encontrado.')

        case 's':
            sock.send(opcao.encode())
            sock.close()
            print("\nSaindo do sistema...")
            break
        
        case _:
            print("[ERRO] Opção inválida. Escolha c, r, u, d ou s.")