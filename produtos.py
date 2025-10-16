"""
Tela de Produtos - Gestão completa de produtos
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from database import Database
from utils import Formatador, Validador
from typing import Optional

class Produtos(ctk.CTkFrame):
    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.db = db
        self.configure(fg_color="transparent")
        self.produto_selecionado_id = None
        
        # Container principal
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        titulo = ctk.CTkLabel(
            container,
            text="📦 Gestão de Produtos",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titulo.pack(pady=(0, 20))
        
        # Frame de busca e ações
        self.criar_barra_acoes(container)
        
        # Frame principal dividido
        frame_principal = ctk.CTkFrame(container, fg_color="transparent")
        frame_principal.pack(fill="both", expand=True)
        
        # Lista de produtos (esquerda)
        self.criar_lista_produtos(frame_principal)
        
        # Formulário de produto (direita)
        self.criar_formulario(frame_principal)
        
        # Carregar dados
        self.carregar_produtos()
        self.carregar_categorias()
    
    def criar_barra_acoes(self, parent):
        """Cria barra de busca e ações"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=(0, 15))
        
        # Busca
        self.entry_busca = ctk.CTkEntry(
            frame,
            placeholder_text="🔍 Buscar produto...",
            width=300
        )
        self.entry_busca.pack(side="left", padx=5, pady=10)
        self.entry_busca.bind("<KeyRelease>", lambda e: self.filtrar_produtos())
        
        # Filtro por categoria
        self.combo_filtro_cat = ctk.CTkComboBox(
            frame,
            values=["Todas as Categorias"],
            width=200,
            command=lambda x: self.filtrar_produtos()
        )
        self.combo_filtro_cat.pack(side="left", padx=5)
        
        # Botão Novo
        btn_novo = ctk.CTkButton(
            frame,
            text="➕ Novo Produto",
            command=self.novo_produto,
            width=150,
            fg_color="#2ca02c",
            hover_color="#28a745"
        )
        btn_novo.pack(side="right", padx=5)
        
        # Botão Alertas
        self.btn_alertas = ctk.CTkButton(
            frame,
            text="⚠️ Estoque Baixo (0)",
            command=self.mostrar_alertas,
            width=150,
            fg_color="#d62728",
            hover_color="#c82333"
        )
        self.btn_alertas.pack(side="right", padx=5)
    
    def criar_lista_produtos(self, parent):
        """Cria lista de produtos"""
        frame = ctk.CTkFrame(parent)
        frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        label = ctk.CTkLabel(
            frame,
            text="Lista de Produtos",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        label.pack(pady=10)
        
        # Frame com scroll para lista
        self.scroll_lista = ctk.CTkScrollableFrame(frame)
        self.scroll_lista.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Cabeçalho da tabela
        self.criar_cabecalho_lista()
    
    def criar_cabecalho_lista(self):
        """Cria cabeçalho da lista"""
        frame_header = ctk.CTkFrame(self.scroll_lista, fg_color="#1f77b4")
        frame_header.pack(fill="x", pady=(0, 5))
        
        headers = [
            ("ID", 50),
            ("Nome", 200),
            ("Categoria", 120),
            ("Estoque", 80),
            ("P. Venda", 100),
            ("Ações", 100)
        ]
        
        for texto, largura in headers:
            label = ctk.CTkLabel(
                frame_header,
                text=texto,
                font=ctk.CTkFont(size=11, weight="bold"),
                width=largura
            )
            label.pack(side="left", padx=5, pady=5)
    
    def criar_formulario(self, parent):
        """Cria formulário de produto"""
        frame = ctk.CTkFrame(parent)
        frame.pack(side="right", fill="both", padx=(10, 0))
        
        label = ctk.CTkLabel(
            frame,
            text="Detalhes do Produto",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        label.pack(pady=10)
        
        # Scroll frame
        scroll = ctk.CTkScrollableFrame(frame, width=400)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Nome
        ctk.CTkLabel(scroll, text="Nome do Produto *", anchor="w").pack(fill="x", pady=(10, 0))
        self.entry_nome = ctk.CTkEntry(scroll, placeholder_text="Ex: Notebook Dell")
        self.entry_nome.pack(fill="x", pady=(5, 10))
        
        # Descrição
        ctk.CTkLabel(scroll, text="Descrição", anchor="w").pack(fill="x")
        self.text_descricao = ctk.CTkTextbox(scroll, height=80)
        self.text_descricao.pack(fill="x", pady=(5, 10))
        
        # Categoria
        ctk.CTkLabel(scroll, text="Categoria *", anchor="w").pack(fill="x")
        frame_cat = ctk.CTkFrame(scroll, fg_color="transparent")
        frame_cat.pack(fill="x", pady=(5, 10))
        
        self.combo_categoria = ctk.CTkComboBox(frame_cat, values=["Selecione..."], width=250)
        self.combo_categoria.pack(side="left", expand=True, fill="x")
        
        btn_nova_cat = ctk.CTkButton(
            frame_cat,
            text="+",
            width=40,
            command=self.nova_categoria
        )
        btn_nova_cat.pack(side="right", padx=(5, 0))
        
        # Preços
        frame_precos = ctk.CTkFrame(scroll, fg_color="transparent")
        frame_precos.pack(fill="x", pady=10)
        
        # Preço de Custo
        frame_custo = ctk.CTkFrame(frame_precos, fg_color="transparent")
        frame_custo.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkLabel(frame_custo, text="Preço de Custo *", anchor="w").pack(fill="x")
        self.entry_preco_custo = ctk.CTkEntry(frame_custo, placeholder_text="0,00")
        self.entry_preco_custo.pack(fill="x", pady=(5, 0))
        self.entry_preco_custo.bind("<KeyRelease>", self.calcular_margem_auto)
        
        # Preço de Venda
        frame_venda = ctk.CTkFrame(frame_precos, fg_color="transparent")
        frame_venda.pack(side="right", fill="x", expand=True, padx=(5, 0))
        ctk.CTkLabel(frame_venda, text="Preço de Venda *", anchor="w").pack(fill="x")
        self.entry_preco_venda = ctk.CTkEntry(frame_venda, placeholder_text="0,00")
        self.entry_preco_venda.pack(fill="x", pady=(5, 0))
        self.entry_preco_venda.bind("<KeyRelease>", self.calcular_margem_auto)
        
        # Margem calculada
        self.label_margem = ctk.CTkLabel(
            scroll,
            text="Margem de Lucro: 0%",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#2ca02c"
        )
        self.label_margem.pack(pady=10)
        
        # Calculadora de margem
        frame_calc_margem = ctk.CTkFrame(scroll)
        frame_calc_margem.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            frame_calc_margem,
            text="Calcular preço com margem desejada:",
            font=ctk.CTkFont(size=11)
        ).pack(pady=(10, 5))
        
        frame_calc_inputs = ctk.CTkFrame(frame_calc_margem, fg_color="transparent")
        frame_calc_inputs.pack(fill="x", padx=10, pady=(0, 10))
        
        self.entry_margem_desejada = ctk.CTkEntry(
            frame_calc_inputs,
            placeholder_text="% margem",
            width=100
        )
        self.entry_margem_desejada.pack(side="left", padx=(0, 5))
        
        btn_calc = ctk.CTkButton(
            frame_calc_inputs,
            text="Calcular",
            width=100,
            command=self.calcular_preco_margem
        )
        btn_calc.pack(side="left")
        
        # Estoque
        frame_estoque = ctk.CTkFrame(scroll, fg_color="transparent")
        frame_estoque.pack(fill="x", pady=10)
        
        frame_qty = ctk.CTkFrame(frame_estoque, fg_color="transparent")
        frame_qty.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkLabel(frame_qty, text="Quantidade em Estoque *", anchor="w").pack(fill="x")
        self.entry_estoque = ctk.CTkEntry(frame_qty, placeholder_text="0")
        self.entry_estoque.pack(fill="x", pady=(5, 0))
        
        frame_min = ctk.CTkFrame(frame_estoque, fg_color="transparent")
        frame_min.pack(side="right", fill="x", expand=True, padx=(5, 0))
        ctk.CTkLabel(frame_min, text="Estoque Mínimo *", anchor="w").pack(fill="x")
        self.entry_estoque_min = ctk.CTkEntry(frame_min, placeholder_text="10")
        self.entry_estoque_min.pack(fill="x", pady=(5, 0))
        
        # Imagem (opcional)
        ctk.CTkLabel(scroll, text="Imagem (opcional)", anchor="w").pack(fill="x", pady=(10, 0))
        frame_img = ctk.CTkFrame(scroll, fg_color="transparent")
        frame_img.pack(fill="x", pady=(5, 10))
        
        self.entry_imagem = ctk.CTkEntry(frame_img, placeholder_text="Caminho da imagem...")
        self.entry_imagem.pack(side="left", fill="x", expand=True)
        
        btn_img = ctk.CTkButton(
            frame_img,
            text="📁",
            width=40,
            command=self.selecionar_imagem
        )
        btn_img.pack(side="right", padx=(5, 0))
        
        # Botões de ação
        frame_botoes = ctk.CTkFrame(scroll, fg_color="transparent")
        frame_botoes.pack(fill="x", pady=20)
        
        self.btn_salvar = ctk.CTkButton(
            frame_botoes,
            text="💾 Salvar",
            command=self.salvar_produto,
            fg_color="#2ca02c",
            hover_color="#28a745"
        )
        self.btn_salvar.pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        self.btn_cancelar = ctk.CTkButton(
            frame_botoes,
            text="❌ Cancelar",
            command=self.limpar_formulario,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        self.btn_cancelar.pack(side="right", expand=True, fill="x", padx=(5, 0))
    
    def carregar_categorias(self):
        """Carrega categorias no combobox"""
        categorias = self.db.listar_categorias()
        valores = ["Selecione..."] + [cat['nome'] for cat in categorias]
        
        self.combo_categoria.configure(values=valores)
        self.combo_filtro_cat.configure(
            values=["Todas as Categorias"] + [cat['nome'] for cat in categorias]
        )
    
    def nova_categoria(self):
        """Abre diálogo para criar nova categoria"""
        dialog = ctk.CTkInputDialog(
            text="Nome da nova categoria:",
            title="Nova Categoria"
        )
        nome = dialog.get_input()
        
        if nome:
            try:
                self.db.adicionar_categoria(nome)
                self.carregar_categorias()
                self.combo_categoria.set(nome)
                messagebox.showinfo("Sucesso", "Categoria criada com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao criar categoria: {str(e)}")
    
    def calcular_margem_auto(self, event=None):
        """Calcula margem automaticamente"""
        try:
            custo_str = self.entry_preco_custo.get().replace(",", ".")
            venda_str = self.entry_preco_venda.get().replace(",", ".")
            
            if custo_str and venda_str:
                custo = float(custo_str)
                venda = float(venda_str)
                
                if custo > 0:
                    margem = Formatador.calcular_margem(venda, custo)
                    self.label_margem.configure(
                        text=f"Margem de Lucro: {Formatador.formatar_porcentagem(margem)}"
                    )
                    
                    # Colorir baseado na margem
                    if margem < 10:
                        self.label_margem.configure(text_color="#d62728")
                    elif margem < 30:
                        self.label_margem.configure(text_color="#ff7f0e")
                    else:
                        self.label_margem.configure(text_color="#2ca02c")
        except:
            pass
    
    def calcular_preco_margem(self):
        """Calcula preço de venda baseado em margem desejada"""
        try:
            custo_str = self.entry_preco_custo.get().replace(",", ".")
            margem_str = self.entry_margem_desejada.get().replace(",", ".")
            
            if not custo_str or not margem_str:
                messagebox.showwarning("Atenção", "Preencha o preço de custo e a margem desejada!")
                return
            
            custo = float(custo_str)
            margem = float(margem_str)
            
            preco_venda = Formatador.calcular_preco_com_margem(custo, margem)
            self.entry_preco_venda.delete(0, "end")
            self.entry_preco_venda.insert(0, f"{preco_venda:.2f}")
            
            self.calcular_margem_auto()
            
        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos!")
    
    def selecionar_imagem(self):
        """Abre diálogo para selecionar imagem"""
        filename = filedialog.askopenfilename(
            title="Selecionar Imagem",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if filename:
            self.entry_imagem.delete(0, "end")
            self.entry_imagem.insert(0, filename)
    
    def carregar_produtos(self):
        """Carrega lista de produtos"""
        # Limpar lista
        for widget in self.scroll_lista.winfo_children():
            if widget != self.scroll_lista.winfo_children()[0]:  # Não remove cabeçalho
                widget.destroy()
        
        produtos = self.db.listar_produtos()
        produtos_baixo = self.db.produtos_estoque_baixo()
        
        # Atualizar botão de alertas
        self.btn_alertas.configure(text=f"⚠️ Estoque Baixo ({len(produtos_baixo)})")
        
        for produto in produtos:
            self.criar_item_produto(produto, produto['id'] in [p['id'] for p in produtos_baixo])
    
    def criar_item_produto(self, produto, alerta=False):
        """Cria item de produto na lista"""
        cor_fundo = "#ffe6e6" if alerta else "transparent"
        
        frame = ctk.CTkFrame(self.scroll_lista, fg_color=cor_fundo)
        frame.pack(fill="x", pady=2)
        
        # ID
        ctk.CTkLabel(frame, text=str(produto['id']), width=50).pack(side="left", padx=5)
        
        # Nome
        nome_texto = produto['nome'][:30] + "..." if len(produto['nome']) > 30 else produto['nome']
        ctk.CTkLabel(frame, text=nome_texto, width=200, anchor="w").pack(side="left", padx=5)
        
        # Categoria
        cat_texto = produto.get('categoria_nome', 'S/Cat')[:15]
        ctk.CTkLabel(frame, text=cat_texto, width=120).pack(side="left", padx=5)
        
        # Estoque
        estoque_texto = f"{produto['estoque']}"
        if alerta:
            estoque_texto += " ⚠️"
        ctk.CTkLabel(
            frame,
            text=estoque_texto,
            width=80,
            text_color="#d62728" if alerta else None
        ).pack(side="left", padx=5)
        
        # Preço
        ctk.CTkLabel(
            frame,
            text=Formatador.formatar_moeda(produto['preco_venda']),
            width=100
        ).pack(side="left", padx=5)
        
        # Botões de ação
        frame_acoes = ctk.CTkFrame(frame, fg_color="transparent", width=100)
        frame_acoes.pack(side="left", padx=5)
        
        btn_editar = ctk.CTkButton(
            frame_acoes,
            text="✏️",
            width=35,
            command=lambda: self.editar_produto(produto['id'])
        )
        btn_editar.pack(side="left", padx=2)
        
        btn_excluir = ctk.CTkButton(
            frame_acoes,
            text="🗑️",
            width=35,
            fg_color="#d62728",
            hover_color="#c82333",
            command=lambda: self.excluir_produto(produto['id'])
        )
        btn_excluir.pack(side="left", padx=2)
    
    def filtrar_produtos(self):
        """Filtra produtos por busca e categoria"""
        # Implementação simplificada - recarrega tudo
        self.carregar_produtos()
    
    def novo_produto(self):
        """Prepara formulário para novo produto"""
        self.limpar_formulario()
        self.produto_selecionado_id = None
        self.btn_salvar.configure(text="💾 Salvar")
    
    def editar_produto(self, produto_id):
        """Carrega produto para edição"""
        produto = self.db.buscar_produto(produto_id)
        if not produto:
            return
        
        self.produto_selecionado_id = produto_id
        
        # Preencher formulário
        self.entry_nome.delete(0, "end")
        self.entry_nome.insert(0, produto['nome'])
        
        self.text_descricao.delete("1.0", "end")
        self.text_descricao.insert("1.0", produto['descricao'] or "")
        
        if produto.get('categoria_nome'):
            self.combo_categoria.set(produto['categoria_nome'])
        
        self.entry_preco_custo.delete(0, "end")
        self.entry_preco_custo.insert(0, f"{produto['preco_custo']:.2f}")
        
        self.entry_preco_venda.delete(0, "end")
        self.entry_preco_venda.insert(0, f"{produto['preco_venda']:.2f}")
        
        self.entry_estoque.delete(0, "end")
        self.entry_estoque.insert(0, str(produto['estoque']))
        
        self.entry_estoque_min.delete(0, "end")
        self.entry_estoque_min.insert(0, str(produto['estoque_minimo']))
        
        self.entry_imagem.delete(0, "end")
        self.entry_imagem.insert(0, produto['imagem_path'] or "")
        
        self.calcular_margem_auto()
        
        self.btn_salvar.configure(text="💾 Atualizar")
    
    def salvar_produto(self):
        """Salva ou atualiza produto"""
        # Validações
        if not self.entry_nome.get().strip():
            messagebox.showwarning("Atenção", "Nome do produto é obrigatório!")
            return
        
        if self.combo_categoria.get() == "Selecione...":
            messagebox.showwarning("Atenção", "Selecione uma categoria!")
            return
        
        try:
            preco_custo = float(self.entry_preco_custo.get().replace(",", "."))
            preco_venda = float(self.entry_preco_venda.get().replace(",", "."))
            estoque = int(self.entry_estoque.get())
            estoque_min = int(self.entry_estoque_min.get())
        except ValueError:
            messagebox.showerror("Erro", "Valores numéricos inválidos!")
            return
        
        # Buscar categoria_id
        categorias = self.db.listar_categorias()
        categoria_id = None
        for cat in categorias:
            if cat['nome'] == self.combo_categoria.get():
                categoria_id = cat['id']
                break
        
        try:
            if self.produto_selecionado_id is None:
                # Novo produto
                self.db.adicionar_produto(
                    nome=self.entry_nome.get().strip(),
                    descricao=self.text_descricao.get("1.0", "end").strip(),
                    categoria_id=categoria_id,
                    preco_custo=preco_custo,
                    preco_venda=preco_venda,
                    estoque=estoque,
                    estoque_minimo=estoque_min,
                    imagem_path=self.entry_imagem.get().strip()
                )
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            else:
                # Atualizar produto
                self.db.atualizar_produto(
                    produto_id=self.produto_selecionado_id,
                    nome=self.entry_nome.get().strip(),
                    descricao=self.text_descricao.get("1.0", "end").strip(),
                    categoria_id=categoria_id,
                    preco_custo=preco_custo,
                    preco_venda=preco_venda,
                    estoque=estoque,
                    estoque_minimo=estoque_min,
                    imagem_path=self.entry_imagem.get().strip()
                )
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
            
            self.limpar_formulario()
            self.carregar_produtos()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar produto: {str(e)}")
    
    def excluir_produto(self, produto_id):
        """Exclui produto"""
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este produto?"):
            try:
                self.db.remover_produto(produto_id)
                messagebox.showinfo("Sucesso", "Produto removido com sucesso!")
                self.carregar_produtos()
                if self.produto_selecionado_id == produto_id:
                    self.limpar_formulario()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover produto: {str(e)}")
    
    def limpar_formulario(self):
        """Limpa formulário"""
        self.produto_selecionado_id = None
        self.entry_nome.delete(0, "end")
        self.text_descricao.delete("1.0", "end")
        self.combo_categoria.set("Selecione...")
        self.entry_preco_custo.delete(0, "end")
        self.entry_preco_venda.delete(0, "end")
        self.entry_estoque.delete(0, "end")
        self.entry_estoque.insert(0, "0")
        self.entry_estoque_min.delete(0, "end")
        self.entry_estoque_min.insert(0, "10")
        self.entry_imagem.delete(0, "end")
        self.entry_margem_desejada.delete(0, "end")
        self.label_margem.configure(text="Margem de Lucro: 0%")
        self.btn_salvar.configure(text="💾 Salvar")
    
    def mostrar_alertas(self):
        """Mostra produtos com estoque baixo"""
        produtos = self.db.produtos_estoque_baixo()
        
        if not produtos:
            messagebox.showinfo("Alertas", "Nenhum produto com estoque baixo!")
            return
        
        # Criar janela de alertas
        janela = ctk.CTkToplevel(self)
        janela.title("⚠️ Alertas de Estoque Baixo")
        janela.geometry("600x400")
        
        label = ctk.CTkLabel(
            janela,
            text="Produtos com Estoque Baixo",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        label.pack(pady=20)
        
        scroll = ctk.CTkScrollableFrame(janela)
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        for produto in produtos:
            frame = ctk.CTkFrame(scroll)
            frame.pack(fill="x", pady=5)
            
            texto = f"⚠️ {produto['nome']}\nEstoque: {produto['estoque']} / Mínimo: {produto['estoque_minimo']}"
            ctk.CTkLabel(
                frame,
                text=texto,
                font=ctk.CTkFont(size=12),
                justify="left"
            ).pack(padx=10, pady=10)
