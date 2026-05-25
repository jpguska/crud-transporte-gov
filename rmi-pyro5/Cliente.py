import Pyro5.api

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
    opcoes = {'1': 'Trem', '2': 'Metrô', '3': 'Ônibus Articulado', '4': 'VLT', '5': 'Balsa'}
    while True:
        print("\nEscolha o Modo de Transporte (Modal):")
        for chave, valor in opcoes.items():
            print(f"  [{chave}] {valor}")
        escolha = input("Digite o número do modal (1-5): ")
        if escolha in opcoes:
            return opcoes[escolha]
        print("[ERRO] Opção inválida! Escolha um número de 1 a 5.")

def main():
    print("Iniciando cliente RMI...")
    
    # 1. Obtenção do Proxy
    crud = Pyro5.api.Proxy("PYRONAME:transporte.CRUD")
    
    input("\n[PAUSA 1 e 2] Após a chamada do proxy/nameservice. Pressione ENTER...")
    
    # Forçando o Bind explicitamente para gerar os pacotes correspondentes na rede
    crud._pyroBind()
    input("\n[PAUSA 3] Após ter chamado o método de bind no cliente. Pressione ENTER...")

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
                capacidade = ler_inteiro('Capacidade Máxima de Passageiros: ')
                extensao = ler_float('Extensão da Rota em km (use PONTO): ')
                tarifa = ler_float('Tarifa em R$ (use PONTO): ')
                
                # Criação do Dicionário
                obj_linha = {
                    'rota': rota, 'modal': modal, 'capacidade': capacidade, 
                    'extensao': extensao, 'tarifa': tarifa
                }
                
                # Chamada de método local passando parâmetros de forma natural
                id_recebido = crud.inserir(obj_linha)
                
                if id_recebido == -1 or id_recebido is None:
                    print('[ERRO] Falha ao cadastrar linha.')
                else:
                    print(f'Linha cadastrada. ID gerado: {id_recebido}')
                
                input("\n[PAUSA 4] Após execução do método INSERIR. Pressione ENTER...")

            case 'r':
                print("\n--- BUSCAR LINHA ---")
                id_busca = ler_inteiro('Digite o ID da linha para buscar: ')
                
                # Chamada do método remoto - Retorna um Objeto
                linha = crud.buscar(id_busca)
                
                if linha:
                    print(f"\n[DADOS DA LINHA {id_busca}]")
                    print(f"   Rota.......: {linha['rota']}")
                    print(f"   Modal......: {linha['modal']}")
                    print(f"   Capacidade.: {linha['capacidade']} passageiros")
                    print(f"   Extensão...: {linha['extensao']:.1f} km") 
                    print(f"   Tarifa.....: R$ {linha['tarifa']:.2f}")
                else:
                    print("[ERRO] Linha não encontrada no sistema.")
                    
                input("\n[PAUSA 4] Após execução do método BUSCAR. Pressione ENTER...")

            case 'u':
                print("\n--- ATUALIZAR LINHA ---")
                id_upd = ler_inteiro('Digite o ID da linha a ser atualizada: ')
                
                # Monta o objeto com os novos dados
                obj_linha = {
                    'rota': input('Nova Rota: '),
                    'modal': escolher_modal(),
                    'capacidade': ler_inteiro('Nova Capacidade: '),
                    'extensao': ler_float('Nova Extensão em km: '),
                    'tarifa': ler_float('Nova Tarifa em R$: ')
                }
                
                sucesso = crud.atualizar(id_upd, obj_linha)
                if sucesso:
                    print('Linha atualizada.')
                else:
                    print('[ERRO] ID não encontrado.')

            case 'd':
                print("\n--- DELETAR LINHA ---")
                id_del = ler_inteiro('Digite o ID da linha para deletar: ')
                
                sucesso = crud.deletar(id_del)
                if sucesso:
                    print('Linha deletada.')
                else:
                    print('[ERRO] ID não encontrado.')

            case 's':
                print("\nSaindo do sistema...")
                break
            
            case _:
                print("[ERRO] Opção inválida. Escolha c, r, u, d ou s.")

if __name__ == "__main__":
    main()