import random
from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):

        self.driver.close()

    ## Criar ##
  
    def criarUsuario(self):
        with self.driver.session(database="neo4j") as session:
            session.execute_write(self._usuario)

    @staticmethod
    def _usuario(db):
        query = ("CREATE (object: usuario {nome: $nomeUsu, email: $emailUsu, cpf: $cpfUsu, estado: $estadoUsu, cidade: $cidadeUsu, rua: $ruaUsu, numero: $numeroUsu})")

        nomeUsu = input("Nome: ")
        emailUsu = input("Email: ")
        cpfUsu = input("CPF: ")
        print("\n---- Endereço ----")
        estadoUsu = input("Estado: ")
        cidadeUsu = input("Cidade: ")
        ruaUsu = input("Rua: ")
        numeroUsu = input("Número: ")

        result = db.run(query, nomeUsu=nomeUsu, emailUsu=emailUsu, cpfUsu=cpfUsu, estadoUsu=estadoUsu, cidadeUsu=cidadeUsu, ruaUsu=ruaUsu, numeroUsu=numeroUsu)

        print("Usuário criado com sucesso!")
        return [{"object": row["object"]["nome"]["email"]["cpf"]["estado"]["cidade"]["rua"]["numero"]} for row in result]


    def criarVendedor(self):
        with self.driver.session(database="neo4j") as session:
            session.execute_write(self._vendedor)

    @staticmethod
    def _vendedor(db):
        query = ("CREATE (object: vendedor {nome: $nomeVend, email: $emailVend, cnpj: $cnpjVend})")

        nomeVend = input("Nome: ")
        emailVend = input("Email: ")
        cnpjVend = input("CNPJ: ")
    
        result = db.run(query, nomeVend=nomeVend, emailVend=emailVend, cnpjVend=cnpjVend)

        print("Vendedor criado com sucesso!")
        return [{"object": row["object"]["nome"]["email"]["cnpj"]} for row in result]

    def criarProduto(self):
        with self.driver.session(database="neo4j") as session:
            session.execute_write(self._produto)

    @staticmethod
    def _produto(db):
        query = ("CREATE (object: produto {nome: $nomeProduto, descricao: $descricaoProduto, preco: $precoProduto, vendedor: $emailVendedor})")

        nomeProduto = input("Nome: ")
        descricaoProduto = input("Descrição: ")
        precoProduto = input("Preço: ")
        emailVendedor = input("Email do vendedor: ")

        result = db.run(query, nomeProduto=nomeProduto, descricaoProduto=descricaoProduto, precoProduto=precoProduto, emailVendedor=emailVendedor)

        print("Produto criado com sucesso!")
        return [{"object": row["object"]["nome"]["descricao"]["preco"]["vendedor"]} for row in result]

    def realizarCompra(self):
        with self.driver.session(database="neo4j") as session:
            session.execute_write(self._compra)

    @staticmethod
    def _compra(db):

        query = ("CREATE (object: compra {id: $idCompra,produto: $nomeProduto,vendedor: $emailVendedor, usuario: $emailUsuario})")

        idCompra = str(random.randint(1, 100000))
        nomeProduto = input("Nome do produto: ")
        emailVendedor = input("Email do vendedor: ")
        emailUsuario = input("Email do usuário: ")

        result = db.run(query, idCompra=idCompra, nomeProduto=nomeProduto, emailVendedor=emailVendedor, emailUsuario=emailUsuario)

        print("Compra criada com sucesso!")
        return [{"object": row["object"]["id"]["produto"]["vendedor"]["usuario"]} for row in result]
    

    ## Procurar todos ##

    def procurarUsuarios(self):
        with self.driver.session(database="neo4j") as session:
            session.read_transaction(self._usuarios)

    @staticmethod
    def _usuarios(db):
        query = "MATCH (u:usuario) RETURN u"
        result = db.run(query)
        return [print([row]) for row in result]


    def procurarVendedores(self):
        with self.driver.session(database="neo4j") as session:
            session.read_transaction(self._vendedores)

    @staticmethod
    def _vendedores(db):
        query = "MATCH (v:vendedor) RETURN v"
        result = db.run(query)
        return [print([row]) for row in result]

    def procurarProdutos(self):
        with self.driver.session(database="neo4j") as session:
            session.read_transaction(self._produtos)

    @staticmethod
    def _produtos(db):
        query = "MATCH (p:produto) RETURN p"
        result = db.run(query)
        return [print([row]) for row in result]

    def procurarCompras(self):
        with self.driver.session(database="neo4j") as session:
            session.read_transaction(self._compras)

    @staticmethod
    def _compras(db):
        query = "MATCH (c:compra) RETURN c"
        result = db.run(query)
        return [print([row]) for row in result]

    
    ## Procurar Um ##

    def procurarUsuario(self):
        with self.driver.session(database="neo4j") as session:
            session.read_transaction(self._lerUsuario)
    
    @staticmethod
    def _lerUsuario(db):
        emailUsuario = input("Insira o email do usuário: ")
        query = "MATCH (u:usuario) WHERE u.email = $emailUsuario RETURN u"
        result = db.run(query, emailUsuario=emailUsuario)
        return [print([row]) for row in result]


    def procurarVendedor(self):
        with self.driver.session(database="neo4j") as session:
            session.read_transaction(self._lerVendedor)
    
    @staticmethod
    def _lerVendedor(db):
        emailVendedor = input("Insira o email do vendedor: ")
        query = "MATCH (v:vendedor) WHERE v.email = $emailVendedor RETURN v"
        result = db.run(query, emailVendedor=emailVendedor)
        return [print([row]) for row in result]


    def procurarProduto(self):
        with self.driver.session(database="neo4j") as session:
            session.read_transaction(self._lerProduto)
    
    @staticmethod
    def _lerProduto(db):
        nomeProduto = input("Insira o nome do produto que deseja encontrar: ")
        query = "MATCH (p:produto) WHERE p.nome = $nomeProduto RETURN p"
        result = db.run(query, nomeProduto=nomeProduto)
        return [print([row]) for row in result]


    def procurarCompra(self):
        with self.driver.session(database="neo4j") as session:
            session.read_transaction(self._lerCompra)
    
    @staticmethod
    def _lerCompra(db):
        emailUsuario = input("Insira o email do usuario da compra: ")
        query = "MATCH (c:compra) WHERE c.usuario = $emailUsuario RETURN c"
        result = db.run(query, emailUsuario=emailUsuario)
        return [print([row]) for row in result]


    ## Atualizar ##

    def atualizarUsuario(self):
        with self.driver.session(database="neo4j") as session:
            session.execute_write(self._atlUsuario)

    @staticmethod
    def _atlUsuario(db):
        emailUsuario = input("Insira o email do usuário: ")
        
        print('''
                1 - Nome
                2 - Email
                3 - CPF
                4 - Rua
                5 - Número
                6 - Cidade
                7 - Estado
            ''')
        
        escolha = input("Digite o que deseja atualizar: ")
        dado = ''
        match escolha:
            case '1':
                dado = "nome"
            case '2':
                dado = "email"
            case '3':
                dado = "cpf"
            case '4':
                dado = "rua"
            case '5':
                dado = "numero"
            case '6':
                dado = "cidade"
            case '7':
                dado = "estado"
            case _ :
                print("Operação não entendida")

        dadoAtualizado = input("Insira a nova informação: ")

        query = ("MATCH (u:usuario) WHERE u.email = $emailUsuario SET u." + dado + " = $dadoAtualizado")

        db.run(query, emailUsuario = emailUsuario, dado=dado, dadoAtualizado=dadoAtualizado)

    def atualizarVendedor(self):
        with self.driver.session(database="neo4j") as session:
            session.execute_write(self._atlVendedor)

    @staticmethod
    def _atlVendedor(db):
        emailVendedor = input("Insira o email do vendedor: ")

        print('''
                1 - Nome
                2 - Email
                3 - CNPJ
            ''')

        
        escolha = input("Digite o que deseja atualizar: ")
        dado = ''
        match escolha:
            case '1':
                dado = "nome"
            case '2':
                dado = "email"
            case '3':
                dado = "cnpj"
            case _ :
                print("Operação não entendida")

        dadoAtualizado = input("Insira a nova informação: ")

        query = ("MATCH (v:vendedor) WHERE v.email = $emailVendedor SET v." + dado + " = $dadoAtualizado")

        db.run(query, emailVendedor=emailVendedor, dado=dado, dadoAtualizado=dadoAtualizado)

    def atualizarProduto(self):
        with self.driver.session(database="neo4j") as session:
            session.execute_write(self._atlProduto)

    @staticmethod
    def _atlProduto(db):
        nomeProduto = input("Insira o nome do produto : ")

        print('''
                1 - Nome
                2 - Preço
            ''')
        
        escolha = input("Digite o que deseja atualizar: ")
        dado = ''
        match escolha:
            case '1':
                dado = "nome"
            case '2':
                dado = "preco"
            case _ :
                print("Operação não entendida")

        dadoAtualizado = input("Insira a nova informação: ")

        query = ("MATCH (p:produto) WHERE p.nome = $nomeProduto SET p." + dado + " = $dadoAtualizado")

        db.run(query, nomeProd=nomeProduto, dado=dado, dadoAtualizado=dadoAtualizado)
    
    ## Deletar ##

    def deletarUsuario(self):
        with self.driver.session(database="neo4j") as session:
            session.write_transaction(self._delUsuario)

    @staticmethod
    def _delUsuario(db):
        emailUsuario = input("Insira o email do usuário: ")
        query = "MATCH (u:usuario) WHERE u.email = $emailUsuario DETACH DELETE u"
        print("Usuário deletado com sucesso")
        db.run(query, emailUsuario=emailUsuario)

    def deletarVendedor(self):
        with self.driver.session(database="neo4j") as session:
            session.write_transaction(self._delVendedor)

    @staticmethod
    def _delVendedor(db):
        emailVendedor = input("Insira o email do vendedor: ")
        query = "MATCH (v:vendedor) WHERE v.email = $emailVendedor DETACH DELETE v"
        print("Vendedor deletado com sucesso")
        db.run(query, emailVendedor=emailVendedor)

    def deletarProduto(self):
        with self.driver.session(database="neo4j") as session:
            session.write_transaction(self._delProduto)

    @staticmethod
    def _delProduto(db):
        nomeProduto = input("Insira o nome do produto: ")
        query = "MATCH (p:produto) WHERE p.nome = $nomeProduto DETACH DELETE p"
        print("Produto deletado com sucesso")
        db.run(query, nomeProduto=nomeProduto)

if __name__ == "__main__":

    uri = "neo4j+s://72709b83.databases.neo4j.io"
    user = "neo4j"
    password = "pC_hpxthwwYzKSzUJbCc9D0JH975Nxpwx5OhjB-uVSU"
    app = App(uri, user, password)

    def menu():
        loop = True
        while loop:
            print("""
                1 - Novo Usuario \n
                2 - Novo Vendedor \n 
                3 - Novo Produto \n
                4 - Realizar Compra \n
                5 - Encontrar Usuario \n
                6 - Encontrar Vendedor \n
                7 - Encontrar Produto \n
                8 - Encontrar Compra \n
                9 - Atualizar Usuario \n
                10 - Atualizar Vendedor \n
                11 - Atualizar Produto \n
                12 - Deletar Usuario \n
                13 - Deletar Vendedor \n
                14 - Deletar Produto \n
                15 - Encontrar todos Usuarios \n
                16 - Encontrar todos Vendedores \n
                17 - Encontrar todos Produtos \n
                18 - Encontrar todas Compras \n
                0 - Sair \n
            """)
            escolha = input("Digite a Operação desejada: ")
            match escolha:
                case '1':
                    app.criarUsuario()
                case '2':
                    app.criarVendedor()
                case '3':
                    app.criarProduto()
                case '4':
                    app.realizarCompra()
                case '5':
                    app.procurarUsuario()
                case '6':
                    app.procurarVendedor()
                case '7':
                    app.procurarProduto()
                case '8':
                    app.procurarCompra()
                case '9':
                    app.atualizarUsuario()
                case '10':
                    app.atualizarVendedor()
                case '11':
                    app.atualizarProduto()
                case '12':
                    app.deletarUsuario()
                case '13':
                    app.deletarVendedor()
                case '14':
                    app.deletarProduto()
                case '15':
                    app.procurarUsuarios()
                case '16':
                    app.procurarVendedores()
                case '17':
                    app.procurarProdutos()
                case '18':
                    app.procurarCompras()
                case '0':
                    print("Até a Próxima!")
                    loop = False
                    app.close()
                    break
                case _:
                    print("Operação não entendida")


menu()


    