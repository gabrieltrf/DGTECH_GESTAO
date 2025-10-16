"""
Tela de Histórico de Preços com Gráficos
"""

import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from database import Database
from utils import Formatador
from tkinter import messagebox

class HistoricoPrecos(ctk.CTkToplevel):
    def __init__(self, parent, db: Database, produto_id: int):
        super().__init__(parent)
        
        self.db = db
        self.produto_id = produto_id
        
        # Configurar janela
        self.title("📈 Histórico de Preços")
        self.geometry("900x700")
        
        # Buscar produto
        self.produto = db.buscar_produto(produto_id)
        if not self.produto:
            messagebox.showerror("Erro", "Produto não encontrado!")
            self.destroy()
            return
        
        # Criar interface
        self.criar_interface()
        
        # Carregar dados
        self.carregar_historico()
    
    def criar_interface(self):
        """Cria interface da janela"""
        # Cabeçalho
        frame_header = ctk.CTkFrame(self, fg_color="#1f77b4", corner_radius=0)
        frame_header.pack(fill="x")
        
        ctk.CTkLabel(
            frame_header,
            text=f"📦 {self.produto['nome']}",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        ).pack(pady=15)
        
        # Informações atuais
        frame_info = ctk.CTkFrame(self)
        frame_info.pack(fill="x", padx=20, pady=20)
        
        info_text = f"""
        💰 Preço de Custo Atual: {Formatador.formatar_moeda(self.produto['preco_custo'])}
        💵 Preço de Venda Atual: {Formatador.formatar_moeda(self.produto['preco_venda'])}
        📊 Margem Atual: {Formatador.formatar_porcentagem(Formatador.calcular_margem(self.produto['preco_venda'], self.produto['preco_custo']))}
        """
        
        ctk.CTkLabel(
            frame_info,
            text=info_text,
            font=ctk.CTkFont(size=13),
            justify="left"
        ).pack(pady=10, padx=10)
        
        # Abas
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.tab_grafico = self.tabview.add("📈 Gráfico")
        self.tab_tabela = self.tabview.add("📋 Tabela")
        
        # Frame para gráfico
        self.frame_grafico = ctk.CTkFrame(self.tab_grafico)
        self.frame_grafico.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame para tabela
        self.scroll_tabela = ctk.CTkScrollableFrame(self.tab_tabela)
        self.scroll_tabela.pack(fill="both", expand=True, padx=10, pady=10)
    
    def carregar_historico(self):
        """Carrega histórico de preços"""
        historico = self.db.obter_historico_precos(self.produto_id)
        
        if not historico:
            ctk.CTkLabel(
                self.frame_grafico,
                text="Sem histórico de alterações de preços",
                font=ctk.CTkFont(size=14)
            ).pack(pady=50)
            
            ctk.CTkLabel(
                self.scroll_tabela,
                text="Sem histórico de alterações de preços",
                font=ctk.CTkFont(size=14)
            ).pack(pady=50)
            return
        
        # Criar gráfico
        self.criar_grafico(historico)
        
        # Criar tabela
        self.criar_tabela(historico)
    
    def criar_grafico(self, historico):
        """Cria gráfico de evolução de preços"""
        fig = Figure(figsize=(8, 5), dpi=80)
        ax = fig.add_subplot(111)
        
        # Preparar dados
        datas = [h['data_alteracao'][:10] for h in historico]
        custos = [h['preco_custo'] for h in historico]
        vendas = [h['preco_venda'] for h in historico]
        
        # Adicionar ponto atual
        datas.append(datetime.now().strftime("%Y-%m-%d"))
        custos.append(self.produto['preco_custo'])
        vendas.append(self.produto['preco_venda'])
        
        # Formatar datas
        datas_formatadas = [Formatador.formatar_data(d + " 00:00:00") for d in datas]
        
        # Plotar linhas
        ax.plot(datas_formatadas, custos, marker='o', linewidth=2, 
                label='Preço de Custo', color='#d62728', markersize=8)
        ax.plot(datas_formatadas, vendas, marker='s', linewidth=2, 
                label='Preço de Venda', color='#2ca02c', markersize=8)
        
        # Preencher área entre as linhas (margem)
        ax.fill_between(range(len(vendas)), custos, vendas, 
                        alpha=0.2, color='#2ca02c', label='Margem')
        
        ax.set_title('Evolução de Preços ao Longo do Tempo', 
                     fontsize=14, weight='bold', pad=20)
        ax.set_xlabel('Data', fontsize=11)
        ax.set_ylabel('Preço (R$)', fontsize=11)
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.tick_params(axis='x', rotation=45, labelsize=9)
        
        fig.tight_layout()
        
        # Adicionar ao frame
        canvas = FigureCanvasTkAgg(fig, self.frame_grafico)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()
    
    def criar_tabela(self, historico):
        """Cria tabela com histórico"""
        # Cabeçalho
        frame_header = ctk.CTkFrame(self.scroll_tabela, fg_color="#1f77b4")
        frame_header.pack(fill="x", pady=(0, 10))
        
        headers = ["Data", "Preço Custo", "Preço Venda", "Margem", "Variação"]
        for h in headers:
            ctk.CTkLabel(
                frame_header,
                text=h,
                font=ctk.CTkFont(size=11, weight="bold"),
                width=150
            ).pack(side="left", padx=5, pady=5)
        
        # Adicionar item atual
        historico_completo = historico + [{
            'data_alteracao': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'preco_custo': self.produto['preco_custo'],
            'preco_venda': self.produto['preco_venda']
        }]
        
        # Items
        for i, item in enumerate(historico_completo):
            frame_item = ctk.CTkFrame(self.scroll_tabela)
            frame_item.pack(fill="x", pady=2)
            
            # Data
            data_fmt = Formatador.formatar_data_hora(item['data_alteracao'])
            ctk.CTkLabel(frame_item, text=data_fmt, width=150).pack(side="left", padx=5)
            
            # Preço Custo
            ctk.CTkLabel(
                frame_item,
                text=Formatador.formatar_moeda(item['preco_custo']),
                width=150,
                text_color="#d62728"
            ).pack(side="left", padx=5)
            
            # Preço Venda
            ctk.CTkLabel(
                frame_item,
                text=Formatador.formatar_moeda(item['preco_venda']),
                width=150,
                text_color="#2ca02c"
            ).pack(side="left", padx=5)
            
            # Margem
            margem = Formatador.calcular_margem(item['preco_venda'], item['preco_custo'])
            ctk.CTkLabel(
                frame_item,
                text=Formatador.formatar_porcentagem(margem),
                width=150
            ).pack(side="left", padx=5)
            
            # Variação (comparado com anterior)
            if i > 0:
                variacao_custo = ((item['preco_custo'] - historico_completo[i-1]['preco_custo']) / 
                                 historico_completo[i-1]['preco_custo'] * 100)
                variacao_venda = ((item['preco_venda'] - historico_completo[i-1]['preco_venda']) / 
                                 historico_completo[i-1]['preco_venda'] * 100)
                
                texto_var = f"C: {variacao_custo:+.1f}% | V: {variacao_venda:+.1f}%"
                cor_var = "#2ca02c" if variacao_venda > 0 else "#d62728"
            else:
                texto_var = "Primeiro registro"
                cor_var = "gray"
            
            ctk.CTkLabel(
                frame_item,
                text=texto_var,
                width=150,
                text_color=cor_var,
                font=ctk.CTkFont(size=10)
            ).pack(side="left", padx=5)
