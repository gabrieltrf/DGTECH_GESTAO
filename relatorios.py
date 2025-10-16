"""
Tela de Relatórios Avançados
Análises inteligentes, gráficos de evolução e comparativos
"""

import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from database import Database
from analytics import Analytics
from utils import Formatador, Periodo
from tkinter import messagebox

class RelatoriosAvancados(ctk.CTkFrame):
    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.db = db
        self.analytics = Analytics(db)
        self.configure(fg_color="transparent")
        
        # Container principal com tabs
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        titulo = ctk.CTkLabel(
            self.scroll_frame,
            text="📊 Relatórios Avançados",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titulo.pack(pady=(0, 20))
        
        # Tabs
        self.tabview = ctk.CTkTabview(self.scroll_frame, height=750)
        self.tabview.pack(fill="both", expand=True)
        
        # Criar abas
        self.tab_abc = self.tabview.add("🎯 Análise ABC")
        self.tab_evolucao = self.tabview.add("📈 Evolução")
        self.tab_sazonalidade = self.tabview.add("📅 Sazonalidade")
        self.tab_previsao = self.tabview.add("🔮 Previsões")
        self.tab_alertas = self.tabview.add("⚠️ Alertas")
        self.tab_metas = self.tabview.add("🎯 Metas")
        
        # Carregar conteúdo das abas
        self.criar_aba_abc()
        self.criar_aba_evolucao()
        self.criar_aba_sazonalidade()
        self.criar_aba_previsao()
        self.criar_aba_alertas()
        self.criar_aba_metas()
    
    # ==================== ABA ANÁLISE ABC ====================
    
    def criar_aba_abc(self):
        """Cria aba de Análise ABC"""
        frame = ctk.CTkFrame(self.tab_abc)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Explicação
        texto_explicacao = """
        📊 Análise ABC - Classificação de Produtos por Importância
        
        • Classe A: Produtos que geram 80% da receita (Alta prioridade)
        • Classe B: Produtos que geram 15% da receita (Média prioridade)  
        • Classe C: Produtos que geram 5% da receita (Baixa prioridade)
        • Sem Vendas: Produtos sem movimentação
        """
        
        label_exp = ctk.CTkLabel(
            frame,
            text=texto_explicacao,
            font=ctk.CTkFont(size=11),
            justify="left"
        )
        label_exp.pack(pady=10, padx=10)
        
        # Botão atualizar
        btn_atualizar = ctk.CTkButton(
            frame,
            text="🔄 Atualizar Análise",
            command=self.atualizar_abc,
            fg_color="#2ca02c",
            hover_color="#28a745"
        )
        btn_atualizar.pack(pady=10)
        
        # Frame para gráfico
        self.frame_grafico_abc = ctk.CTkFrame(frame)
        self.frame_grafico_abc.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame para tabelas
        self.frame_tabelas_abc = ctk.CTkScrollableFrame(frame, height=300)
        self.frame_tabelas_abc.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.atualizar_abc()
    
    def atualizar_abc(self):
        """Atualiza análise ABC"""
        # Limpar
        for widget in self.frame_grafico_abc.winfo_children():
            widget.destroy()
        for widget in self.frame_tabelas_abc.winfo_children():
            widget.destroy()
        
        # Obter dados
        abc = self.analytics.analise_abc()
        
        # Gráfico de pizza
        fig = Figure(figsize=(8, 5), dpi=80)
        ax = fig.add_subplot(111)
        
        valores = [
            len(abc['A']),
            len(abc['B']),
            len(abc['C']),
            len(abc['sem_vendas'])
        ]
        labels = [
            f"Classe A ({len(abc['A'])} produtos)",
            f"Classe B ({len(abc['B'])} produtos)",
            f"Classe C ({len(abc['C'])} produtos)",
            f"Sem vendas ({len(abc['sem_vendas'])} produtos)"
        ]
        cores = ['#2ca02c', '#ff7f0e', '#1f77b4', '#d62728']
        
        ax.pie(valores, labels=labels, autopct='%1.1f%%', colors=cores, startangle=90)
        ax.set_title('Distribuição de Produtos por Classe ABC', fontsize=14, weight='bold')
        
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, self.frame_grafico_abc)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()
        
        # Tabelas por classe
        for classe, cor, produtos in [
            ('A', '#2ca02c', abc['A'][:10]),
            ('B', '#ff7f0e', abc['B'][:10]),
            ('C', '#1f77b4', abc['C'][:10])
        ]:
            if produtos:
                frame_classe = ctk.CTkFrame(self.frame_tabelas_abc)
                frame_classe.pack(fill="x", pady=10, padx=5)
                
                ctk.CTkLabel(
                    frame_classe,
                    text=f"📊 Classe {classe} - Top 10",
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=cor
                ).pack(pady=10)
                
                for prod in produtos:
                    texto = f"{prod['nome']}: {Formatador.formatar_moeda(prod['receita_total'])} ({prod['participacao']:.1f}%)"
                    ctk.CTkLabel(
                        frame_classe,
                        text=texto,
                        font=ctk.CTkFont(size=11)
                    ).pack(anchor="w", padx=10, pady=2)
    
    # ==================== ABA EVOLUÇÃO ====================
    
    def criar_aba_evolucao(self):
        """Cria aba de evolução de estoque e vendas"""
        frame = ctk.CTkFrame(self.tab_evolucao)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Controles
        frame_controles = ctk.CTkFrame(frame, fg_color="transparent")
        frame_controles.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            frame_controles,
            text="Período:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left", padx=5)
        
        self.combo_periodo_evolucao = ctk.CTkComboBox(
            frame_controles,
            values=["Últimos 7 dias", "Últimos 30 dias", "Últimos 90 dias", "Este Ano"],
            width=150
        )
        self.combo_periodo_evolucao.set("Últimos 30 dias")
        self.combo_periodo_evolucao.pack(side="left", padx=5)
        
        btn_atualizar = ctk.CTkButton(
            frame_controles,
            text="🔄 Atualizar",
            command=self.atualizar_evolucao,
            width=100
        )
        btn_atualizar.pack(side="left", padx=5)
        
        # Gráficos
        self.frame_evolucao_graficos = ctk.CTkFrame(frame)
        self.frame_evolucao_graficos.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.atualizar_evolucao()
    
    def atualizar_evolucao(self):
        """Atualiza gráficos de evolução"""
        for widget in self.frame_evolucao_graficos.winfo_children():
            widget.destroy()
        
        # Determinar período
        periodo_selecionado = self.combo_periodo_evolucao.get()
        if "7 dias" in periodo_selecionado:
            data_inicio, data_fim = Periodo.ultimos_n_dias(7)
        elif "30 dias" in periodo_selecionado:
            data_inicio, data_fim = Periodo.ultimos_n_dias(30)
        elif "90 dias" in periodo_selecionado:
            data_inicio, data_fim = Periodo.ultimos_n_dias(90)
        else:
            data_inicio, data_fim = Periodo.inicio_ano(), Periodo.fim_ano()
        
        vendas = self.db.listar_vendas(data_inicio, data_fim)
        
        # Agrupar por data
        vendas_por_data = {}
        estoque_por_data = {}
        
        for venda in vendas:
            data = venda['data_venda'][:10]
            if data not in vendas_por_data:
                vendas_por_data[data] = {'receita': 0, 'quantidade': 0}
            
            vendas_por_data[data]['receita'] += venda['valor_total']
            vendas_por_data[data]['quantidade'] += venda['quantidade']
        
        # Criar figura com 2 subplots
        fig = Figure(figsize=(12, 8), dpi=80)
        
        # Gráfico 1: Receita ao longo do tempo
        ax1 = fig.add_subplot(211)
        datas = sorted(vendas_por_data.keys())
        receitas = [vendas_por_data[d]['receita'] for d in datas]
        datas_formatadas = [Formatador.formatar_data(d + " 00:00:00") for d in datas]
        
        ax1.plot(datas_formatadas, receitas, marker='o', linewidth=2, color='#2ca02c', markersize=6)
        ax1.fill_between(range(len(receitas)), receitas, alpha=0.3, color='#2ca02c')
        ax1.set_title('Evolução da Receita', fontsize=14, weight='bold')
        ax1.set_xlabel('Data', fontsize=10)
        ax1.set_ylabel('Receita (R$)', fontsize=10)
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45, labelsize=8)
        
        # Gráfico 2: Quantidade vendida
        ax2 = fig.add_subplot(212)
        quantidades = [vendas_por_data[d]['quantidade'] for d in datas]
        
        ax2.bar(datas_formatadas, quantidades, color='#1f77b4', alpha=0.7)
        ax2.set_title('Evolução da Quantidade Vendida', fontsize=14, weight='bold')
        ax2.set_xlabel('Data', fontsize=10)
        ax2.set_ylabel('Quantidade', fontsize=10)
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.tick_params(axis='x', rotation=45, labelsize=8)
        
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, self.frame_evolucao_graficos)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()
    
    # ==================== ABA SAZONALIDADE ====================
    
    def criar_aba_sazonalidade(self):
        """Cria aba de análise de sazonalidade"""
        frame = ctk.CTkFrame(self.tab_sazonalidade)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botão atualizar
        btn_atualizar = ctk.CTkButton(
            frame,
            text="🔄 Atualizar Análise",
            command=self.atualizar_sazonalidade,
            fg_color="#2ca02c",
            hover_color="#28a745"
        )
        btn_atualizar.pack(pady=10)
        
        # Frame para gráficos
        self.frame_sazonalidade = ctk.CTkFrame(frame)
        self.frame_sazonalidade.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.atualizar_sazonalidade()
    
    def atualizar_sazonalidade(self):
        """Atualiza gráficos de sazonalidade"""
        for widget in self.frame_sazonalidade.winfo_children():
            widget.destroy()
        
        dados = self.analytics.analise_sazonalidade()
        
        if not dados:
            ctk.CTkLabel(
                self.frame_sazonalidade,
                text="Sem dados suficientes para análise de sazonalidade",
                font=ctk.CTkFont(size=14)
            ).pack(pady=50)
            return
        
        # Criar figura com 3 subplots
        fig = Figure(figsize=(12, 10), dpi=80)
        
        # Gráfico 1: Vendas por dia da semana
        ax1 = fig.add_subplot(311)
        ax1.bar(dados['por_dia_semana']['labels'], dados['por_dia_semana']['valores'], 
                color='#1f77b4', alpha=0.7)
        ax1.set_title('Vendas por Dia da Semana', fontsize=12, weight='bold')
        ax1.set_ylabel('Receita (R$)', fontsize=10)
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Gráfico 2: Vendas por mês
        ax2 = fig.add_subplot(312)
        ax2.bar(dados['por_mes']['labels'], dados['por_mes']['valores'], 
                color='#2ca02c', alpha=0.7)
        ax2.set_title('Vendas por Mês', fontsize=12, weight='bold')
        ax2.set_ylabel('Receita (R$)', fontsize=10)
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Gráfico 3: Vendas por hora (se houver dados)
        ax3 = fig.add_subplot(313)
        horas_com_vendas = [i for i, v in enumerate(dados['por_hora']['valores']) if v > 0]
        if horas_com_vendas:
            labels_hora = [dados['por_hora']['labels'][i] for i in horas_com_vendas]
            valores_hora = [dados['por_hora']['valores'][i] for i in horas_com_vendas]
            ax3.plot(labels_hora, valores_hora, marker='o', linewidth=2, color='#ff7f0e', markersize=6)
            ax3.fill_between(range(len(valores_hora)), valores_hora, alpha=0.3, color='#ff7f0e')
        ax3.set_title('Vendas por Hora do Dia', fontsize=12, weight='bold')
        ax3.set_xlabel('Hora', fontsize=10)
        ax3.set_ylabel('Receita (R$)', fontsize=10)
        ax3.grid(True, alpha=0.3)
        
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, self.frame_sazonalidade)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()
    
    # ==================== ABA PREVISÕES ====================
    
    def criar_aba_previsao(self):
        """Cria aba de previsões"""
        frame = ctk.CTkFrame(self.tab_previsao)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botão atualizar
        btn_atualizar = ctk.CTkButton(
            frame,
            text="🔄 Atualizar Previsões",
            command=self.atualizar_previsoes,
            fg_color="#2ca02c",
            hover_color="#28a745"
        )
        btn_atualizar.pack(pady=10)
        
        # Frame para conteúdo
        self.frame_previsoes = ctk.CTkScrollableFrame(frame, height=650)
        self.frame_previsoes.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.atualizar_previsoes()
    
    def atualizar_previsoes(self):
        """Atualiza previsões"""
        for widget in self.frame_previsoes.winfo_children():
            widget.destroy()
        
        # 1. Previsão de vendas
        previsao = self.analytics.previsao_vendas(30)
        
        frame_prev_vendas = ctk.CTkFrame(self.frame_previsoes)
        frame_prev_vendas.pack(fill="x", pady=10, padx=5)
        
        ctk.CTkLabel(
            frame_prev_vendas,
            text="🔮 Previsão de Vendas (Próximos 30 dias)",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        cards_previsao = ctk.CTkFrame(frame_prev_vendas, fg_color="transparent")
        cards_previsao.pack(fill="x", padx=10, pady=10)
        
        # Cards
        self.criar_card_previsao(
            cards_previsao,
            "💰 Receita Prevista",
            Formatador.formatar_moeda(previsao.get('previsao_receita', 0)),
            "#1f77b4"
        ).pack(side="left", expand=True, fill="x", padx=5)
        
        self.criar_card_previsao(
            cards_previsao,
            "📈 Lucro Previsto",
            Formatador.formatar_moeda(previsao.get('previsao_lucro', 0)),
            "#2ca02c"
        ).pack(side="left", expand=True, fill="x", padx=5)
        
        self.criar_card_previsao(
            cards_previsao,
            "📊 Confiança",
            f"{previsao.get('confianca', 0):.0f}%",
            "#ff7f0e"
        ).pack(side="left", expand=True, fill="x", padx=5)
        
        self.criar_card_previsao(
            cards_previsao,
            "📉 Tendência",
            previsao.get('tendencia', 'N/A'),
            "#9467bd"
        ).pack(side="left", expand=True, fill="x", padx=5)
        
        # 2. Previsão de reposição
        reposicoes = self.analytics.previsao_reposicao(60)
        
        frame_repos = ctk.CTkFrame(self.frame_previsoes)
        frame_repos.pack(fill="x", pady=10, padx=5)
        
        ctk.CTkLabel(
            frame_repos,
            text="📦 Previsão de Reposição de Estoque",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        if reposicoes:
            # Cabeçalho
            frame_header = ctk.CTkFrame(frame_repos, fg_color="#1f77b4")
            frame_header.pack(fill="x", padx=10, pady=5)
            
            headers = ["Produto", "Estoque", "Dias Rest.", "Data Repos.", "Qtd Sugerida", "Urgência"]
            for h in headers:
                ctk.CTkLabel(
                    frame_header,
                    text=h,
                    font=ctk.CTkFont(size=11, weight="bold"),
                    width=120
                ).pack(side="left", padx=5, pady=5)
            
            # Dados
            for repos in reposicoes[:10]:  # Top 10
                cor_urgencia = {
                    'ALTA': '#d62728',
                    'MÉDIA': '#ff7f0e',
                    'BAIXA': '#2ca02c'
                }.get(repos['urgencia'], 'gray')
                
                frame_item = ctk.CTkFrame(frame_repos)
                frame_item.pack(fill="x", padx=10, pady=2)
                
                ctk.CTkLabel(frame_item, text=repos['produto_nome'][:20], width=120).pack(side="left", padx=5)
                ctk.CTkLabel(frame_item, text=str(repos['estoque_atual']), width=120).pack(side="left", padx=5)
                ctk.CTkLabel(frame_item, text=str(repos['dias_restantes']), width=120).pack(side="left", padx=5)
                ctk.CTkLabel(frame_item, text=Formatador.formatar_data(repos['data_reposicao'] + " 00:00:00"), width=120).pack(side="left", padx=5)
                ctk.CTkLabel(frame_item, text=str(repos['qtd_sugerida']), width=120).pack(side="left", padx=5)
                ctk.CTkLabel(frame_item, text=repos['urgencia'], width=120, text_color=cor_urgencia, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=5)
        else:
            ctk.CTkLabel(
                frame_repos,
                text="Nenhuma previsão de reposição necessária",
                font=ctk.CTkFont(size=12)
            ).pack(pady=20)
    
    def criar_card_previsao(self, parent, titulo, valor, cor):
        """Cria card de previsão"""
        card = ctk.CTkFrame(parent, corner_radius=10)
        
        ctk.CTkLabel(
            card,
            text=titulo,
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(pady=(10, 5))
        
        ctk.CTkLabel(
            card,
            text=valor,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=cor
        ).pack(pady=(5, 10))
        
        return card
    
    # ==================== ABA ALERTAS ====================
    
    def criar_aba_alertas(self):
        """Cria aba de alertas inteligentes"""
        frame = ctk.CTkFrame(self.tab_alertas)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botão atualizar
        btn_atualizar = ctk.CTkButton(
            frame,
            text="🔄 Atualizar Alertas",
            command=self.atualizar_alertas,
            fg_color="#2ca02c",
            hover_color="#28a745"
        )
        btn_atualizar.pack(pady=10)
        
        # Frame para alertas
        self.frame_alertas = ctk.CTkScrollableFrame(frame, height=650)
        self.frame_alertas.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.atualizar_alertas()
    
    def atualizar_alertas(self):
        """Atualiza alertas inteligentes"""
        for widget in self.frame_alertas.winfo_children():
            widget.destroy()
        
        alertas = self.analytics.gerar_alertas_inteligentes()
        
        if not alertas:
            ctk.CTkLabel(
                self.frame_alertas,
                text="✅ Nenhum alerta no momento!",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#2ca02c"
            ).pack(pady=50)
            return
        
        for alerta in alertas:
            cor_prioridade = {
                'ALTA': '#d62728',
                'MÉDIA': '#ff7f0e',
                'BAIXA': '#1f77b4'
            }.get(alerta['prioridade'], 'gray')
            
            frame_alerta = ctk.CTkFrame(self.frame_alertas, fg_color=cor_prioridade, corner_radius=10)
            frame_alerta.pack(fill="x", pady=5, padx=5)
            
            # Conteúdo
            frame_conteudo = ctk.CTkFrame(frame_alerta, fg_color="transparent")
            frame_conteudo.pack(fill="x", padx=15, pady=15)
            
            # Ícone e título
            ctk.CTkLabel(
                frame_conteudo,
                text=f"{alerta['icone']} {alerta['titulo']}",
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(anchor="w")
            
            # Mensagem
            ctk.CTkLabel(
                frame_conteudo,
                text=alerta['mensagem'],
                font=ctk.CTkFont(size=11)
            ).pack(anchor="w", pady=(5, 2))
            
            # Ação sugerida
            ctk.CTkLabel(
                frame_conteudo,
                text=f"💡 {alerta['acao']}",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#d4edda"
            ).pack(anchor="w", pady=(2, 0))
    
    # ==================== ABA METAS ====================
    
    def criar_aba_metas(self):
        """Cria aba de metas"""
        frame = ctk.CTkFrame(self.tab_metas)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botões
        frame_btns = ctk.CTkFrame(frame, fg_color="transparent")
        frame_btns.pack(fill="x", pady=10)
        
        btn_nova = ctk.CTkButton(
            frame_btns,
            text="➕ Nova Meta",
            command=self.nova_meta,
            fg_color="#2ca02c",
            hover_color="#28a745"
        )
        btn_nova.pack(side="left", padx=5)
        
        btn_atualizar = ctk.CTkButton(
            frame_btns,
            text="🔄 Atualizar",
            command=self.atualizar_metas
        )
        btn_atualizar.pack(side="left", padx=5)
        
        # Frame para metas
        self.frame_metas = ctk.CTkScrollableFrame(frame, height=650)
        self.frame_metas.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.atualizar_metas()
    
    def nova_meta(self):
        """Abre diálogo para criar nova meta"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Nova Meta")
        dialog.geometry("400x450")
        dialog.grab_set()
        
        # Tipo
        ctk.CTkLabel(dialog, text="Tipo de Meta:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(20, 5))
        combo_tipo = ctk.CTkComboBox(dialog, values=["RECEITA", "LUCRO", "VENDAS"], width=300)
        combo_tipo.pack(pady=5)
        
        # Valor
        ctk.CTkLabel(dialog, text="Valor da Meta:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5))
        entry_valor = ctk.CTkEntry(dialog, width=300, placeholder_text="Ex: 10000")
        entry_valor.pack(pady=5)
        
        # Período
        ctk.CTkLabel(dialog, text="Período:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5))
        combo_periodo = ctk.CTkComboBox(dialog, values=["MENSAL", "TRIMESTRAL", "SEMESTRAL", "ANUAL"], width=300)
        combo_periodo.pack(pady=5)
        
        # Data início
        ctk.CTkLabel(dialog, text="Data Início (AAAA-MM-DD):", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5))
        entry_inicio = ctk.CTkEntry(dialog, width=300, placeholder_text=Periodo.inicio_mes())
        entry_inicio.insert(0, Periodo.inicio_mes())
        entry_inicio.pack(pady=5)
        
        # Data fim
        ctk.CTkLabel(dialog, text="Data Fim (AAAA-MM-DD):", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5))
        entry_fim = ctk.CTkEntry(dialog, width=300, placeholder_text=Periodo.fim_mes())
        entry_fim.insert(0, Periodo.fim_mes())
        entry_fim.pack(pady=5)
        
        # Botões
        frame_btns = ctk.CTkFrame(dialog, fg_color="transparent")
        frame_btns.pack(pady=20)
        
        def salvar():
            try:
                valor = float(entry_valor.get().replace(",", "."))
                self.db.adicionar_meta(
                    tipo=combo_tipo.get(),
                    valor_meta=valor,
                    periodo=combo_periodo.get(),
                    data_inicio=entry_inicio.get(),
                    data_fim=entry_fim.get()
                )
                messagebox.showinfo("Sucesso", "Meta criada com sucesso!")
                dialog.destroy()
                self.atualizar_metas()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao criar meta: {str(e)}")
        
        ctk.CTkButton(
            frame_btns,
            text="💾 Salvar",
            command=salvar,
            fg_color="#2ca02c",
            hover_color="#28a745",
            width=120
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            frame_btns,
            text="❌ Cancelar",
            command=dialog.destroy,
            fg_color="#6c757d",
            hover_color="#5a6268",
            width=120
        ).pack(side="left", padx=5)
    
    def atualizar_metas(self):
        """Atualiza lista de metas"""
        for widget in self.frame_metas.winfo_children():
            widget.destroy()
        
        metas = self.db.listar_metas()
        
        if not metas:
            ctk.CTkLabel(
                self.frame_metas,
                text="Nenhuma meta cadastrada. Clique em '➕ Nova Meta' para começar!",
                font=ctk.CTkFont(size=14)
            ).pack(pady=50)
            return
        
        for meta in metas:
            progresso_data = self.db.progresso_meta(meta['id'])
            
            if not progresso_data:
                continue
            
            frame_meta = ctk.CTkFrame(self.frame_metas, corner_radius=10)
            frame_meta.pack(fill="x", pady=10, padx=5)
            
            # Cabeçalho
            frame_header = ctk.CTkFrame(frame_meta, fg_color="transparent")
            frame_header.pack(fill="x", padx=15, pady=10)
            
            icones = {'RECEITA': '💰', 'LUCRO': '📈', 'VENDAS': '🛒'}
            icone = icones.get(meta['tipo'], '🎯')
            
            ctk.CTkLabel(
                frame_header,
                text=f"{icone} Meta de {meta['tipo']} - {meta['periodo']}",
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(side="left")
            
            # Progresso
            percentual = progresso_data['percentual']
            cor_progresso = '#2ca02c' if percentual >= 100 else '#ff7f0e' if percentual >= 70 else '#d62728'
            
            frame_progresso = ctk.CTkFrame(frame_meta, fg_color="transparent")
            frame_progresso.pack(fill="x", padx=15, pady=(0, 10))
            
            # Barra de progresso
            progress = ctk.CTkProgressBar(frame_progresso, width=400, height=25)
            progress.pack(fill="x", pady=5)
            progress.set(min(percentual / 100, 1.0))
            
            # Textos
            texto_valores = f"{Formatador.formatar_moeda(progresso_data['valor_atual'])} de {Formatador.formatar_moeda(progresso_data['valor_meta'])}"
            ctk.CTkLabel(
                frame_progresso,
                text=texto_valores,
                font=ctk.CTkFont(size=12)
            ).pack()
            
            texto_percentual = f"{percentual:.1f}% atingido"
            if progresso_data['atingido']:
                texto_percentual += " ✅ META ATINGIDA!"
            
            ctk.CTkLabel(
                frame_progresso,
                text=texto_percentual,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=cor_progresso
            ).pack()
            
            # Período
            ctk.CTkLabel(
                frame_progresso,
                text=f"Período: {Formatador.formatar_data(meta['data_inicio'] + ' 00:00:00')} a {Formatador.formatar_data(meta['data_fim'] + ' 00:00:00')}",
                font=ctk.CTkFont(size=10),
                text_color="gray"
            ).pack(pady=(5, 0))
            
            # Botão desativar
            if not progresso_data['atingido']:
                btn_desativar = ctk.CTkButton(
                    frame_meta,
                    text="🗑️ Desativar",
                    command=lambda m=meta['id']: self.desativar_meta(m),
                    fg_color="#d62728",
                    hover_color="#c82333",
                    width=100
                )
                btn_desativar.pack(pady=(0, 10))
    
    def desativar_meta(self, meta_id):
        """Desativa uma meta"""
        if messagebox.askyesno("Confirmar", "Deseja desativar esta meta?"):
            self.db.desativar_meta(meta_id)
            self.atualizar_metas()
