"""
DGTECH GESTÃO - Sistema de Administração de Vendas
Aplicação Principal com Interface Moderna
"""

import customtkinter as ctk
from database import Database
from dashboard import Dashboard
from produtos import Produtos
from vendas import Vendas
from financeiro import Financeiro
from configuracoes import Configuracoes
from relatorios import RelatoriosAvancados
import sys

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configurações da janela
        self.title("DGTECH GESTÃO - Sistema de Vendas")
        self.geometry("1400x900")
        
        # Definir ícone (se disponível)
        try:
            self.iconbitmap("icon.ico")
        except:
            pass
        
        # Inicializar banco de dados
        self.db = Database()
        
        # Carregar configurações
        self.carregar_configuracoes()
        
        # Configurar grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Criar navegação lateral
        self.criar_menu_lateral()
        
        # Criar área de conteúdo
        self.criar_area_conteudo()
        
        # Mostrar dashboard inicial
        self.mostrar_dashboard()
        
        # Executar otimizações ao iniciar
        try:
            self.db.criar_indices()
        except:
            pass  # Índices já podem existir
    
    def carregar_configuracoes(self):
        """Carrega configurações do sistema"""
        tema = self.db.get_config('tema')
        if tema:
            ctk.set_appearance_mode(tema)
        else:
            ctk.set_appearance_mode("dark")
        
        # Tema de cor padrão
        ctk.set_default_color_theme("blue")
    
    def criar_menu_lateral(self):
        """Cria menu de navegação lateral"""
        self.frame_nav = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.frame_nav.grid(row=0, column=0, sticky="nsew")
        self.frame_nav.grid_rowconfigure(8, weight=1)
        
        # Logo/Título
        logo_frame = ctk.CTkFrame(self.frame_nav, fg_color="transparent")
        logo_frame.grid(row=0, column=0, padx=20, pady=30)
        
        label_logo = ctk.CTkLabel(
            logo_frame,
            text="🏢 DGTECH",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        label_logo.pack()
        
        label_subtitle = ctk.CTkLabel(
            logo_frame,
            text="Sistema de Gestão",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        label_subtitle.pack()
        
        # Botões de navegação
        self.btn_dashboard = self.criar_botao_nav(
            "📊 Dashboard",
            self.mostrar_dashboard,
            row=1
        )
        
        self.btn_produtos = self.criar_botao_nav(
            "📦 Produtos",
            self.mostrar_produtos,
            row=2
        )
        
        self.btn_vendas = self.criar_botao_nav(
            "🛒 Vendas",
            self.mostrar_vendas,
            row=3
        )
        
        self.btn_financeiro = self.criar_botao_nav(
            "💰 Financeiro",
            self.mostrar_financeiro,
            row=4
        )
        
        self.btn_relatorios = self.criar_botao_nav(
            "📊 Relatórios",
            self.mostrar_relatorios,
            row=5
        )
        
        self.btn_config = self.criar_botao_nav(
            "⚙️ Configurações",
            self.mostrar_configuracoes,
            row=6
        )
        
        # Botão sair (no final)
        btn_sair = ctk.CTkButton(
            self.frame_nav,
            text="🚪 Sair",
            command=self.sair,
            fg_color="#d62728",
            hover_color="#c82333",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        btn_sair.grid(row=9, column=0, padx=20, pady=20, sticky="ew")
        
        # Informação da versão
        label_versao = ctk.CTkLabel(
            self.frame_nav,
            text="v1.0.0",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        label_versao.grid(row=10, column=0, pady=(0, 10))
    
    def criar_botao_nav(self, texto, comando, row):
        """Cria um botão de navegação"""
        btn = ctk.CTkButton(
            self.frame_nav,
            text=texto,
            command=comando,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            height=50,
            anchor="w",
            font=ctk.CTkFont(size=14)
        )
        btn.grid(row=row, column=0, padx=20, pady=5, sticky="ew")
        return btn
    
    def destacar_botao(self, botao_ativo):
        """Destaca o botão ativo"""
        # Resetar todos os botões
        botoes = [
            self.btn_dashboard,
            self.btn_produtos,
            self.btn_vendas,
            self.btn_financeiro,
            self.btn_relatorios,
            self.btn_config
        ]
        
        for btn in botoes:
            btn.configure(fg_color="transparent")
        
        # Destacar botão ativo
        botao_ativo.configure(fg_color=("gray75", "gray25"))
    
    def criar_area_conteudo(self):
        """Cria área principal de conteúdo"""
        self.frame_conteudo = ctk.CTkFrame(self, corner_radius=0)
        self.frame_conteudo.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.frame_conteudo.grid_rowconfigure(0, weight=1)
        self.frame_conteudo.grid_columnconfigure(0, weight=1)
    
    def limpar_conteudo(self):
        """Limpa a área de conteúdo"""
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()
    
    def mostrar_dashboard(self):
        """Mostra a tela de Dashboard"""
        self.limpar_conteudo()
        self.destacar_botao(self.btn_dashboard)
        
        dashboard = Dashboard(self.frame_conteudo, self.db)
        dashboard.grid(row=0, column=0, sticky="nsew")
    
    def mostrar_produtos(self):
        """Mostra a tela de Produtos"""
        self.limpar_conteudo()
        self.destacar_botao(self.btn_produtos)
        
        produtos = Produtos(self.frame_conteudo, self.db)
        produtos.grid(row=0, column=0, sticky="nsew")
    
    def mostrar_vendas(self):
        """Mostra a tela de Vendas"""
        self.limpar_conteudo()
        self.destacar_botao(self.btn_vendas)
        
        vendas = Vendas(self.frame_conteudo, self.db)
        vendas.grid(row=0, column=0, sticky="nsew")
    
    def mostrar_financeiro(self):
        """Mostra a tela Financeiro"""
        self.limpar_conteudo()
        self.destacar_botao(self.btn_financeiro)
        
        financeiro = Financeiro(self.frame_conteudo, self.db)
        financeiro.grid(row=0, column=0, sticky="nsew")
    
    def mostrar_relatorios(self):
        """Mostra a tela de Relatórios Avançados"""
        self.limpar_conteudo()
        self.destacar_botao(self.btn_relatorios)
        
        relatorios = RelatoriosAvancados(self.frame_conteudo, self.db)
        relatorios.grid(row=0, column=0, sticky="nsew")
    
    def mostrar_configuracoes(self):
        """Mostra a tela de Configurações"""
        self.limpar_conteudo()
        self.destacar_botao(self.btn_config)
        
        config = Configuracoes(self.frame_conteudo, self.db, self.config_callback)
        config.grid(row=0, column=0, sticky="nsew")
    
    def config_callback(self, evento, dados):
        """Callback para eventos de configuração"""
        if evento == 'tema_alterado':
            # Tema já foi alterado nas configurações
            pass
    
    def sair(self):
        """Fecha a aplicação"""
        if ctk.CTkMessagebox is not None:
            resposta = ctk.CTkMessagebox(
                title="Confirmar Saída",
                message="Deseja realmente sair do sistema?",
                icon="question",
                option_1="Cancelar",
                option_2="Sair"
            )
            if resposta.get() == "Sair":
                self.quit()
                self.destroy()
        else:
            # Fallback se CTkMessagebox não estiver disponível
            from tkinter import messagebox
            if messagebox.askyesno("Confirmar", "Deseja realmente sair?"):
                self.quit()
                self.destroy()

def main():
    """Função principal"""
    try:
        app = App()
        app.mainloop()
    except KeyboardInterrupt:
        print("\nSistema encerrado pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"Erro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
