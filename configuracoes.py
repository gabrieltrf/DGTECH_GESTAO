"""
Tela de Configurações - Tema e preferências do sistema
"""

import customtkinter as ctk
from tkinter import messagebox
from database import Database

class Configuracoes(ctk.CTkFrame):
    def __init__(self, parent, db: Database, app_callback=None):
        super().__init__(parent)
        self.db = db
        self.app_callback = app_callback
        self.configure(fg_color="transparent")
        
        # Container principal
        container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        titulo = ctk.CTkLabel(
            container,
            text="⚙️ Configurações",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titulo.pack(pady=(0, 30))
        
        # Seção de Aparência
        self.criar_secao_aparencia(container)
        
        # Seção de Estoque
        self.criar_secao_estoque(container)
        
        # Seção de Preços
        self.criar_secao_precos(container)
        
        # Seção de Informações
        self.criar_secao_info(container)
        
        # Botão salvar
        btn_salvar = ctk.CTkButton(
            container,
            text="💾 Salvar Configurações",
            command=self.salvar_configuracoes,
            fg_color="#2ca02c",
            hover_color="#28a745",
            height=45,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        btn_salvar.pack(pady=30, padx=100, fill="x")
        
        # Carregar configurações atuais
        self.carregar_configuracoes()
    
    def criar_secao_aparencia(self, parent):
        """Cria seção de aparência"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=(0, 20), padx=20)
        
        label_titulo = ctk.CTkLabel(
            frame,
            text="🎨 Aparência",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        label_titulo.pack(pady=15, anchor="w", padx=15)
        
        # Tema
        frame_tema = ctk.CTkFrame(frame, fg_color="transparent")
        frame_tema.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(
            frame_tema,
            text="Tema do Sistema:",
            font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=(0, 15))
        
        self.var_tema = ctk.StringVar(value="dark")
        
        radio_dark = ctk.CTkRadioButton(
            frame_tema,
            text="🌙 Escuro",
            variable=self.var_tema,
            value="dark",
            command=self.mudar_tema
        )
        radio_dark.pack(side="left", padx=10)
        
        radio_light = ctk.CTkRadioButton(
            frame_tema,
            text="☀️ Claro",
            variable=self.var_tema,
            value="light",
            command=self.mudar_tema
        )
        radio_light.pack(side="left", padx=10)
        
        # Escala de UI
        frame_escala = ctk.CTkFrame(frame, fg_color="transparent")
        frame_escala.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(
            frame_escala,
            text="Escala da Interface:",
            font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=(0, 15))
        
        self.slider_escala = ctk.CTkSlider(
            frame_escala,
            from_=0.8,
            to=1.2,
            number_of_steps=8,
            command=self.atualizar_escala_label
        )
        self.slider_escala.set(1.0)
        self.slider_escala.pack(side="left", padx=10, fill="x", expand=True)
        
        self.label_escala = ctk.CTkLabel(
            frame_escala,
            text="100%",
            width=60
        )
        self.label_escala.pack(side="left", padx=5)
    
    def criar_secao_estoque(self, parent):
        """Cria seção de estoque"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=(0, 20), padx=20)
        
        label_titulo = ctk.CTkLabel(
            frame,
            text="📦 Gestão de Estoque",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        label_titulo.pack(pady=15, anchor="w", padx=15)
        
        # Alerta de estoque
        frame_alerta = ctk.CTkFrame(frame, fg_color="transparent")
        frame_alerta.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(
            frame_alerta,
            text="Quantidade mínima para alerta de estoque baixo:",
            font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=(0, 15))
        
        self.entry_estoque_alerta = ctk.CTkEntry(
            frame_alerta,
            width=100,
            placeholder_text="10"
        )
        self.entry_estoque_alerta.pack(side="left", padx=5)
        
        ctk.CTkLabel(
            frame_alerta,
            text="unidades",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(side="left", padx=5)
    
    def criar_secao_precos(self, parent):
        """Cria seção de preços"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=(0, 20), padx=20)
        
        label_titulo = ctk.CTkLabel(
            frame,
            text="💰 Gestão de Preços",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        label_titulo.pack(pady=15, anchor="w", padx=15)
        
        # Margem padrão
        frame_margem = ctk.CTkFrame(frame, fg_color="transparent")
        frame_margem.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(
            frame_margem,
            text="Margem de lucro padrão para novos produtos:",
            font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=(0, 15))
        
        self.entry_margem_padrao = ctk.CTkEntry(
            frame_margem,
            width=100,
            placeholder_text="30"
        )
        self.entry_margem_padrao.pack(side="left", padx=5)
        
        ctk.CTkLabel(
            frame_margem,
            text="%",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(side="left", padx=5)
    
    def criar_secao_info(self, parent):
        """Cria seção de informações"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=(0, 20), padx=20)
        
        label_titulo = ctk.CTkLabel(
            frame,
            text="ℹ️ Informações do Sistema",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        label_titulo.pack(pady=15, anchor="w", padx=15)
        
        info_frame = ctk.CTkFrame(frame, fg_color="#e8f4f8")
        info_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        infos = [
            ("📊 Sistema:", "DGTECH GESTÃO - Sistema de Gestão de Vendas"),
            ("🔢 Versão:", "1.0.0"),
            ("👨‍💻 Desenvolvido por:", "DGTECH"),
            ("📅 Ano:", "2025"),
            ("🐍 Python:", "3.x"),
            ("🖼️ Interface:", "CustomTkinter"),
            ("💾 Banco de Dados:", "SQLite")
        ]
        
        for label, valor in infos:
            frame_info = ctk.CTkFrame(info_frame, fg_color="transparent")
            frame_info.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(
                frame_info,
                text=label,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=150,
                anchor="w"
            ).pack(side="left", padx=5)
            
            ctk.CTkLabel(
                frame_info,
                text=valor,
                font=ctk.CTkFont(size=12),
                anchor="w"
            ).pack(side="left", padx=5)
        
        # Estatísticas do banco
        self.criar_estatisticas(frame)
    
    def criar_estatisticas(self, parent):
        """Cria área de estatísticas do sistema"""
        frame_stats = ctk.CTkFrame(parent, fg_color="#d4edda")
        frame_stats.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(
            frame_stats,
            text="📈 Estatísticas",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5), padx=10, anchor="w")
        
        # Buscar dados
        produtos = self.db.listar_produtos()
        vendas = self.db.listar_vendas()
        categorias = self.db.listar_categorias()
        
        stats = [
            ("Total de Produtos:", str(len(produtos))),
            ("Total de Categorias:", str(len(categorias))),
            ("Total de Vendas:", str(len(vendas))),
            ("Produtos com Estoque Baixo:", str(len(self.db.produtos_estoque_baixo())))
        ]
        
        for label, valor in stats:
            frame_stat = ctk.CTkFrame(frame_stats, fg_color="transparent")
            frame_stat.pack(fill="x", padx=10, pady=2)
            
            ctk.CTkLabel(
                frame_stat,
                text=label,
                font=ctk.CTkFont(size=11),
                width=200,
                anchor="w"
            ).pack(side="left", padx=5)
            
            ctk.CTkLabel(
                frame_stat,
                text=valor,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#2ca02c",
                anchor="e"
            ).pack(side="right", padx=5)
        
        frame_stats.pack(pady=(0, 10))
    
    def carregar_configuracoes(self):
        """Carrega configurações salvas"""
        # Tema
        tema = self.db.get_config('tema')
        if tema:
            self.var_tema.set(tema)
        
        # Alerta de estoque
        estoque_alerta = self.db.get_config('estoque_alerta')
        if estoque_alerta:
            self.entry_estoque_alerta.delete(0, "end")
            self.entry_estoque_alerta.insert(0, estoque_alerta)
        
        # Margem padrão
        margem = self.db.get_config('margem_padrao')
        if margem:
            self.entry_margem_padrao.delete(0, "end")
            self.entry_margem_padrao.insert(0, margem)
    
    def mudar_tema(self):
        """Muda o tema da aplicação"""
        tema = self.var_tema.get()
        ctk.set_appearance_mode(tema)
        
        # Se houver callback para atualizar app principal
        if self.app_callback:
            self.app_callback('tema_alterado', tema)
    
    def atualizar_escala_label(self, valor):
        """Atualiza label da escala"""
        percentual = int(valor * 100)
        self.label_escala.configure(text=f"{percentual}%")
    
    def salvar_configuracoes(self):
        """Salva todas as configurações"""
        try:
            # Salvar tema
            self.db.set_config('tema', self.var_tema.get())
            
            # Salvar alerta de estoque
            estoque_alerta = self.entry_estoque_alerta.get().strip()
            if estoque_alerta and estoque_alerta.isdigit():
                self.db.set_config('estoque_alerta', estoque_alerta)
            
            # Salvar margem padrão
            margem = self.entry_margem_padrao.get().strip()
            if margem and margem.replace('.', '').replace(',', '').isdigit():
                self.db.set_config('margem_padrao', margem)
            
            # Salvar escala (para futura implementação)
            escala = str(self.slider_escala.get())
            self.db.set_config('escala_ui', escala)
            
            messagebox.showinfo(
                "Sucesso",
                "Configurações salvas com sucesso!\n\nAlgumas alterações podem exigir reiniciar o sistema."
            )
            
            # Aplicar tema
            self.mudar_tema()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {str(e)}")
