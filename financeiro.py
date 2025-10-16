"""
Tela de Financeiro - Gestão financeira, despesas e relatórios
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from database import Database
from utils import Formatador, Periodo, ExportadorPDF, ExportadorExcel

class Financeiro(ctk.CTkFrame):
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
            text="💰 Gestão Financeira",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titulo.pack(pady=(0, 20))
        
        # Filtros de período
        self.criar_filtros_periodo()
        
        # Cards de resumo financeiro
        self.criar_cards_financeiros()
        
        # Gráficos financeiros
        self.criar_graficos_financeiros()
        
        # Gestão de despesas
        self.criar_gestao_despesas()
        
        # Carregar dados
        self.atualizar_financeiro()
    
    def criar_filtros_periodo(self):
        """Cria filtros de período"""
        frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        frame.pack(fill="x", pady=(0, 20))
        
        label = ctk.CTkLabel(
            frame,
            text="Período:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label.pack(side="left", padx=5)
        
        self.combo_periodo = ctk.CTkComboBox(
            frame,
            values=["Hoje", "Esta Semana", "Este Mês", "Este Ano", "Mês Anterior"],
            command=lambda x: self.atualizar_financeiro(),
            width=200
        )
        self.combo_periodo.set("Este Mês")
        self.combo_periodo.pack(side="left", padx=5)
        
        btn_atualizar = ctk.CTkButton(
            frame,
            text="🔄 Atualizar",
            command=self.atualizar_financeiro,
            width=120
        )
        btn_atualizar.pack(side="left", padx=5)
        
        # Botões de exportação
        btn_pdf = ctk.CTkButton(
            frame,
            text="📄 Exportar PDF",
            command=self.exportar_relatorio_pdf,
            width=150,
            fg_color="#d62728",
            hover_color="#c82333"
        )
        btn_pdf.pack(side="right", padx=5)
        
        btn_excel = ctk.CTkButton(
            frame,
            text="📊 Exportar Excel",
            command=self.exportar_relatorio_excel,
            width=150,
            fg_color="#2ca02c",
            hover_color="#28a745"
        )
        btn_excel.pack(side="right", padx=5)
    
    def criar_cards_financeiros(self):
        """Cria cards com indicadores financeiros"""
        frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        frame.pack(fill="x", pady=(0, 20))
        
        # Receita
        self.card_receita = self.criar_card(
            frame,
            "💵 Receita Total",
            "R$ 0,00",
            "#1f77b4"
        )
        self.card_receita.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Lucro Bruto
        self.card_lucro_bruto = self.criar_card(
            frame,
            "📊 Lucro Bruto",
            "R$ 0,00",
            "#2ca02c"
        )
        self.card_lucro_bruto.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Despesas
        self.card_despesas = self.criar_card(
            frame,
            "💸 Despesas Totais",
            "R$ 0,00",
            "#ff7f0e"
        )
        self.card_despesas.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        # Lucro Líquido
        self.card_lucro_liquido = self.criar_card(
            frame,
            "💰 Lucro Líquido",
            "R$ 0,00",
            "#2ca02c"
        )
        self.card_lucro_liquido.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")
        
        for i in range(4):
            frame.columnconfigure(i, weight=1)
    
    def criar_card(self, parent, titulo, valor, cor):
        """Cria um card financeiro"""
        card = ctk.CTkFrame(parent, corner_radius=10)
        
        label_titulo = ctk.CTkLabel(
            card,
            text=titulo,
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )
        label_titulo.pack(pady=(15, 5))
        
        label_valor = ctk.CTkLabel(
            card,
            text=valor,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=cor
        )
        label_valor.pack(pady=(5, 15))
        
        card.label_valor = label_valor
        return card
    
    def criar_graficos_financeiros(self):
        """Cria área de gráficos financeiros"""
        frame = ctk.CTkFrame(self.scroll_frame)
        frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Gráfico de pizza - Distribuição
        frame_esq = ctk.CTkFrame(frame)
        frame_esq.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
        
        label1 = ctk.CTkLabel(
            frame_esq,
            text="📊 Distribuição Financeira",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        label1.pack(pady=10)
        
        self.figura_pizza = Figure(figsize=(5, 4), dpi=80)
        self.ax_pizza = self.figura_pizza.add_subplot(111)
        self.canvas_pizza = FigureCanvasTkAgg(self.figura_pizza, frame_esq)
        self.canvas_pizza.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        # Gráfico de barras - Lucro mensal
        frame_dir = ctk.CTkFrame(frame)
        frame_dir.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)
        
        label2 = ctk.CTkLabel(
            frame_dir,
            text="📈 Evolução do Lucro",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        label2.pack(pady=10)
        
        self.figura_lucro = Figure(figsize=(5, 4), dpi=80)
        self.ax_lucro = self.figura_lucro.add_subplot(111)
        self.canvas_lucro = FigureCanvasTkAgg(self.figura_lucro, frame_dir)
        self.canvas_lucro.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    def criar_gestao_despesas(self):
        """Cria seção de gestão de despesas"""
        frame_principal = ctk.CTkFrame(self.scroll_frame)
        frame_principal.pack(fill="x", pady=(0, 20))
        
        label_titulo = ctk.CTkLabel(
            frame_principal,
            text="📝 Gestão de Despesas",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        label_titulo.pack(pady=15)
        
        # Container
        container = ctk.CTkFrame(frame_principal, fg_color="transparent")
        container.pack(fill="x", padx=10, pady=(0, 10))
        
        # Formulário de despesa (esquerda)
        frame_form = ctk.CTkFrame(container)
        frame_form.pack(side="left", fill="both", padx=(0, 10), pady=10)
        
        ctk.CTkLabel(
            frame_form,
            text="Nova Despesa",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=10)
        
        # Descrição
        ctk.CTkLabel(frame_form, text="Descrição *", anchor="w").pack(fill="x", padx=10)
        self.entry_desc_despesa = ctk.CTkEntry(
            frame_form,
            placeholder_text="Ex: Frete, Taxa, Marketing..."
        )
        self.entry_desc_despesa.pack(fill="x", padx=10, pady=(5, 10))
        
        # Valor
        ctk.CTkLabel(frame_form, text="Valor *", anchor="w").pack(fill="x", padx=10)
        self.entry_valor_despesa = ctk.CTkEntry(
            frame_form,
            placeholder_text="0,00"
        )
        self.entry_valor_despesa.pack(fill="x", padx=10, pady=(5, 10))
        
        # Categoria
        ctk.CTkLabel(frame_form, text="Categoria", anchor="w").pack(fill="x", padx=10)
        self.combo_cat_despesa = ctk.CTkComboBox(
            frame_form,
            values=["Frete", "Taxas", "Marketing", "Aluguel", "Salários", "Outros"]
        )
        self.combo_cat_despesa.pack(fill="x", padx=10, pady=(5, 10))
        
        # Data
        ctk.CTkLabel(frame_form, text="Data (AAAA-MM-DD)", anchor="w").pack(fill="x", padx=10)
        self.entry_data_despesa = ctk.CTkEntry(
            frame_form,
            placeholder_text=datetime.now().strftime("%Y-%m-%d")
        )
        self.entry_data_despesa.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_data_despesa.pack(fill="x", padx=10, pady=(5, 10))
        
        # Observações
        ctk.CTkLabel(frame_form, text="Observações", anchor="w").pack(fill="x", padx=10)
        self.text_obs_despesa = ctk.CTkTextbox(frame_form, height=60)
        self.text_obs_despesa.pack(fill="x", padx=10, pady=(5, 10))
        
        # Botões
        frame_btns = ctk.CTkFrame(frame_form, fg_color="transparent")
        frame_btns.pack(fill="x", padx=10, pady=(10, 15))
        
        btn_add = ctk.CTkButton(
            frame_btns,
            text="➕ Adicionar",
            command=self.adicionar_despesa,
            fg_color="#2ca02c",
            hover_color="#28a745"
        )
        btn_add.pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        btn_limpar = ctk.CTkButton(
            frame_btns,
            text="🔄 Limpar",
            command=self.limpar_form_despesa,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        btn_limpar.pack(side="right", expand=True, fill="x", padx=(5, 0))
        
        # Lista de despesas (direita)
        frame_lista = ctk.CTkFrame(container)
        frame_lista.pack(side="right", fill="both", expand=True, padx=(10, 0), pady=10)
        
        ctk.CTkLabel(
            frame_lista,
            text="Despesas Registradas",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=10)
        
        # Scroll para despesas
        self.scroll_despesas = ctk.CTkScrollableFrame(frame_lista, height=300)
        self.scroll_despesas.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Cabeçalho
        self.criar_cabecalho_despesas()
    
    def criar_cabecalho_despesas(self):
        """Cria cabeçalho da lista de despesas"""
        frame = ctk.CTkFrame(self.scroll_despesas, fg_color="#ff7f0e")
        frame.pack(fill="x", pady=(0, 5))
        
        headers = [
            ("Data", 100),
            ("Descrição", 180),
            ("Categoria", 100),
            ("Valor", 100),
            ("Ações", 80)
        ]
        
        for texto, largura in headers:
            label = ctk.CTkLabel(
                frame,
                text=texto,
                font=ctk.CTkFont(size=11, weight="bold"),
                width=largura
            )
            label.pack(side="left", padx=5, pady=5)
    
    def get_periodo_datas(self):
        """Retorna datas baseado no período"""
        periodo = self.combo_periodo.get()
        
        if periodo == "Hoje":
            return Periodo.hoje(), Periodo.hoje()
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
    
    def atualizar_financeiro(self):
        """Atualiza todos os dados financeiros"""
        data_inicio, data_fim = self.get_periodo_datas()
        
        # Atualizar cards
        self.atualizar_cards_financeiros(data_inicio, data_fim)
        
        # Atualizar gráficos
        self.atualizar_grafico_pizza(data_inicio, data_fim)
        self.atualizar_grafico_lucro(data_inicio, data_fim)
        
        # Atualizar lista de despesas
        self.carregar_despesas(data_inicio, data_fim)
    
    def atualizar_cards_financeiros(self, data_inicio, data_fim):
        """Atualiza cards financeiros"""
        # Resumo de vendas
        resumo = self.db.get_resumo_vendas(data_inicio, data_fim)
        self.card_receita.label_valor.configure(
            text=Formatador.formatar_moeda(resumo['receita_total'])
        )
        
        # Lucro
        lucro_data = self.db.get_lucro_periodo(data_inicio, data_fim)
        self.card_lucro_bruto.label_valor.configure(
            text=Formatador.formatar_moeda(lucro_data['lucro_bruto'])
        )
        self.card_despesas.label_valor.configure(
            text=Formatador.formatar_moeda(lucro_data['despesas'])
        )
        self.card_lucro_liquido.label_valor.configure(
            text=Formatador.formatar_moeda(lucro_data['lucro_liquido'])
        )
        
        # Colorir lucro líquido
        if lucro_data['lucro_liquido'] < 0:
            self.card_lucro_liquido.label_valor.configure(text_color="#d62728")
        else:
            self.card_lucro_liquido.label_valor.configure(text_color="#2ca02c")
    
    def atualizar_grafico_pizza(self, data_inicio, data_fim):
        """Atualiza gráfico de pizza"""
        self.ax_pizza.clear()
        
        lucro_data = self.db.get_lucro_periodo(data_inicio, data_fim)
        
        valores = []
        labels = []
        cores = []
        
        if lucro_data['lucro_bruto'] > 0:
            valores.append(lucro_data['lucro_bruto'])
            labels.append('Lucro')
            cores.append('#2ca02c')
        
        if lucro_data['despesas'] > 0:
            valores.append(lucro_data['despesas'])
            labels.append('Despesas')
            cores.append('#ff7f0e')
        
        if valores:
            self.ax_pizza.pie(
                valores,
                labels=labels,
                autopct='%1.1f%%',
                colors=cores,
                startangle=90
            )
            self.ax_pizza.axis('equal')
        else:
            self.ax_pizza.text(
                0.5, 0.5, 'Sem dados no período',
                ha='center', va='center', fontsize=12
            )
        
        self.figura_pizza.tight_layout()
        self.canvas_pizza.draw()
    
    def atualizar_grafico_lucro(self, data_inicio, data_fim):
        """Atualiza gráfico de evolução do lucro"""
        self.ax_lucro.clear()
        
        # Buscar vendas por data
        vendas = self.db.listar_vendas(data_inicio, data_fim)
        despesas = self.db.listar_despesas(data_inicio, data_fim)
        
        if vendas or despesas:
            # Agrupar por data
            lucro_por_data = {}
            
            # Processar vendas
            for venda in vendas:
                data = venda['data_venda'][:10]
                produto = self.db.buscar_produto(venda['produto_id'])
                if produto:
                    lucro = (venda['preco_unitario'] - produto['preco_custo']) * venda['quantidade']
                    lucro_por_data[data] = lucro_por_data.get(data, 0) + lucro
            
            # Subtrair despesas
            for despesa in despesas:
                data = despesa['data_despesa']
                lucro_por_data[data] = lucro_por_data.get(data, 0) - despesa['valor']
            
            if lucro_por_data:
                datas = sorted(lucro_por_data.keys())
                valores = [lucro_por_data[data] for data in datas]
                
                # Formatar datas
                datas_formatadas = [Formatador.formatar_data(data + " 00:00:00") for data in datas]
                
                # Cores baseadas em positivo/negativo
                cores = ['#2ca02c' if v >= 0 else '#d62728' for v in valores]
                
                self.ax_lucro.bar(datas_formatadas, valores, color=cores, alpha=0.7)
                self.ax_lucro.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
                self.ax_lucro.set_xlabel('Data', fontsize=10)
                self.ax_lucro.set_ylabel('Lucro (R$)', fontsize=10)
                self.ax_lucro.tick_params(axis='x', rotation=45, labelsize=8)
                self.ax_lucro.tick_params(axis='y', labelsize=8)
                self.ax_lucro.grid(True, alpha=0.3, axis='y')
        else:
            self.ax_lucro.text(
                0.5, 0.5, 'Sem dados no período',
                ha='center', va='center', fontsize=12
            )
        
        self.figura_lucro.tight_layout()
        self.canvas_lucro.draw()
    
    def adicionar_despesa(self):
        """Adiciona uma nova despesa"""
        # Validações
        descricao = self.entry_desc_despesa.get().strip()
        if not descricao:
            messagebox.showwarning("Atenção", "Preencha a descrição!")
            return
        
        try:
            valor = float(self.entry_valor_despesa.get().replace(",", "."))
            if valor <= 0:
                raise ValueError()
        except:
            messagebox.showwarning("Atenção", "Informe um valor válido!")
            return
        
        data = self.entry_data_despesa.get().strip()
        if not data:
            data = datetime.now().strftime("%Y-%m-%d")
        
        try:
            self.db.adicionar_despesa(
                descricao=descricao,
                valor=valor,
                categoria=self.combo_cat_despesa.get(),
                data_despesa=data,
                observacoes=self.text_obs_despesa.get("1.0", "end").strip()
            )
            
            messagebox.showinfo("Sucesso", "Despesa registrada com sucesso!")
            self.limpar_form_despesa()
            self.atualizar_financeiro()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao registrar despesa: {str(e)}")
    
    def limpar_form_despesa(self):
        """Limpa formulário de despesa"""
        self.entry_desc_despesa.delete(0, "end")
        self.entry_valor_despesa.delete(0, "end")
        self.combo_cat_despesa.set("Outros")
        self.entry_data_despesa.delete(0, "end")
        self.entry_data_despesa.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.text_obs_despesa.delete("1.0", "end")
    
    def carregar_despesas(self, data_inicio, data_fim):
        """Carrega lista de despesas"""
        # Limpar lista
        for widget in self.scroll_despesas.winfo_children():
            if widget != self.scroll_despesas.winfo_children()[0]:
                widget.destroy()
        
        despesas = self.db.listar_despesas(data_inicio, data_fim)
        
        for despesa in despesas:
            self.criar_item_despesa(despesa)
    
    def criar_item_despesa(self, despesa):
        """Cria item de despesa na lista"""
        frame = ctk.CTkFrame(self.scroll_despesas)
        frame.pack(fill="x", pady=2)
        
        # Data
        data_formatada = Formatador.formatar_data(despesa['data_despesa'] + " 00:00:00")
        ctk.CTkLabel(frame, text=data_formatada, width=100).pack(side="left", padx=5)
        
        # Descrição
        desc_texto = despesa['descricao'][:25] + "..." if len(despesa['descricao']) > 25 else despesa['descricao']
        ctk.CTkLabel(frame, text=desc_texto, width=180, anchor="w").pack(side="left", padx=5)
        
        # Categoria
        ctk.CTkLabel(frame, text=despesa['categoria'], width=100).pack(side="left", padx=5)
        
        # Valor
        ctk.CTkLabel(
            frame,
            text=Formatador.formatar_moeda(despesa['valor']),
            width=100,
            text_color="#d62728",
            font=ctk.CTkFont(weight="bold")
        ).pack(side="left", padx=5)
        
        # Botão excluir
        btn_excluir = ctk.CTkButton(
            frame,
            text="🗑️",
            width=80,
            fg_color="#d62728",
            hover_color="#c82333",
            command=lambda: self.excluir_despesa(despesa['id'])
        )
        btn_excluir.pack(side="left", padx=5)
    
    def excluir_despesa(self, despesa_id):
        """Exclui uma despesa"""
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir esta despesa?"):
            try:
                self.db.remover_despesa(despesa_id)
                messagebox.showinfo("Sucesso", "Despesa removida com sucesso!")
                self.atualizar_financeiro()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover despesa: {str(e)}")
    
    def exportar_relatorio_pdf(self):
        """Exporta relatório financeiro em PDF"""
        data_inicio, data_fim = self.get_periodo_datas()
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            initialfile=f"relatorio_financeiro_{datetime.now().strftime('%Y%m%d')}.pdf"
        )
        
        if filename:
            try:
                resumo = self.db.get_resumo_vendas(data_inicio, data_fim)
                lucro_data = self.db.get_lucro_periodo(data_inicio, data_fim)
                
                dados = {
                    'receita_total': resumo['receita_total'],
                    'lucro_bruto': lucro_data['lucro_bruto'],
                    'despesas': lucro_data['despesas'],
                    'lucro_liquido': lucro_data['lucro_liquido']
                }
                
                periodo_texto = self.combo_periodo.get()
                ExportadorPDF.gerar_relatorio_financeiro(dados, filename, periodo_texto)
                messagebox.showinfo("Sucesso", f"Relatório exportado para:\n{filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")
    
    def exportar_relatorio_excel(self):
        """Exporta relatório financeiro em Excel"""
        data_inicio, data_fim = self.get_periodo_datas()
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")],
            initialfile=f"relatorio_financeiro_{datetime.now().strftime('%Y%m%d')}.xlsx"
        )
        
        if filename:
            try:
                vendas = self.db.listar_vendas(data_inicio, data_fim)
                despesas = self.db.listar_despesas(data_inicio, data_fim)
                produtos = self.db.listar_produtos()
                
                resumo = self.db.get_resumo_vendas(data_inicio, data_fim)
                lucro_data = self.db.get_lucro_periodo(data_inicio, data_fim)
                
                dados = {
                    'vendas': vendas,
                    'despesas': despesas,
                    'produtos': produtos,
                    'resumo': {
                        'receita_total': resumo['receita_total'],
                        'lucro_bruto': lucro_data['lucro_bruto'],
                        'despesas_total': lucro_data['despesas'],
                        'lucro_liquido': lucro_data['lucro_liquido']
                    }
                }
                
                ExportadorExcel.gerar_relatorio_completo(dados, filename)
                messagebox.showinfo("Sucesso", f"Relatório exportado para:\n{filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")
