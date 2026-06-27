import customtkinter as ctk
from tkinter import messagebox
import banco

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class SistemaEstoque(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Sistema de Controle de Estoque e Vendas")
        self.geometry("900x600")

        # Inicializa a estrutura do banco de dados
        banco.criar_tabelas()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.criar_menu()

        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=20,
            pady=20
        )

        self.mostrar_dashboard()

    def criar_menu(self):
        self.frame_menu = ctk.CTkFrame(self, width=180, corner_radius=0)
        self.frame_menu.grid(row=0, column=0, sticky="ns")

        titulo = ctk.CTkLabel(
            self.frame_menu,
            text="MENU",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        titulo.pack(pady=20)

        ctk.CTkButton(
            self.frame_menu,
            text="Dashboard",
            command=self.mostrar_dashboard
        ).pack(pady=10, padx=20)

        ctk.CTkButton(
            self.frame_menu,
            text="Cadastrar Produto",
            command=self.mostrar_cadastro
        ).pack(pady=10, padx=20)

        ctk.CTkButton(
            self.frame_menu,
            text="Pesquisar Produto",
            command=self.mostrar_pesquisa
        ).pack(pady=10, padx=20)

        ctk.CTkButton(
            self.frame_menu,
            text="Entrada Estoque",
            command=self.mostrar_entrada_estoque
        ).pack(pady=10, padx=20)
        
        ctk.CTkButton(
            self.frame_menu,
            text="Estoque",
            command=self.mostrar_relatorio
        ).pack(pady=10, padx=20)

        ctk.CTkButton(
            self.frame_menu,
            text="Registrar Venda",
            command=self.mostrar_vendas
        ).pack(pady=10, padx=20)

        ctk.CTkButton(
            self.frame_menu,
            text="Movimentações",
            command=self.mostrar_movimentacoes
        ).pack(pady=10, padx=20)

    def limpar_frame(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

    # DASHBOARD
    def mostrar_dashboard(self):
        self.limpar_frame()

        total_produtos = banco.total_produtos()
        estoque_baixo = banco.produtos_estoque_baixo()
        total_itens = banco.quantidade_total_estoque()
        ultima = banco.ultima_movimentacao()

        ctk.CTkLabel(
            self.frame_principal,
            text="Dashboard",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)

        if ultima:
            ctk.CTkLabel(
                self.frame_principal,
                text=(
                    f"Última movimentação:\n"
                    f"{ultima[0]} | {ultima[1]} | Qtd: {ultima[2]}"
                ),
                 font=ctk.CTkFont(size=14)
            ).pack(pady=20)

        ctk.CTkLabel(
            self.frame_principal,
            text=f"Produtos cadastrados: {total_produtos}",
            font=ctk.CTkFont(size=16)
        ).pack(pady=10)

        ctk.CTkLabel(
            self.frame_principal,
            text=f"Produtos com estoque baixo: {estoque_baixo}",
            font=ctk.CTkFont(size=16),
            text_color="red" if estoque_baixo > 0 else "green"
        ).pack(pady=10)

        ctk.CTkLabel(
            self.frame_principal,
            text=f"Total de itens em estoque: {total_itens}",
            font=ctk.CTkFont(size=16)
        ).pack(pady=10)
    
    # CADASTRO 
    def mostrar_cadastro(self):
        self.limpar_frame()

        titulo = ctk.CTkLabel(
            self.frame_principal,
            text="Cadastro de Produto",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titulo.pack(pady=20)

        self.entry_nome = ctk.CTkEntry(self.frame_principal, placeholder_text="Nome", width=300)
        self.entry_nome.pack(pady=10)

        self.entry_qtd = ctk.CTkEntry(self.frame_principal, placeholder_text="Quantidade", width=300)
        self.entry_qtd.pack(pady=10)

        self.entry_minimo = ctk.CTkEntry(self.frame_principal, placeholder_text="Estoque mínimo", width=300)
        self.entry_minimo.pack(pady=10)

        self.entry_preco = ctk.CTkEntry(self.frame_principal, placeholder_text="Preço de venda", width=300)
        self.entry_preco.pack(pady=10)

        ctk.CTkButton(
            self.frame_principal,
            text="Salvar Produto",
            command=self.salvar_produto
        ).pack(pady=20)

    def salvar_produto(self):
        nome = self.entry_nome.get().strip()

        if not nome:
            messagebox.showerror("Erro", "O nome do produto não pode estar vazio.")
            return

        try:
            qtd = int(self.entry_qtd.get())
            minimo = int(self.entry_minimo.get())
            preco = float(self.entry_preco.get())
        except ValueError:
            messagebox.showerror("Erro", "Quantidade, Estoque Mínimo e Preço devem conter valores numéricos válidos.")
            return

        try:
            banco.inserir_produto(nome, qtd, minimo, preco)
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            
            self.entry_nome.delete(0, 'end')
            self.entry_qtd.delete(0, 'end')
            self.entry_minimo.delete(0, 'end')
            self.entry_preco.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar no banco de dados: {e}")
   
    # ESTOQUE
    def mostrar_relatorio(self):
        self.limpar_frame()

        titulo = ctk.CTkLabel(
            self.frame_principal,
            text="Estoque Atual",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titulo.pack(pady=20)

        frame_lista = ctk.CTkScrollableFrame(self.frame_principal, width=650, height=400)
        frame_lista.pack(fill="both", expand=True, padx=20, pady=20)

        produtos = banco.listar_produtos()

        for produto in produtos:
            p_id, p_nome, p_qtd, p_minimo, p_preco = produto
            cor_texto = "red" if p_qtd <= p_minimo else "green"

            texto = (
                f"ID: {p_id} | "
                f"Produto: {p_nome} | "
                f"Qtd Atual: {p_qtd} | "
                f"Mínimo: {p_minimo} | "
                f"Preço: R$ {p_preco:.2f}"
            )

            ctk.CTkLabel(
                frame_lista,
                text=texto,
                text_color=cor_texto,
                font=ctk.CTkFont(size=14)
            ).pack(anchor="w", padx=15, pady=6)

    # VENDAS
    def mostrar_vendas(self):
        self.limpar_frame()

        ctk.CTkLabel(
            self.frame_principal,
            text="Registrar Venda",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)

        self.entry_id_produto = ctk.CTkEntry(self.frame_principal, placeholder_text="ID do Produto", width=300)
        self.entry_id_produto.pack(pady=10)

        self.entry_qtd_venda = ctk.CTkEntry(self.frame_principal, placeholder_text="Quantidade Vendida", width=300)
        self.entry_qtd_venda.pack(pady=10)

        ctk.CTkButton(
            self.frame_principal,
            text="Confirmar Venda",
            command=self.registrar_venda
        ).pack(pady=20)

    def registrar_venda(self):
        try:
            produto_id = int(self.entry_id_produto.get())
            quantidade = int(self.entry_qtd_venda.get())
        except ValueError:
            messagebox.showerror("Erro", "ID do Produto e Quantidade devem ser números inteiros.")
            return

        try:
            produto = banco.buscar_produto_por_id(produto_id)

            if produto is None:
                messagebox.showerror("Erro", "Produto não encontrado.")
                return

            estoque_atual = produto[2]

            if estoque_atual < quantidade:
                messagebox.showerror("Erro", f"Estoque insuficiente. Quantidade disponível: {estoque_atual}")
                return

            novo_estoque = estoque_atual - quantidade
            banco.atualizar_estoque(produto_id, novo_estoque)
            banco.registrar_movimentacao(produto_id, 'SAIDA', quantidade)

            messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")
            
            self.entry_id_produto.delete(0, 'end')
            self.entry_qtd_venda.delete(0, 'end')

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao processar a transação: {e}")

    # PESQUISA
    def mostrar_pesquisa(self):
        self.limpar_frame()

        ctk.CTkLabel(
            self.frame_principal,
            text="Pesquisar Produto",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)

        self.entry_busca = ctk.CTkEntry(
            self.frame_principal,
            width=300,
            placeholder_text="Digite o nome do produto"
        )
        self.entry_busca.pack(pady=10)

        ctk.CTkButton(
            self.frame_principal,
            text="Buscar",
            command=self.buscar_produto
        ).pack(pady=10)

        self.frame_resultados = ctk.CTkScrollableFrame(
            self.frame_principal,
            width=700,
            height=350
        )
        self.frame_resultados.pack(fill="both", expand=True, padx=20, pady=20)

    def buscar_produto(self):
        for widget in self.frame_resultados.winfo_children():
            widget.destroy()

        produtos = banco.buscar_produtos_por_nome(self.entry_busca.get())

        if not produtos:
            ctk.CTkLabel(
                self.frame_resultados,
                text="Nenhum produto encontrado."
            ).pack(pady=20)
            return

        for produto in produtos:
            frame = ctk.CTkFrame(self.frame_resultados)
            frame.pack(fill="x", padx=10, pady=5)

            texto = (
                f"ID: {produto[0]} | "
                f"{produto[1]} | "
                f"Qtd: {produto[2]} | "
                f"Preço: R$ {produto[4]:.2f}"
            )

            ctk.CTkLabel(frame, text=texto).pack(side="left", padx=10)

            ctk.CTkButton(
                frame,
                text="Editar",
                state="disabled"
            ).pack(side="right", padx=5)

            ctk.CTkButton(
                frame,
                text="Excluir",
                fg_color="red",
                command=lambda pid=produto[0]: self.excluir_produto(pid)
            ).pack(side="right", padx=5)

    def excluir_produto(self, produto_id):
        resposta = messagebox.askyesno(
            "Confirmação",
            "Deseja excluir este produto?"
        )

        if resposta:
            banco.excluir_produto(produto_id)
            messagebox.showinfo("Sucesso", "Produto excluído.")
            self.buscar_produto()

    # ENTRADA DE ESTOQUE
    def mostrar_entrada_estoque(self):
        self.limpar_frame()

        ctk.CTkLabel(
            self.frame_principal,
            text="Entrada de Estoque",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)

        self.entry_produto_entrada = ctk.CTkEntry(
            self.frame_principal,
            placeholder_text="ID Produto",
            width=300
        )
        self.entry_produto_entrada.pack(pady=10)

        self.entry_qtd_entrada = ctk.CTkEntry(
            self.frame_principal,
            placeholder_text="Quantidade",
            width=300
        )
        self.entry_qtd_entrada.pack(pady=10)

        ctk.CTkButton(
            self.frame_principal,
            text="Adicionar Estoque",
            command=self.adicionar_estoque
        ).pack(pady=20)

    def adicionar_estoque(self):
        try:
            produto_id = int(self.entry_produto_entrada.get())
            quantidade = int(self.entry_qtd_entrada.get())

            sucesso = banco.entrada_estoque(produto_id, quantidade)

            if sucesso:
                messagebox.showinfo("Sucesso", "Estoque atualizado.")
                self.entry_produto_entrada.delete(0, 'end')
                self.entry_qtd_entrada.delete(0, 'end')
            else:
                messagebox.showerror("Erro", "Produto não encontrado.")

        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos.")

    # MOVIMENTAÇÕES
    def mostrar_movimentacoes(self):
        self.limpar_frame()

        ctk.CTkLabel(
            self.frame_principal,
            text="Histórico de Movimentações",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)

        frame = ctk.CTkScrollableFrame(
            self.frame_principal,
            width=700,
            height=400
        )
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        movimentacoes = banco.listar_movimentacoes_completas()

        for mov in movimentacoes:
            texto = (
                f"{mov[4]} | "
                f"{mov[1]} | "
                f"{mov[2]} | "
                f"Qtd: {mov[3]}"
            )

            cor = "green" if mov[2] == "ENTRADA" else "red"

            ctk.CTkLabel(
                frame,
                text=texto,
                text_color=cor
            ).pack(anchor="w", padx=10, pady=5)

if __name__ == "__main__":
    app = SistemaEstoque()
    app.mainloop()