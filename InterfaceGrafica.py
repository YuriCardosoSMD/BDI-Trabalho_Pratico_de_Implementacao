from dao.ClienteDAO import ClienteDAO
from dao.MedicamentoDAO import MedicamentoDAO
from dao.EstoqueDAO import EstoqueDAO
from dao.VendaDAO import VendaDAO


# Classe que implementa a interface da aplicação
class InterfaceGrafica:

    def __init__(self):
        self.cliente_dao = ClienteDAO()
        self.medicamento_dao = MedicamentoDAO()
        self.estoque_dao = EstoqueDAO()
        self.venda_dao = VendaDAO()

    # Menu Principal
    def menu_principal(self):
        while True:
            print("==============================")
            print("Sistema da Farmácia")
            print("==============================")
            print("1 - Clientes")
            print("2 - Medicamentos")
            print("3 - Estoque")
            print("4 - Vendas")
            print("0 - Sair")
            print("==============================")
            opcao = input("Digite uma opção: ")
            if opcao == "1":
                self.menu_clientes()
            elif opcao == "2":
                self.menu_medicamentos()
            elif opcao == "3":
                self.menu_estoque()
            elif opcao == "4":
                self.menu_vendas()
            elif opcao == "0":
                print("Aplicação encerrada")
                break
            else:
                print("Opção inválida")

    # ==================== CLIENTES ====================

    def menu_clientes(self):
        while True:
            print("==============================")
            print("Clientes")
            print("==============================")
            print("1 - Listar Todos")
            print("2 - Buscar por Código")
            print("3 - Inserir")
            print("4 - Atualizar")
            print("5 - Remover")
            print("0 - Voltar")
            print("==============================")
            opcao = input("Digite uma opção: ")
            if opcao == "1":
                self.listar_clientes()
            elif opcao == "2":
                self.buscar_cliente()
            elif opcao == "3":
                self.inserir_cliente()
            elif opcao == "4":
                self.atualizar_cliente()
            elif opcao == "5":
                self.remover_cliente()
            elif opcao == "0":
                break
            else:
                print("Opção inválida")

    def listar_clientes(self):
        clientes = self.cliente_dao.listar_todos()
        if not clientes:
            print("Nenhum registro encontrado")
            return
        for c in clientes:
            print(f"Código = {c.codigo} | Nome = {c.nome}")

    def buscar_cliente(self):
        try:
            codigo = int(input("Digite o código: "))
            c = self.cliente_dao.buscar(codigo)
            if c:
                print(f"Código = {c.codigo} | Nome = {c.nome}")
            else:
                print("Cliente não encontrado")
        except ValueError:
            print("Código inválido")

    def inserir_cliente(self):
        nome = input("Nome: ").strip()
        sucesso = self.cliente_dao.inserir(nome)
        print("Registro inserido com sucesso" if sucesso else "Falha ao inserir registro")

    def atualizar_cliente(self):
        try:
            codigo = int(input("Código: "))
            nome = input("Novo nome: ").strip()
            sucesso = self.cliente_dao.atualizar(nome, codigo)
            print("Registro atualizado com sucesso" if sucesso else "Falha ao atualizar registro")
        except ValueError:
            print("Código inválido")

    def remover_cliente(self):
        try:
            codigo = int(input("Código: "))
            sucesso = self.cliente_dao.remover(codigo)
            print("Registro removido com sucesso" if sucesso else "Falha ao remover registro")
        except ValueError:
            print("Código inválido")

    # ==================== MEDICAMENTOS ====================

    def menu_medicamentos(self):
        while True:
            print("==============================")
            print("Medicamentos")
            print("==============================")
            print("1 - Listar Todos")
            print("2 - Inserir")
            print("3 - Atualizar")
            print("0 - Voltar")
            print("==============================")
            opcao = input("Digite uma opção: ")
            if opcao == "1":
                self.listar_medicamentos()
            elif opcao == "2":
                self.inserir_medicamento()
            elif opcao == "3":
                self.atualizar_medicamento()
            elif opcao == "0":
                break
            else:
                print("Opção inválida")

    def listar_medicamentos(self):
        medicamentos = self.medicamento_dao.listar_todos()
        if not medicamentos:
            print("Nenhum registro encontrado")
            return
        for m in medicamentos:
            print(
                f"Código = {m.codigo} | Descrição = {m.descricao} | Preço = R$ {m.preco:.2f} "
                f"| Categoria = {m.categoria} | Fabricante = {m.fabricante}"
            )

    def inserir_medicamento(self):
        try:
            descricao = input("Descrição: ").strip()
            preco = float(input("Preço: ").replace(",", "."))
            cod_categoria = int(input("Código da categoria: "))
            cod_fabricante = int(input("Código do fabricante: "))
            sucesso = self.medicamento_dao.inserir(descricao, preco, cod_categoria, cod_fabricante)
            print("Registro inserido com sucesso" if sucesso else "Falha ao inserir registro")
        except ValueError:
            print("Valor inválido")

    def atualizar_medicamento(self):
        try:
            codigo = int(input("Código: "))
            descricao = input("Nova descrição: ").strip()
            preco = float(input("Novo preço: ").replace(",", "."))
            sucesso = self.medicamento_dao.atualizar(descricao, preco, codigo)
            print("Registro atualizado com sucesso" if sucesso else "Falha ao atualizar registro")
        except ValueError:
            print("Valor inválido")

    # ==================== ESTOQUE ====================

    def menu_estoque(self):
        while True:
            print("==============================")
            print("Estoque")
            print("==============================")
            print("1 - Consultar Estoque de uma Filial")
            print("2 - Atualizar Quantidade")
            print("0 - Voltar")
            print("==============================")
            opcao = input("Digite uma opção: ")
            if opcao == "1":
                self.listar_estoque()
            elif opcao == "2":
                self.atualizar_estoque()
            elif opcao == "0":
                break
            else:
                print("Opção inválida")

    def listar_estoque(self):
        try:
            cod_filial = int(input("Código da filial: "))
            estoque = self.estoque_dao.listar_por_filial(cod_filial)
            if not estoque:
                print("Nenhum registro encontrado")
                return
            for e in estoque:
                print(f"Medicamento = {e.medicamento} | Quantidade = {e.quantidade}")
        except ValueError:
            print("Código inválido")

    def atualizar_estoque(self):
        try:
            cod_filial = int(input("Código da filial: "))
            id_medicamento = int(input("Código do medicamento: "))
            quantidade = int(input("Nova quantidade: "))
            sucesso = self.estoque_dao.atualizar(quantidade, cod_filial, id_medicamento)
            print("Registro atualizado com sucesso" if sucesso else "Falha ao atualizar registro")
        except ValueError:
            print("Valor inválido")

    # ==================== VENDAS ====================

    def menu_vendas(self):
        while True:
            print("==============================")
            print("Vendas")
            print("==============================")
            print("1 - Listar Todas")
            print("2 - Ver Itens de uma Venda")
            print("3 - Registrar Venda")
            print("4 - Cancelar Venda")
            print("0 - Voltar")
            print("==============================")
            opcao = input("Digite uma opção: ")
            if opcao == "1":
                self.listar_vendas()
            elif opcao == "2":
                self.listar_itens_venda()
            elif opcao == "3":
                self.inserir_venda()
            elif opcao == "4":
                self.remover_venda()
            elif opcao == "0":
                break
            else:
                print("Opção inválida")

    def listar_vendas(self):
        vendas = self.venda_dao.listar_todas()
        if not vendas:
            print("Nenhum registro encontrado")
            return
        for v in vendas:
            print(
                f"Código = {v.codigo} | Data = {v.data_hora:%d/%m/%Y %H:%M} | Filial = {v.filial} "
                f"| Cliente = {v.cliente} | Funcionário = {v.funcionario}"
            )

    def listar_itens_venda(self):
        try:
            id_venda = int(input("Código da venda: "))
            itens = self.venda_dao.listar_itens(id_venda)
            if not itens:
                print("Nenhum registro encontrado")
                return
            total = 0
            for i in itens:
                subtotal = i.quantidade * i.preco_unitario
                total += subtotal
                print(
                    f"Medicamento = {i.medicamento} | Qtd = {i.quantidade} "
                    f"| Preço = R$ {i.preco_unitario:.2f} | Subtotal = R$ {subtotal:.2f}"
                )
            print(f"Total da venda = R$ {total:.2f}")
        except ValueError:
            print("Código inválido")

    def inserir_venda(self):
        try:
            cod_filial = int(input("Código da filial: "))
            id_cliente = int(input("Código do cliente: "))
            id_funcionario = int(input("Código do funcionário: "))

            itens = []
            while True:
                codigo = input("Código do medicamento (Enter para finalizar): ").strip()
                if codigo == "":
                    break
                medicamento = self.medicamento_dao.buscar(int(codigo))
                if medicamento is None:
                    print("Medicamento não encontrado")
                    continue
                quantidade = int(input("Quantidade: "))
                itens.append((medicamento.codigo, quantidade, medicamento.preco))
                print(f"Item adicionado: {medicamento.descricao} (R$ {medicamento.preco:.2f})")

            if not itens:
                print("A venda precisa ter pelo menos um item")
                return

            id_venda = self.venda_dao.inserir(cod_filial, id_cliente, id_funcionario, itens)
            print(f"Venda {id_venda} registrada com sucesso" if id_venda else "Falha ao registrar venda")
        except ValueError:
            print("Valor inválido")

    def remover_venda(self):
        try:
            id_venda = int(input("Código da venda: "))
            sucesso = self.venda_dao.remover(id_venda)
            print("Venda cancelada com sucesso" if sucesso else "Falha ao cancelar venda")
        except ValueError:
            print("Código inválido")


# Inicializa a aplicação
if __name__ == "__main__":
    gui = InterfaceGrafica()
    gui.menu_principal()
