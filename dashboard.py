"""
Tela de Dashboard - Painel principal com resumo e KPIs
"""

import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime
from database import Database
from utils import Formatador, Periodo

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.db = db
        self.configure(fg_color="transparent")
        
        # Container principal com scroll
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        titulo = ctk.CTkLabel(
            self.scroll_frame,
            text="📊 Dashboard",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titulo.pack(pady=(0, 20))
        
        # Frame de filtros de período
        self.criar_filtros_periodo()
        
        # Cards de resumo (KPIs)
        self.criar_cards_kpi()
        
        # Gráficos
        self.criar_graficos()
        
        # Tabela de produtos mais vendidos
        self.criar_tabela_top_produtos()
        
        # Carregar dados iniciais
        self.atualizar_dashboard()
    
    def criar_filtros_periodo(self):
        """Cria filtros de período"""
        frame_filtros = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        frame_filtros.pack(fill="x", pady=(0, 20))
        
        label = ctk.CTkLabel(
            frame_filtros,
            text="Período:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label.pack(side="left", padx=5)
        
        periodos = ["Hoje", "Ontem", "Esta Semana", "Este Mês", "Este Ano", "Mês Anterior"]
        
        self.combo_periodo = ctk.CTkComboBox(
            frame_filtros,
            values=periodos,
            command=self.atualizar_dashboard,
            width=200
        )
        self.combo_periodo.set("Este Mês")
        self.combo_periodo.pack(side="left", padx=5)
        
        btn_atualizar = ctk.CTkButton(
            frame_filtros,
            text="🔄 Atualizar",
            command=self.atualizar_dashboard,
            width=120
        )
        btn_atualizar.pack(side="left", padx=5)
    
    def criar_cards_kpi(self):
        """Cria cards com indicadores principais"""
        self.frame_cards = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.frame_cards.pack(fill="x", pady=(0, 20))
        
        # Criar 4 cards
        self.card_receita = self.criar_card(
            self.frame_cards,
            "💰 Receita Total",
            "R$ 0,00",
            "#1f77b4"
        )
        self.card_receita.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.card_lucro = self.criar_card(
            self.frame_cards,
            "📈 Lucro Líquido",
            "R$ 0,00",
            "#2ca02c"
        )
        self.card_lucro.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.card_vendas = self.criar_card(
            self.frame_cards,
            "🛒 Total de Vendas",
            "0",
            "#ff7f0e"
        )
        self.card_vendas.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        self.card_ticket = self.criar_card(
            self.frame_cards,
            "🎫 Ticket Médio",
            "R$ 0,00",
            "#9467bd"
        )
        self.card_ticket.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")
        
        # Segunda linha de cards
        self.card_estoque = self.criar_card(
            self.frame_cards,
            "📦 Valor em Estoque",
            "R$ 0,00",
            "#8c564b"
        )
        self.card_estoque.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.card_despesas = self.criar_card(
            self.frame_cards,
            "💸 Despesas",
            "R$ 0,00",
            "#e377c2"
        )
        self.card_despesas.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        self.card_margem = self.criar_card(
            self.frame_cards,
            "📊 Margem Média",
            "0%",
            "#17becf"
        )
        self.card_margem.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        
        self.card_alertas = self.criar_card(
            self.frame_cards,
            "⚠️ Alertas de Estoque",
            "0",
            "#d62728"
        )
        self.card_alertas.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")
        
        # Configurar grid
        for i in range(4):
            self.frame_cards.columnconfigure(i, weight=1)
    
    def criar_card(self, parent, titulo, valor, cor):
        """Cria um card de KPI"""
        card = ctk.CTkFrame(parent, corner_radius=10)
        
        # Título do card
        label_titulo = ctk.CTkLabel(
            card,
            text=titulo,
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )
        label_titulo.pack(pady=(15, 5))
        
        # Valor do card
        label_valor = ctk.CTkLabel(
            card,
            text=valor,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=cor
        )
        label_valor.pack(pady=(5, 15))
        
        # Salvar referência ao label de valor
        card.label_valor = label_valor
        
        return card
    
    def criar_graficos(self):
        """Cria área de gráficos"""
        frame_graficos = ctk.CTkFrame(self.scroll_frame)
        frame_graficos.pack(fill="both", expand=True, pady=(0, 20))
        
        # Frame esquerdo - Gráfico de vendas/lucro
        frame_esq = ctk.CTkFrame(frame_graficos)
        frame_esq.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
        
        label_grafico1 = ctk.CTkLabel(
            frame_esq,
            text="📈 Evolução de Vendas",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        label_grafico1.pack(pady=10)
        
        # Criar gráfico de vendas
        self.figura_vendas = Figure(figsize=(6, 4), dpi=80)
        self.ax_vendas = self.figura_vendas.add_subplot(111)
        self.canvas_vendas = FigureCanvasTkAgg(self.figura_vendas, frame_esq)
        self.canvas_vendas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame direito - Gráfico de produtos
        frame_dir = ctk.CTkFrame(frame_graficos)
        frame_dir.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)
        
        label_grafico2 = ctk.CTkLabel(
            frame_dir,
            text="🏆 Produtos Mais Vendidos",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        label_grafico2.pack(pady=10)
        
        # Criar gráfico de produtos
        self.figura_produtos = Figure(figsize=(6, 4), dpi=80)
        self.ax_produtos = self.figura_produtos.add_subplot(111)
        self.canvas_produtos = FigureCanvasTkAgg(self.figura_produtos, frame_dir)
        self.canvas_produtos.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    def criar_tabela_top_produtos(self):
        """Cria tabela com top produtos"""
        frame_tabela = ctk.CTkFrame(self.scroll_frame)
        frame_tabela.pack(fill="x", pady=(0, 20), padx=10)
        
        label_titulo = ctk.CTkLabel(
            frame_tabela,
            text="🔝 Top 5 Produtos Mais Vendidos",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        label_titulo.pack(pady=10)
        
        # Frame para a tabela
        self.frame_tabela_produtos = ctk.CTkFrame(frame_tabela)
        self.frame_tabela_produtos.pack(fill="x", padx=10, pady=(0, 10))
    
    def get_periodo_datas(self):
        """Retorna datas de início e fim baseado no período selecionado"""
        periodo = self.combo_periodo.get()
        
        if periodo == "Hoje":
            return Periodo.hoje(), Periodo.hoje()
        elif periodo == "Ontem":
            return Periodo.ontem(), Periodo.ontem()
        elif periodo == "Esta Semana":
            return Periodo.inicio_semana(), Periodo.fim_semana()
        elif periodo == "Este Mês":
            return Periodo.inicio_mes(), Periodo.fim_mes()
        elif periodo == "Este Ano":
            return Periodo.inicio_ano(), Periodo.fim_ano()
        elif periodo == "Mês Anterior":
            return Periodo.mes_anterior()
        else:
            return Periodo.inicio_mes(), Periodo.fim_mes()
    
    def atualizar_dashboard(self, *args):
        """Atualiza todos os dados do dashboard"""
        data_inicio, data_fim = self.get_periodo_datas()
        
        # Atualizar KPIs
        self.atualizar_kpis(data_inicio, data_fim)
        
        # Atualizar gráficos
        self.atualizar_grafico_vendas(data_inicio, data_fim)
        self.atualizar_grafico_produtos()
        
        # Atualizar tabela
        self.atualizar_tabela_produtos()
    
    def atualizar_kpis(self, data_inicio, data_fim):
        """Atualiza os cards de KPI"""
        # Resumo de vendas
        resumo = self.db.get_resumo_vendas(data_inicio, data_fim)
        self.card_receita.label_valor.configure(
            text=Formatador.formatar_moeda(resumo['receita_total'])
        )
        self.card_vendas.label_valor.configure(
            text=str(resumo['total_vendas'])
        )
        self.card_ticket.label_valor.configure(
            text=Formatador.formatar_moeda(resumo['ticket_medio'])
        )
        
        # Lucro e despesas
        lucro_data = self.db.get_lucro_periodo(data_inicio, data_fim)
        self.card_lucro.label_valor.configure(
            text=Formatador.formatar_moeda(lucro_data['lucro_liquido'])
        )
        self.card_despesas.label_valor.configure(
            text=Formatador.formatar_moeda(lucro_data['despesas'])
        )
        
        # Valor em estoque
        valor_estoque = self.db.get_valor_estoque_total()
        self.card_estoque.label_valor.configure(
            text=Formatador.formatar_moeda(valor_estoque)
        )
        
        # Margem média
        if resumo['receita_total'] > 0:
            margem = (lucro_data['lucro_bruto'] / resumo['receita_total']) * 100
        else:
            margem = 0
        self.card_margem.label_valor.configure(
            text=Formatador.formatar_porcentagem(margem)
        )
        
        # Alertas de estoque
        produtos_baixo = self.db.produtos_estoque_baixo()
        self.card_alertas.label_valor.configure(
            text=str(len(produtos_baixo))
        )
    
    def atualizar_grafico_vendas(self, data_inicio, data_fim):
        """Atualiza gráfico de evolução de vendas"""
        self.ax_vendas.clear()
        
        # Buscar vendas do período
        vendas = self.db.listar_vendas(data_inicio, data_fim)
        
        if vendas:
            # Agrupar vendas por data
            vendas_por_data = {}
            for venda in vendas:
                data = venda['data_venda'][:10]  # Pegar só a data
                if data not in vendas_por_data:
                    vendas_por_data[data] = 0
                vendas_por_data[data] += venda['valor_total']
            
            # Ordenar por data
            datas = sorted(vendas_por_data.keys())
            valores = [vendas_por_data[data] for data in datas]
            
            # Formatar datas para exibição
            datas_formatadas = [Formatador.formatar_data(data + " 00:00:00") for data in datas]
            
            # Plotar
            self.ax_vendas.plot(datas_formatadas, valores, marker='o', linewidth=2, color='#1f77b4')
            self.ax_vendas.fill_between(range(len(valores)), valores, alpha=0.3, color='#1f77b4')
            self.ax_vendas.set_xlabel('Data', fontsize=10)
            self.ax_vendas.set_ylabel('Valor (R$)', fontsize=10)
            self.ax_vendas.grid(True, alpha=0.3)
            self.ax_vendas.tick_params(axis='x', rotation=45, labelsize=8)
            self.ax_vendas.tick_params(axis='y', labelsize=8)
        else:
            self.ax_vendas.text(0.5, 0.5, 'Sem dados no período', 
                              ha='center', va='center', fontsize=12)
        
        self.figura_vendas.tight_layout()
        self.canvas_vendas.draw()
    
    def atualizar_grafico_produtos(self):
        """Atualiza gráfico de produtos mais vendidos"""
        self.ax_produtos.clear()
        
        produtos = self.db.get_produtos_mais_vendidos(5)
        
        if produtos:
            nomes = [p['nome'][:15] + '...' if len(p['nome']) > 15 else p['nome'] 
                    for p in produtos]
            quantidades = [p['quantidade_vendida'] for p in produtos]
            
            cores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
            
            self.ax_produtos.barh(nomes, quantidades, color=cores[:len(nomes)])
            self.ax_produtos.set_xlabel('Quantidade Vendida', fontsize=10)
            self.ax_produtos.tick_params(axis='both', labelsize=9)
            self.ax_produtos.invert_yaxis()
            
            # Adicionar valores nas barras
            for i, v in enumerate(quantidades):
                self.ax_produtos.text(v, i, f' {v}', va='center', fontsize=9)
        else:
            self.ax_produtos.text(0.5, 0.5, 'Sem dados disponíveis', 
                                ha='center', va='center', fontsize=12)
        
        self.figura_produtos.tight_layout()
        self.canvas_produtos.draw()
    
    def atualizar_tabela_produtos(self):
        """Atualiza tabela de top produtos"""
        # Limpar tabela anterior
        for widget in self.frame_tabela_produtos.winfo_children():
            widget.destroy()
        
        produtos = self.db.get_produtos_mais_vendidos(5)
        
        if produtos:
            # Cabeçalho
            headers = ["#", "Produto", "Qtd Vendida", "Receita"]
            for i, header in enumerate(headers):
                label = ctk.CTkLabel(
                    self.frame_tabela_produtos,
                    text=header,
                    font=ctk.CTkFont(size=12, weight="bold")
                )
                label.grid(row=0, column=i, padx=10, pady=5, sticky="w")
            
            # Dados
            for idx, produto in enumerate(produtos, 1):
                ctk.CTkLabel(
                    self.frame_tabela_produtos,
                    text=str(idx)
                ).grid(row=idx, column=0, padx=10, pady=5, sticky="w")
                
                ctk.CTkLabel(
                    self.frame_tabela_produtos,
                    text=produto['nome']
                ).grid(row=idx, column=1, padx=10, pady=5, sticky="w")
                
                ctk.CTkLabel(
                    self.frame_tabela_produtos,
                    text=str(produto['quantidade_vendida'])
                ).grid(row=idx, column=2, padx=10, pady=5, sticky="w")
                
                ctk.CTkLabel(
                    self.frame_tabela_produtos,
                    text=Formatador.formatar_moeda(produto['receita_total'])
                ).grid(row=idx, column=3, padx=10, pady=5, sticky="w")
        else:
            label = ctk.CTkLabel(
                self.frame_tabela_produtos,
                text="Nenhuma venda registrada",
                font=ctk.CTkFont(size=12)
            )
            label.pack(pady=20)
