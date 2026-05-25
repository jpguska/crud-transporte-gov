import sqlite3

class BD:
    def __init__(self):
        self.conexao = sqlite3.connect("transporte.db")
        cursor = self.conexao.cursor()
        # 6 atributos no total (ID + 5)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS linha_transporte(
                id INTEGER PRIMARY KEY, 
                rota TEXT, 
                modal TEXT, 
                capacidade INTEGER, 
                extensao REAL, 
                tarifa REAL
            )
        """)
        self.conexao.commit()
        cursor.close()

    def inserir(self, rota, modal, capacidade, extensao, tarifa):
        cursor = self.conexao.cursor()
        cursor.execute(
            "INSERT INTO linha_transporte(rota, modal, capacidade, extensao, tarifa) VALUES (?,?,?,?,?)",
            (rota, modal, capacidade, extensao, tarifa)
        )
        id = cursor.lastrowid if cursor.rowcount > 0 else None
        self.conexao.commit()
        cursor.close()
        return id
    
    def buscar(self, id):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM linha_transporte WHERE id = ?", (id,))
        retorno = cursor.fetchone()
        cursor.close()
        return retorno

    def atualizar(self, id, rota, modal, capacidade, extensao, tarifa):
        cursor = self.conexao.cursor()
        cursor.execute(
            "UPDATE linha_transporte SET rota=?, modal=?, capacidade=?, extensao=?, tarifa=? WHERE id=?",
            (rota, modal, capacidade, extensao, tarifa, id)
        )
        self.conexao.commit()
        sucesso = cursor.rowcount > 0
        cursor.close()
        return sucesso

    def deletar(self, id):
        cursor = self.conexao.cursor()
        cursor.execute("DELETE FROM linha_transporte WHERE id = ?", (id,))
        self.conexao.commit()
        sucesso = cursor.rowcount > 0
        cursor.close()
        return sucesso