"""
Tela de Vendas - Registro e listagem de vendas
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from database import Database
from utils import Formatador, Periodo, ExportadorPDF, ExportadorExcel
from tkinter import filedialog

class Vendas(ctk.CTkFrame):
    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.db = db
        self.configure(fg_color="transparent")
        
        # Container principal
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        titulo = ctk.CTkLabel(
            container,
            text="🛒 Gestão de Vendas",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titulo.pack(pady=(0, 20))
        
        # Frame principal dividido
        frame_principal = ctk.CTkFrame(container, fg_color="transparent")
        frame_principal.pack(fill="both", expand=True)
        
        # Formulário de nova venda (esquerda)
        self.criar_formulario_venda(frame_principal)
        
        # Lista de vendas (direita)
        self.criar_lista_vendas(frame_principal)
        
        # Carregar dados
        self.carregar_produtos()
        self.carregar_vendas()
    
    def criar_formulario_venda(self, parent):
        """Cria formulário de nova venda"""
        frame = ctk.CTkFrame(parent)
        frame.pack(side="left", fill="both", padx=(0, 10))
        
        label = ctk.CTkLabel(
            frame,
            text="Nova Venda",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        label.pack(pady=15)
        
        # Scroll
        scroll = ctk.CTkScrollableFrame(frame, width=350)
        scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Produto
        ctk.CTkLabel(scroll, text="Produto *", anchor="w").pack(fill="x", pady=(10, 0))
        self.combo_produto = ctk.CTkComboBox(
            scroll,
            values=["Selecione um produto..."],
            command=self.atualizar_info_produto
        )
        self.combo_produto.pack(fill="x", pady=(5, 10))
        
        # Info do produto
        self.frame_info_produto = ctk.CTkFrame(scroll, fg_color="#e8f4f8")
        self.frame_info_produto.pack(fill="x", pady=(0, 15))
        
        self.label_info_estoque = ctk.CTkLabel(
            self.frame_info_produto,
            text="Estoque disponível: -",
            font=ctk.CTkFont(size=11)
        )
        self.label_info_estoque.pack(pady=(10, 2), padx=10, anchor="w")
        
        self.label_info_preco = ctk.CTkLabel(
            self.frame_info_produto,
            text="Preço: R$ -",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#1f77b4"
        )
        self.label_info_preco.pack(pady=(2, 10), padx=10, anchor="w")
        
        # Quantidade
        ctk.CTkLabel(scroll, text="Quantidade *", anchor="w").pack(fill="x")
        self.entry_quantidade = ctk.CTkEntry(scroll, placeholder_text="0")
        self.entry_quantidade.pack(fill="x", pady=(5, 10))
        self.entry_quantidade.bind("<KeyRelease>", self.calcular_total)
        
        # Cliente
        ctk.CTkLabel(scroll, text="Cliente (opcional)", anchor="w").pack(fill="x")
        self.entry_cliente = ctk.CTkEntry(scroll, placeholder_text="Nome do cliente")
        self.entry_cliente.pack(fill="x", pady=(5, 10))
        
        # Observações
        ctk.CTkLabel(scroll, text="Observações (opcional)", anchor="w").pack(fill="x")
        self.text_observacoes = ctk.CTkTextbox(scroll, height=80)
        self.text_observacoes.pack(fill="x", pady=(5, 15))
        
        # Valor total
        self.label_total = ctk.CTkLabel(
            scroll,
            text="Total: R$ 0,00",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#2ca02c"
        )
        self.label_total.pack(pady=15)
        
        # Botões
        frame_botoes = ctk.CTkFrame(scroll, fg_color="transparent")
        frame_botoes.pack(fill="x", pady=(10, 20))
        
        btn_salvar = ctk.CTkButton(
            frame_botoes,
            text="💰 Registrar Venda",
            command=self.registrar_venda,
            fg_color="#2ca02c",
            hover_color="#28a745",
            height=40
        )
        btn_salvar.pack(fill="x", pady=(0, 5))
        
        btn_limpar = ctk.CTkButton(
            frame_botoes,
            text="🔄 Limpar",
            command=self.limpar_formulario,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        btn_limpar.pack(fill="x")
    
    def criar_lista_vendas(self, parent):
        """Cria lista de vendas"""
        frame = ctk.CTkFrame(parent)
        frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Cabeçalho com filtros
        frame_header = ctk.CTkFrame(frame, fg_color="transparent")
        frame_header.pack(fill="x", pady=10, padx=10)
        
        label = ctk.CTkLabel(
            frame_header,
            text="Histórico de Vendas",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        label.pack(side="left")
        
        # Filtros
        frame_filtros = ctk.CTkFrame(frame)
        frame_filtros.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkLabel(frame_filtros, text="Período:").pack(side="left", padx=(10, 5), pady=10)
        
        self.combo_periodo = ctk.CTkComboBox(
            frame_filtros,
            values=["Hoje", "Esta Semana", "Este Mês", "Este Ano", "Tudo"],
            width=150,
            command=lambda x: self.carregar_vendas()
        )
        self.combo_periodo.set("Este Mês")
        self.combo_periodo.pack(side="left", padx=5)
        
        btn_atualizar = ctk.CTkButton(
            frame_filtros,
            text="🔄",
            width=40,
            command=self.carregar_vendas
        )
        btn_atualizar.pack(side="left", padx=5)
        
        # Botões de exportação
        btn_pdf = ctk.CTkButton(
            frame_filtros,
            text="📄 PDF",
            width=80,
            command=self.exportar_pdf,
            fg_color="#d62728",
            hover_color="#c82333"
        )
        btn_pdf.pack(side="right", padx=(5, 10))
        
        btn_excel = ctk.CTkButton(
            frame_filtros,
            text="📊 Excel",
            width=80,
            command=self.exportar_excel,
            fg_color="#2ca02c",
            hover_color="#28a745"
        )
        btn_excel.pack(side="right", padx=5)
        
        # Resumo
        self.frame_resumo = ctk.CTkFrame(frame)
        self.frame_resumo.pack(fill="x", padx=10, pady=(0, 10))
        
        # Labels de resumo
        frame_resumo_interno = ctk.CTkFrame(self.frame_resumo, fg_color="transparent")
        frame_resumo_interno.pack(fill="x", padx=10, pady=10)
        
        self.label_qtd_vendas = ctk.CTkLabel(
            frame_resumo_interno,
            text="Vendas: 0",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.label_qtd_vendas.pack(side="left", padx=10)
        
        self.label_total_vendas = ctk.CTkLabel(
            frame_resumo_interno,
            text="Total: R$ 0,00",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#2ca02c"
        )
        self.label_total_vendas.pack(side="right", padx=10)
        
        # Lista com scroll
        self.scroll_vendas = ctk.CTkScrollableFrame(frame)
        self.scroll_vendas.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Cabeçalho da tabela
        self.criar_cabecalho_vendas()
    
    def criar_cabecalho_vendas(self):
        """Cria cabeçalho da lista de vendas"""
        frame = ctk.CTkFrame(self.scroll_vendas, fg_color="#1f77b4")
        frame.pack(fill="x", pady=(0, 5))
        
        headers = [
            ("ID", 50),
            ("Data/Hora", 130),
            ("Produto", 180),
            ("Qtd", 50),
            ("Total", 100),
            ("Cliente", 120)
        ]
        
        for texto, largura in headers:
            label = ctk.CTkLabel(
                frame,
                text=texto,
                font=ctk.CTkFont(size=11, weight="bold"),
                width=largura
            )
            label.pack(side="left", padx=5, pady=5)
    
    def carregar_produtos(self):
        """Carrega lista de produtos no combobox"""
        produtos = self.db.listar_produtos()
        valores = ["Selecione um produto..."] + [
            f"{p['nome']} (Est: {p['estoque']})" for p in produtos
        ]
        self.combo_produto.configure(values=valores)
        self.produtos_cache = produtos
    
    def atualizar_info_produto(self, *args):
        """Atualiza informações do produto selecionado"""
        selecao = self.combo_produto.get()
        
        if selecao == "Selecione um produto..." or not hasattr(self, 'produtos_cache'):
            self.label_info_estoque.configure(text="Estoque disponível: -")
            self.label_info_preco.configure(text="Preço: R$ -")
            return
        
        # Extrair nome do produto (remover informação de estoque)
        nome_produto = selecao.split(" (Est:")[0]
        
        # Buscar produto
        for produto in self.produtos_cache:
            if produto['nome'] == nome_produto:
                self.label_info_estoque.configure(
                    text=f"Estoque disponível: {produto['estoque']} unidades"
                )
                self.label_info_preco.configure(
                    text=f"Preço: {Formatador.formatar_moeda(produto['preco_venda'])}"
                )
                
                # Colorir estoque
                if produto['estoque'] <= produto['estoque_minimo']:
                    self.label_info_estoque.configure(text_color="#d62728")
                else:
                    self.label_info_estoque.configure(text_color="gray")
                
                break
        
        self.calcular_total()
    
    def calcular_total(self, *args):
        """Calcula o total da venda"""
        try:
            selecao = self.combo_produto.get()
            if selecao == "Selecione um produto..." or not hasattr(self, 'produtos_cache'):
                self.label_total.configure(text="Total: R$ 0,00")
                return
            
            nome_produto = selecao.split(" (Est:")[0]
            quantidade = int(self.entry_quantidade.get() or 0)
            
            for produto in self.produtos_cache:
                if produto['nome'] == nome_produto:
                    total = produto['preco_venda'] * quantidade
                    self.label_total.configure(
                        text=f"Total: {Formatador.formatar_moeda(total)}"
                    )
                    break
        except:
            self.label_total.configure(text="Total: R$ 0,00")
    
    def registrar_venda(self):
        """Registra uma nova venda"""
        # Validações
        selecao = self.combo_produto.get()
        if selecao == "Selecione um produto...":
            messagebox.showwarning("Atenção", "Selecione um produto!")
            return
        
        try:
            quantidade = int(self.entry_quantidade.get())
            if quantidade <= 0:
                raise ValueError()
        except:
            messagebox.showwarning("Atenção", "Informe uma quantidade válida!")
            return
        
        # Buscar produto
        nome_produto = selecao.split(" (Est:")[0]
        produto_id = None
        
        for produto in self.produtos_cache:
            if produto['nome'] == nome_produto:
                produto_id = produto['id']
                
                # Verificar estoque
                if produto['estoque'] < quantidade:
                    messagebox.showerror(
                        "Erro",
                        f"Estoque insuficiente!\nDisponível: {produto['estoque']}"
                    )
                    return
                break
        
        if not produto_id:
            messagebox.showerror("Erro", "Produto não encontrado!")
            return
        
        # Registrar venda
        try:
            self.db.registrar_venda(
                produto_id=produto_id,
                quantidade=quantidade,
                cliente=self.entry_cliente.get().strip(),
                observacoes=self.text_observacoes.get("1.0", "end").strip()
            )
            
            messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")
            
            # Limpar formulário e atualizar listas
            self.limpar_formulario()
            self.carregar_produtos()  # Atualiza estoque
            self.carregar_vendas()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao registrar venda: {str(e)}")
    
    def limpar_formulario(self):
        """Limpa o formulário de venda"""
        self.combo_produto.set("Selecione um produto...")
        self.entry_quantidade.delete(0, "end")
        self.entry_cliente.delete(0, "end")
        self.text_observacoes.delete("1.0", "end")
        self.label_total.configure(text="Total: R$ 0,00")
        self.label_info_estoque.configure(text="Estoque disponível: -")
        self.label_info_preco.configure(text="Preço: R$ -")
    
    def get_periodo_datas(self):
        """Retorna datas baseado no período selecionado"""
        periodo = self.combo_periodo.get()
        
        if periodo == "Hoje":
            return Periodo.hoje(), Periodo.hoje()
        elif periodo == "Esta Semana":
            return Periodo.inicio_semana(), Periodo.fim_semana()
        elif periodo == "Este Mês":
            return Periodo.inicio_mes(), Periodo.fim_mes()
        elif periodo == "Este Ano":
            return Periodo.inicio_ano(), Periodo.fim_ano()
        else:  # Tudo
            return None, None
    
    def carregar_vendas(self):
        """Carrega lista de vendas"""
        # Limpar lista
        for widget in self.scroll_vendas.winfo_children():
            if widget != self.scroll_vendas.winfo_children()[0]:  # Preservar cabeçalho
                widget.destroy()
        
        data_inicio, data_fim = self.get_periodo_datas()
        vendas = self.db.listar_vendas(data_inicio, data_fim)
        
        # Atualizar resumo
        total_vendas = len(vendas)
        valor_total = sum(v['valor_total'] for v in vendas)
        
        self.label_qtd_vendas.configure(text=f"Vendas: {total_vendas}")
        self.label_total_vendas.configure(
            text=f"Total: {Formatador.formatar_moeda(valor_total)}"
        )
        
        # Listar vendas
        for venda in vendas:
            self.criar_item_venda(venda)
    
    def criar_item_venda(self, venda):
        """Cria item de venda na lista"""
        frame = ctk.CTkFrame(self.scroll_vendas)
        frame.pack(fill="x", pady=2)
        
        # ID
        ctk.CTkLabel(frame, text=str(venda['id']), width=50).pack(side="left", padx=5)
        
        # Data/Hora
        data_formatada = Formatador.formatar_data_hora(venda['data_venda'])
        ctk.CTkLabel(frame, text=data_formatada, width=130).pack(side="left", padx=5)
        
        # Produto
        produto_texto = venda['produto_nome'][:25] + "..." if len(venda['produto_nome']) > 25 else venda['produto_nome']
        ctk.CTkLabel(frame, text=produto_texto, width=180, anchor="w").pack(side="left", padx=5)
        
        # Quantidade
        ctk.CTkLabel(frame, text=str(venda['quantidade']), width=50).pack(side="left", padx=5)
        
        # Total
        ctk.CTkLabel(
            frame,
            text=Formatador.formatar_moeda(venda['valor_total']),
            width=100,
            text_color="#2ca02c",
            font=ctk.CTkFont(weight="bold")
        ).pack(side="left", padx=5)
        
        # Cliente
        cliente_texto = venda['cliente'][:15] + "..." if venda['cliente'] and len(venda['cliente']) > 15 else (venda['cliente'] or "-")
        ctk.CTkLabel(frame, text=cliente_texto, width=120).pack(side="left", padx=5)
    
    def exportar_pdf(self):
        """Exporta vendas para PDF"""
        data_inicio, data_fim = self.get_periodo_datas()
        vendas = self.db.listar_vendas(data_inicio, data_fim)
        
        if not vendas:
            messagebox.showinfo("Atenção", "Nenhuma venda para exportar!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            initialfile=f"vendas_{datetime.now().strftime('%Y%m%d')}.pdf"
        )
        
        if filename:
            try:
                periodo_texto = self.combo_periodo.get()
                ExportadorPDF.gerar_relatorio_vendas(vendas, filename, periodo_texto)
                messagebox.showinfo("Sucesso", f"Relatório exportado para:\n{filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")
    
    def exportar_excel(self):
        """Exporta vendas para Excel"""
        data_inicio, data_fim = self.get_periodo_datas()
        vendas = self.db.listar_vendas(data_inicio, data_fim)
        
        if not vendas:
            messagebox.showinfo("Atenção", "Nenhuma venda para exportar!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")],
            initialfile=f"vendas_{datetime.now().strftime('%Y%m%d')}.xlsx"
        )
        
        if filename:
            try:
                ExportadorExcel.gerar_relatorio_vendas(vendas, filename)
                messagebox.showinfo("Sucesso", f"Relatório exportado para:\n{filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")
