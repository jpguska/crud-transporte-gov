import Pyro5.api
import Banco

@Pyro5.api.expose
class CRUDTransporte(object):
    def __init__(self):
        self.bd = Banco.BD()

    # Recebe um dicionário como parâmetro
    def inserir(self, obj_linha):
        # Desempacota os dados do objeto para inserir no banco
        return self.bd.inserir(
            obj_linha['rota'], 
            obj_linha['modal'], 
            obj_linha['capacidade'], 
            obj_linha['extensao'], 
            obj_linha['tarifa']
        )

    # Retorna um dicionário
    def buscar(self, id_linha):
        tupla = self.bd.buscar(id_linha)
        if tupla:
            # Retorna o registro empacotado como um objeto dicionário
            return {
                'id': tupla[0],
                'rota': tupla[1],
                'modal': tupla[2],
                'capacidade': tupla[3],
                'extensao': tupla[4],
                'tarifa': tupla[5]
            }
        return None

    # Opcionalmente recebe o objeto completo para atualização
    def atualizar(self, id_upd, obj_linha):
        return self.bd.atualizar(
            id_upd, 
            obj_linha['rota'], 
            obj_linha['modal'], 
            obj_linha['capacidade'], 
            obj_linha['extensao'], 
            obj_linha['tarifa']
        )

    def deletar(self, id_del):
        return self.bd.deletar(id_del)

def iniciar_servidor():
    daemon = Pyro5.api.Daemon()
    
    # Procura o nameservice (por padrão porta 9090)
    ns = Pyro5.api.locate_ns() 
    
    uri = daemon.register(CRUDTransporte)
    
    ns.register("transporte.CRUD", uri) 
    
    print("Servidor RMI de Transporte rodando...")
    daemon.requestLoop()

if __name__ == "__main__":
    iniciar_servidor()