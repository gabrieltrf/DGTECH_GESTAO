# 🌐 DGTECH GESTÃO - Versão Web
# Aplicação principal com Streamlit

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from database import Database
from utils import Formatador, Periodo

# Configuração da página
st.set_page_config(
    page_title="DGTECH GESTÃO",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/gabrieltrf/DGTECH_GESTAO',
        'Report a bug': "https://github.com/gabrieltrf/DGTECH_GESTAO/issues",
        'About': "# DGTECH GESTÃO v2.0\nSistema completo de gestão de vendas"
    }
)

# Funções com cache para otimização
@st.cache_data(ttl=60)  # Cache de 60 segundos
def get_produtos_cached():
    """Retorna lista de produtos com cache"""
    db = Database()
    return db.listar_produtos()

@st.cache_data(ttl=60)
def get_vendas_cached(data_inicio, data_fim):
    """Retorna vendas do período com cache"""
    db = Database()
    return db.listar_vendas(data_inicio, data_fim)

@st.cache_data(ttl=60)
def get_resumo_vendas_cached(data_inicio, data_fim):
    """Retorna resumo de vendas com cache"""
    db = Database()
    return db.get_resumo_vendas(data_inicio, data_fim)

@st.cache_data(ttl=300)  # Cache de 5 minutos
def get_categorias_cached():
    """Retorna categorias com cache"""
    db = Database()
    return db.listar_categorias()

# CSS Customizado
st.markdown("""
<style>
    /* Tema principal */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Cards customizados */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2.5em;
        font-weight: bold;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 0.9em;
        opacity: 0.9;
    }
    
    /* Botões */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1e3a8a;
    }
    
    /* Alertas */
    .alert-success {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 15px;
        border-radius: 4px;
        margin: 10px 0;
    }
    
    .alert-danger {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 15px;
        border-radius: 4px;
        margin: 10px 0;
    }
    
    .alert-warning {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 15px;
        border-radius: 4px;
        margin: 10px 0;
    }
    
    /* Tabelas */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar sessão
if 'db' not in st.session_state:
    st.session_state.db = Database()

if 'page' not in st.session_state:
    st.session_state.page = 'Dashboard'

# Sidebar - Navegação
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/1e3a8a/ffffff?text=DGTECH", use_container_width=True)
    st.title("🏢 DGTECH GESTÃO")
    st.markdown("---")
    
    # Menu de navegação
    pages = {
        "📊 Dashboard": "dashboard",
        "📦 Produtos": "produtos",
        "🛒 Vendas": "vendas",
        "💰 Financeiro": "financeiro",
        "📊 Relatórios": "relatorios",
        "⚙️ Configurações": "configuracoes"
    }
    
    for page_name, page_id in pages.items():
        if st.button(page_name, key=page_id, use_container_width=True):
            st.session_state.page = page_name
    
    st.markdown("---")
    st.caption("v2.0 Web | Firebase Edition")
    st.caption("© 2025 DGTECH")

# Conteúdo principal
def show_dashboard():
    st.title("📊 Dashboard")
    
    # Filtro de período
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        periodo = st.selectbox(
            "Período",
            ["Hoje", "Esta Semana", "Este Mês", "Este Ano"],
            key="periodo_dashboard"
        )
    with col2:
        data_inicio = st.date_input("Data Início", datetime.now() - timedelta(days=30))
        data_fim = st.date_input("Data Fim", datetime.now())
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Atualizar", use_container_width=True):
            st.rerun()
    
    # Determinar período
    if periodo == "Hoje":
        data_inicio_str = Periodo.hoje()
        data_fim_str = Periodo.hoje()
    elif periodo == "Esta Semana":
        data_inicio_str = Periodo.inicio_semana()
        data_fim_str = Periodo.fim_semana()
    elif periodo == "Este Mês":
        data_inicio_str = Periodo.inicio_mes()
        data_fim_str = Periodo.fim_mes()
    else:
        data_inicio_str = Periodo.inicio_ano()
        data_fim_str = Periodo.fim_ano()
    
    # KPIs
    resumo = st.session_state.db.get_resumo_vendas(data_inicio_str, data_fim_str)
    financeiro = st.session_state.db.get_lucro_periodo(data_inicio_str, data_fim_str)
    
    # Calcular valor em estoque
    produtos = st.session_state.db.listar_produtos()
    valor_estoque = sum(p['preco_venda'] * p['estoque'] for p in produtos)
    
    # Calcular margem média
    margem_media = 0
    if produtos:
        margens = [(p['preco_venda'] - p['preco_custo']) / p['preco_venda'] * 100 
                   for p in produtos if p['preco_venda'] > 0]
        margem_media = sum(margens) / len(margens) if margens else 0
    
    # Consolidar KPIs
    kpis = {
        'receita_total': resumo['receita_total'],
        'lucro_liquido': financeiro['lucro_liquido'],
        'total_vendas': resumo['total_vendas'],
        'ticket_medio': resumo['ticket_medio'],
        'lucro_bruto': financeiro['lucro_bruto'],
        'despesas': financeiro['despesas'],
        'valor_estoque': valor_estoque,
        'total_despesas': financeiro['despesas'],
        'margem_media': margem_media
    }
    
    # Cards de KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Receita Total",
            value=Formatador.formatar_moeda(kpis['receita_total']),
            delta=f"+{kpis.get('variacao_receita', 0):.1f}%"
        )
    
    with col2:
        st.metric(
            label="📈 Lucro Líquido",
            value=Formatador.formatar_moeda(kpis['lucro_liquido']),
            delta=f"+{kpis.get('variacao_lucro', 0):.1f}%"
        )
    
    with col3:
        st.metric(
            label="🛒 Total de Vendas",
            value=str(kpis['total_vendas']),
            delta=f"+{kpis.get('variacao_vendas', 0)}"
        )
    
    with col4:
        st.metric(
            label="🎫 Ticket Médio",
            value=Formatador.formatar_moeda(kpis['ticket_medio'])
        )
    
    # Segunda linha de KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📦 Valor em Estoque",
            value=Formatador.formatar_moeda(kpis['valor_estoque'])
        )
    
    with col2:
        st.metric(
            label="💸 Despesas",
            value=Formatador.formatar_moeda(kpis['total_despesas'])
        )
    
    with col3:
        st.metric(
            label="📊 Margem Média",
            value=Formatador.formatar_porcentagem(kpis['margem_media'])
        )
    
    with col4:
        alertas = st.session_state.db.produtos_estoque_baixo()
        st.metric(
            label="⚠️ Alertas de Estoque",
            value=str(len(alertas)),
            delta="Crítico" if len(alertas) > 0 else "OK",
            delta_color="inverse"
        )
    
    st.markdown("---")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Evolução de Vendas")
        vendas = st.session_state.db.listar_vendas(data_inicio_str, data_fim_str)
        
        if vendas:
            # Agrupar por data
            vendas_por_data = {}
            for venda in vendas:
                data = venda['data_venda'][:10]
                if data not in vendas_por_data:
                    vendas_por_data[data] = 0
                vendas_por_data[data] += venda['valor_total']
            
            # Criar gráfico
            df_vendas = pd.DataFrame(list(vendas_por_data.items()), columns=['Data', 'Receita'])
            df_vendas['Data'] = pd.to_datetime(df_vendas['Data'])
            
            fig = px.line(
                df_vendas,
                x='Data',
                y='Receita',
                title='',
                markers=True
            )
            fig.update_traces(line_color='#667eea', line_width=3)
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📭 Nenhuma venda no período selecionado")
    
    with col2:
        st.subheader("🏆 Top 5 Produtos")
        top_produtos = st.session_state.db.get_produtos_mais_vendidos(5)
        
        if top_produtos:
            df_top = pd.DataFrame(top_produtos)
            fig = px.bar(
                df_top,
                x='nome',
                y='quantidade_vendida',
                title='',
                color='quantidade_vendida',
                color_continuous_scale='viridis'
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📭 Nenhum produto vendido no período")

def show_produtos():
    st.title("📦 Gestão de Produtos")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📋 Lista de Produtos", "➕ Novo Produto", "⚠️ Alertas de Estoque"])
    
    with tab1:
        # Filtros
        col1, col2, col3 = st.columns(3)
        with col1:
            busca = st.text_input("🔍 Buscar produto", placeholder="Nome ou código...")
        with col2:
            categorias = st.session_state.db.listar_categorias()
            cat_opcoes = ["Todas"] + [c['nome'] for c in categorias]
            categoria_filtro = st.selectbox("Categoria", cat_opcoes)
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Atualizar Lista", use_container_width=True):
                st.rerun()
        
        # Lista de produtos (incluindo inativos)
        produtos = st.session_state.db.listar_produtos(apenas_ativos=False)
        
        if produtos:
            # Aplicar filtros
            produtos_filtrados = produtos.copy()
            
            if busca:
                produtos_filtrados = [p for p in produtos_filtrados if busca.lower() in p['nome'].lower()]
            
            if categoria_filtro != "Todas":
                produtos_filtrados = [p for p in produtos_filtrados if p.get('categoria_nome') == categoria_filtro]
            
            st.caption(f"📊 Total: {len(produtos_filtrados)} produtos encontrados")
            st.markdown("---")
            
            # Exibir produtos em cards
            for produto in produtos_filtrados:
                with st.expander(f"📦 {produto['nome']} - {Formatador.formatar_moeda(produto['preco_venda'])}"):
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.write(f"**Categoria:** {produto.get('categoria_nome', 'Sem categoria')}")
                        st.write(f"**Estoque:** {produto['estoque']} unidades")
                        st.write(f"**Estoque Mínimo:** {produto['estoque_minimo']}")
                        
                        # Alerta de estoque baixo
                        if produto['estoque'] <= produto['estoque_minimo']:
                            st.warning("⚠️ Estoque baixo!")
                    
                    with col2:
                        st.write(f"**Preço Custo:** {Formatador.formatar_moeda(produto['preco_custo'])}")
                        st.write(f"**Preço Venda:** {Formatador.formatar_moeda(produto['preco_venda'])}")
                        
                        # Calcular margem
                        if produto['preco_custo'] > 0:
                            margem = ((produto['preco_venda'] - produto['preco_custo']) / produto['preco_custo']) * 100
                            st.write(f"**Margem:** {margem:.1f}%")
                        
                        # Status
                        status = "✅ Ativo" if produto.get('ativo', True) else "❌ Inativo"
                        st.write(f"**Status:** {status}")
                    
                    with col3:
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # Botão de ativar/desativar
                        if produto.get('ativo', True):
                            if st.button("🔒 Desativar", key=f"deactivate_{produto['id']}", use_container_width=True):
                                try:
                                    st.session_state.db.atualizar_produto_status(produto['id'], False)
                                    st.success("✅ Produto desativado!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Erro: {str(e)}")
                        else:
                            if st.button("✅ Ativar", key=f"activate_{produto['id']}", use_container_width=True):
                                try:
                                    st.session_state.db.atualizar_produto_status(produto['id'], True)
                                    st.success("✅ Produto ativado!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Erro: {str(e)}")
                        
                        # Botão de excluir
                        if st.button("🗑️ Excluir", key=f"delete_{produto['id']}", type="secondary", use_container_width=True):
                            # Verificar se tem confirmação pendente
                            confirm_key = f"confirm_delete_{produto['id']}"
                            
                            if st.session_state.get(confirm_key, False):
                                try:
                                    # Excluir permanentemente
                                    st.session_state.db.excluir_produto_permanente(produto['id'])
                                    st.success(f"✅ Produto '{produto['nome']}' excluído permanentemente!")
                                    st.session_state[confirm_key] = False
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ {str(e)}")
                                    st.info("💡 Você pode desativar o produto em vez de excluí-lo.")
                                    st.session_state[confirm_key] = False
                            else:
                                st.session_state[confirm_key] = True
                                st.warning("⚠️ ATENÇÃO! Esta ação é IRREVERSÍVEL. Clique novamente para confirmar a exclusão permanente.")
                                st.rerun()
        else:
            st.info("📭 Nenhum produto cadastrado")
    
    with tab2:
        with st.form("form_produto"):
            st.subheader("Novo Produto")
            
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("Nome do Produto *")
                descricao = st.text_area("Descrição")
                categoria = st.selectbox(
                    "Categoria *",
                    options=[c['nome'] for c in categorias] if categorias else ["Sem categoria"]
                )
                codigo_barras = st.text_input("Código de Barras")
            
            with col2:
                preco_custo = st.number_input("Preço de Custo (R$) *", min_value=0.0, format="%.2f")
                preco_venda = st.number_input("Preço de Venda (R$) *", min_value=0.0, format="%.2f")
                estoque = st.number_input("Estoque Inicial *", min_value=0, value=0)
                estoque_minimo = st.number_input("Estoque Mínimo", min_value=0, value=10)
            
            # Margem calculada
            if preco_custo > 0:
                margem = ((preco_venda - preco_custo) / preco_custo) * 100
                st.info(f"💰 Margem de Lucro: {margem:.1f}%")
            
            submitted = st.form_submit_button("💾 Salvar Produto", use_container_width=True)
            
            if submitted:
                if not nome or not categoria or preco_custo <= 0 or preco_venda <= 0:
                    st.error("❌ Preencha todos os campos obrigatórios!")
                else:
                    try:
                        # Buscar ID da categoria
                        cat_obj = next((c for c in categorias if c['nome'] == categoria), None)
                        cat_id = cat_obj['id'] if cat_obj else 1
                        
                        st.session_state.db.adicionar_produto(
                            nome=nome,
                            descricao=descricao,
                            categoria_id=cat_id,
                            preco_custo=preco_custo,
                            preco_venda=preco_venda,
                            estoque=estoque,
                            estoque_minimo=estoque_minimo,
                            imagem_path=""
                        )
                        st.success("✅ Produto cadastrado com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao cadastrar produto: {str(e)}")
    
    with tab3:
        alertas = st.session_state.db.produtos_estoque_baixo()
        
        if alertas:
            st.warning(f"⚠️ {len(alertas)} produtos com estoque baixo!")
            
            for produto in alertas:
                with st.expander(f"📦 {produto['nome']} - Estoque: {produto['estoque']}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Estoque Atual:** {produto['estoque']}")
                        st.write(f"**Estoque Mínimo:** {produto['estoque_minimo']}")
                    with col2:
                        st.write(f"**Preço:** {Formatador.formatar_moeda(produto['preco_venda'])}")
                        st.write(f"**Categoria:** {produto.get('categoria_nome', 'S/Cat')}")
                    with col3:
                        qtd_repor = st.number_input(
                            "Quantidade a repor",
                            min_value=1,
                            value=produto['estoque_minimo'] * 2,
                            key=f"repor_{produto['id']}"
                        )
                        if st.button(f"✅ Repor", key=f"btn_repor_{produto['id']}"):
                            st.session_state.db.adicionar_estoque(produto['id'], qtd_repor)
                            st.success(f"✅ {qtd_repor} unidades adicionadas!")
                            st.rerun()
        else:
            st.success("✅ Todos os produtos com estoque adequado!")

def show_vendas():
    st.title("🛒 Gestão de Vendas")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📋 Lista de Vendas", "➕ Nova Venda", "📊 Análise"])
    
    with tab1:
        # Filtros
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            data_inicio = st.date_input("Data Início", value=pd.Timestamp.now() - pd.Timedelta(days=30))
        with col2:
            data_fim = st.date_input("Data Fim", value=pd.Timestamp.now())
        with col3:
            busca_cliente = st.text_input("🔍 Cliente", placeholder="Nome do cliente...")
        with col4:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Atualizar", use_container_width=True):
                st.rerun()
        
        # Listar vendas
        vendas = st.session_state.db.listar_vendas(
            data_inicio.strftime("%Y-%m-%d"),
            data_fim.strftime("%Y-%m-%d")
        )
        
        if vendas:
            # Filtrar por cliente
            if busca_cliente:
                vendas = [v for v in vendas if busca_cliente.lower() in v.get('cliente', '').lower()]
            
            # Estatísticas
            total_vendas = len(vendas)
            receita_total = sum(v['valor_total'] for v in vendas)
            ticket_medio = receita_total / total_vendas if total_vendas > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Vendas", total_vendas)
            with col2:
                st.metric("Receita Total", Formatador.formatar_moeda(receita_total))
            with col3:
                st.metric("Ticket Médio", Formatador.formatar_moeda(ticket_medio))
            
            st.markdown("---")
            
            # Tabela de vendas
            for venda in vendas:
                with st.expander(f"🛒 Venda #{venda['id']} - {venda['data_venda'][:10]} - {Formatador.formatar_moeda(venda['valor_total'])}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Produto:** {venda['produto_nome']}")
                        st.write(f"**Quantidade:** {venda['quantidade']}")
                        st.write(f"**Preço Unitário:** {Formatador.formatar_moeda(venda['preco_unitario'])}")
                        st.write(f"**Cliente:** {venda.get('cliente', 'Não informado')}")
                        if venda.get('observacoes'):
                            st.write(f"**Obs:** {venda['observacoes']}")
                    
                    with col2:
                        if st.button("🗑️ Excluir", key=f"del_venda_{venda['id']}", type="secondary"):
                            if st.session_state.get(f"confirm_del_{venda['id']}", False):
                                try:
                                    st.session_state.db.excluir_venda(venda['id'])
                                    st.success("✅ Venda excluída!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Erro: {str(e)}")
                            else:
                                st.session_state[f"confirm_del_{venda['id']}"] = True
                                st.warning("⚠️ Clique novamente para confirmar")
                        
                        if st.button("📄 PDF", key=f"pdf_venda_{venda['id']}", use_container_width=True):
                            st.info("🚧 Exportação em desenvolvimento")
            
            # Exportação em massa
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📊 Exportar para Excel", use_container_width=True):
                    st.info("🚧 Em desenvolvimento")
            with col2:
                if st.button("📄 Exportar para PDF", use_container_width=True):
                    st.info("🚧 Em desenvolvimento")
        else:
            st.info("📭 Nenhuma venda encontrada no período")
    
    with tab2:
        st.subheader("➕ Registrar Nova Venda")
        
        with st.form("form_nova_venda"):
            col1, col2 = st.columns(2)
            
            with col1:
                # Selecionar produto
                produtos = st.session_state.db.listar_produtos()
                produtos_ativos = [p for p in produtos if p.get('ativo', True) and p['estoque'] > 0]
                
                if not produtos_ativos:
                    st.error("❌ Nenhum produto disponível em estoque!")
                    st.stop()
                
                produto_opcoes = {f"{p['nome']} (Estoque: {p['estoque']})": p['id'] for p in produtos_ativos}
                produto_selecionado = st.selectbox("Produto*", list(produto_opcoes.keys()))
                produto_id = produto_opcoes[produto_selecionado]
                
                # Encontrar produto para pegar dados
                produto = next(p for p in produtos_ativos if p['id'] == produto_id)
                
                quantidade = st.number_input(
                    "Quantidade*",
                    min_value=1,
                    max_value=produto['estoque'],
                    value=1
                )
                
                preco_unitario = st.number_input(
                    "Preço Unitário*",
                    min_value=0.01,
                    value=float(produto['preco_venda']),
                    format="%.2f"
                )
            
            with col2:
                cliente = st.text_input("Cliente", placeholder="Nome do cliente (opcional)")
                
                data_venda = st.date_input("Data da Venda", value=pd.Timestamp.now())
                
                observacoes = st.text_area("Observações", placeholder="Informações adicionais...")
                
                # Cálculo automático
                valor_total = quantidade * preco_unitario
                margem = ((preco_unitario - produto['preco_custo']) / preco_unitario * 100) if preco_unitario > 0 else 0
                
                st.metric("💰 Valor Total", Formatador.formatar_moeda(valor_total))
                st.metric("📊 Margem de Lucro", f"{margem:.1f}%")
            
            submitted = st.form_submit_button("✅ Registrar Venda", use_container_width=True, type="primary")
            
            if submitted:
                try:
                    st.session_state.db.registrar_venda(
                        produto_id=produto_id,
                        quantidade=quantidade,
                        preco_unitario=preco_unitario,
                        cliente=cliente or "",
                        observacoes=observacoes or ""
                    )
                    st.success(f"✅ Venda registrada com sucesso! Valor: {Formatador.formatar_moeda(valor_total)}")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao registrar venda: {str(e)}")
    
    with tab3:
        st.subheader("📊 Análise de Vendas")
        
        # Período
        col1, col2 = st.columns(2)
        with col1:
            data_inicio = st.date_input("De", value=pd.Timestamp.now() - pd.Timedelta(days=30), key="analise_inicio")
        with col2:
            data_fim = st.date_input("Até", value=pd.Timestamp.now(), key="analise_fim")
        
        vendas = st.session_state.db.listar_vendas(
            data_inicio.strftime("%Y-%m-%d"),
            data_fim.strftime("%Y-%m-%d")
        )
        
        if vendas:
            # Vendas por dia
            st.subheader("📅 Vendas por Dia")
            vendas_por_dia = {}
            for venda in vendas:
                dia = venda['data_venda'][:10]
                if dia not in vendas_por_dia:
                    vendas_por_dia[dia] = {'quantidade': 0, 'valor': 0}
                vendas_por_dia[dia]['quantidade'] += venda['quantidade']
                vendas_por_dia[dia]['valor'] += venda['valor_total']
            
            df_dias = pd.DataFrame([
                {'Data': dia, 'Quantidade': info['quantidade'], 'Receita': info['valor']}
                for dia, info in vendas_por_dia.items()
            ])
            df_dias['Data'] = pd.to_datetime(df_dias['Data'])
            df_dias = df_dias.sort_values('Data')
            
            fig = px.line(df_dias, x='Data', y='Receita', markers=True, title='Receita Diária')
            fig.update_traces(line_color='#667eea', line_width=3)
            st.plotly_chart(fig, use_container_width=True)
            
            # Produtos mais vendidos
            st.subheader("🏆 Produtos Mais Vendidos no Período")
            vendas_por_produto = {}
            for venda in vendas:
                nome = venda['produto_nome']
                if nome not in vendas_por_produto:
                    vendas_por_produto[nome] = {'quantidade': 0, 'receita': 0}
                vendas_por_produto[nome]['quantidade'] += venda['quantidade']
                vendas_por_produto[nome]['receita'] += venda['valor_total']
            
            df_produtos = pd.DataFrame([
                {'Produto': nome, 'Quantidade': info['quantidade'], 'Receita': info['receita']}
                for nome, info in vendas_por_produto.items()
            ]).sort_values('Receita', ascending=False).head(10)
            
            fig = px.bar(df_produtos, x='Produto', y='Receita', title='Top 10 Produtos')
            fig.update_traces(marker_color='#667eea')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📭 Nenhuma venda para análise")

def show_financeiro():
    st.title("💰 Gestão Financeira")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Resumo Financeiro", "💸 Despesas", "📈 Fluxo de Caixa"])
    
    with tab1:
        # Período
        col1, col2, col3 = st.columns(3)
        with col1:
            periodo = st.selectbox("Período", ["Hoje", "Esta Semana", "Este Mês", "Este Ano"])
        
        # Calcular datas
        if periodo == "Hoje":
            data_inicio = Periodo.hoje()
            data_fim = Periodo.hoje()
        elif periodo == "Esta Semana":
            data_inicio = Periodo.inicio_semana()
            data_fim = Periodo.fim_semana()
        elif periodo == "Este Mês":
            data_inicio = Periodo.inicio_mes()
            data_fim = Periodo.fim_mes()
        else:
            data_inicio = Periodo.inicio_ano()
            data_fim = Periodo.fim_ano()
        
        # Obter dados
        resumo_vendas = st.session_state.db.get_resumo_vendas(data_inicio, data_fim)
        lucro_periodo = st.session_state.db.get_lucro_periodo(data_inicio, data_fim)
        
        # Cards principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "💰 Receita Total",
                Formatador.formatar_moeda(resumo_vendas['receita_total'])
            )
        
        with col2:
            st.metric(
                "💵 Lucro Bruto",
                Formatador.formatar_moeda(lucro_periodo['lucro_bruto'])
            )
        
        with col3:
            st.metric(
                "💸 Despesas",
                Formatador.formatar_moeda(lucro_periodo['despesas'])
            )
        
        with col4:
            lucro_liquido = lucro_periodo['lucro_liquido']
            st.metric(
                "📈 Lucro Líquido",
                Formatador.formatar_moeda(lucro_liquido),
                delta=f"{lucro_liquido:.2f}",
                delta_color="normal" if lucro_liquido >= 0 else "inverse"
            )
        
        st.markdown("---")
        
        # Gráfico de Pizza - Distribuição
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Distribuição Financeira")
            if lucro_periodo['lucro_bruto'] > 0 or lucro_periodo['despesas'] > 0:
                fig = px.pie(
                    values=[lucro_periodo['lucro_bruto'], lucro_periodo['despesas']],
                    names=['Lucro Bruto', 'Despesas'],
                    title='',
                    color_discrete_sequence=['#667eea', '#f56565']
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("📭 Sem dados financeiros")
        
        with col2:
            st.subheader("💹 Evolução do Lucro")
            vendas = st.session_state.db.listar_vendas(data_inicio, data_fim)
            despesas = st.session_state.db.listar_despesas(data_inicio, data_fim)
            
            if vendas or despesas:
                # Agrupar por data
                dados_por_dia = {}
                
                for venda in vendas:
                    dia = venda['data_venda'][:10]
                    if dia not in dados_por_dia:
                        dados_por_dia[dia] = {'receita': 0, 'despesas': 0}
                    dados_por_dia[dia]['receita'] += venda['valor_total']
                
                for despesa in despesas:
                    dia = despesa['data_despesa'][:10]
                    if dia not in dados_por_dia:
                        dados_por_dia[dia] = {'receita': 0, 'despesas': 0}
                    dados_por_dia[dia]['despesas'] += despesa['valor']
                
                df_evolucao = pd.DataFrame([
                    {
                        'Data': dia,
                        'Receita': info['receita'],
                        'Despesas': info['despesas'],
                        'Lucro': info['receita'] - info['despesas']
                    }
                    for dia, info in dados_por_dia.items()
                ])
                df_evolucao['Data'] = pd.to_datetime(df_evolucao['Data'])
                df_evolucao = df_evolucao.sort_values('Data')
                
                fig = px.line(df_evolucao, x='Data', y='Lucro', markers=True, title='')
                fig.update_traces(line_color='#667eea', line_width=3)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("📭 Sem dados para o período")
    
    with tab2:
        st.subheader("💸 Gestão de Despesas")
        
        # Formulário de nova despesa
        with st.expander("➕ Adicionar Nova Despesa"):
            with st.form("form_despesa"):
                col1, col2 = st.columns(2)
                
                with col1:
                    descricao = st.text_input("Descrição*", placeholder="Ex: Aluguel, Luz, Internet...")
                    valor = st.number_input("Valor*", min_value=0.01, format="%.2f")
                
                with col2:
                    categorias = st.session_state.db.listar_categorias()
                    cat_opcoes = [c['nome'] for c in categorias]
                    categoria = st.selectbox("Categoria", cat_opcoes if cat_opcoes else ["Geral"])
                    
                    data_despesa = st.date_input("Data", value=pd.Timestamp.now())
                
                observacoes = st.text_area("Observações", placeholder="Detalhes adicionais...")
                
                submitted = st.form_submit_button("💾 Salvar Despesa", use_container_width=True, type="primary")
                
                if submitted:
                    if not descricao:
                        st.error("❌ Descrição é obrigatória!")
                    else:
                        try:
                            st.session_state.db.adicionar_despesa(
                                descricao=descricao,
                                valor=valor,
                                categoria=categoria,
                                data_despesa=data_despesa.strftime("%Y-%m-%d"),
                                observacoes=observacoes or ""
                            )
                            st.success("✅ Despesa registrada com sucesso!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erro: {str(e)}")
        
        # Lista de despesas
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            data_inicio = st.date_input("De", value=pd.Timestamp.now() - pd.Timedelta(days=30), key="desp_inicio")
        with col2:
            data_fim = st.date_input("Até", value=pd.Timestamp.now(), key="desp_fim")
        
        despesas = st.session_state.db.listar_despesas(
            data_inicio.strftime("%Y-%m-%d"),
            data_fim.strftime("%Y-%m-%d")
        )
        
        if despesas:
            total_despesas = sum(d['valor'] for d in despesas)
            st.metric("💸 Total de Despesas", Formatador.formatar_moeda(total_despesas))
            
            st.markdown("---")
            
            for despesa in despesas:
                with st.expander(f"💸 {despesa['descricao']} - {Formatador.formatar_moeda(despesa['valor'])} - {despesa['data_despesa'][:10]}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Categoria:** {despesa['categoria']}")
                        if despesa.get('observacoes'):
                            st.write(f"**Obs:** {despesa['observacoes']}")
                    
                    with col2:
                        if st.button("🗑️ Excluir", key=f"del_desp_{despesa['id']}"):
                            try:
                                st.session_state.db.remover_despesa(despesa['id'])
                                st.success("✅ Despesa excluída!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erro: {str(e)}")
        else:
            st.info("📭 Nenhuma despesa no período")
    
    with tab3:
        st.subheader("📈 Fluxo de Caixa")
        
        # Período
        col1, col2 = st.columns(2)
        with col1:
            data_inicio = st.date_input("De", value=pd.Timestamp.now() - pd.Timedelta(days=90), key="fluxo_inicio")
        with col2:
            data_fim = st.date_input("Até", value=pd.Timestamp.now(), key="fluxo_fim")
        
        vendas = st.session_state.db.listar_vendas(
            data_inicio.strftime("%Y-%m-%d"),
            data_fim.strftime("%Y-%m-%d")
        )
        despesas = st.session_state.db.listar_despesas(
            data_inicio.strftime("%Y-%m-%d"),
            data_fim.strftime("%Y-%m-%d")
        )
        
        if vendas or despesas:
            # Consolidar dados
            fluxo = {}
            
            for venda in vendas:
                dia = venda['data_venda'][:10]
                if dia not in fluxo:
                    fluxo[dia] = {'entradas': 0, 'saidas': 0}
                fluxo[dia]['entradas'] += venda['valor_total']
            
            for despesa in despesas:
                dia = despesa['data_despesa'][:10]
                if dia not in fluxo:
                    fluxo[dia] = {'entradas': 0, 'saidas': 0}
                fluxo[dia]['saidas'] += despesa['valor']
            
            # Criar DataFrame
            df_fluxo = pd.DataFrame([
                {
                    'Data': dia,
                    'Entradas': info['entradas'],
                    'Saídas': info['saidas'],
                    'Saldo': info['entradas'] - info['saidas']
                }
                for dia, info in fluxo.items()
            ])
            df_fluxo['Data'] = pd.to_datetime(df_fluxo['Data'])
            df_fluxo = df_fluxo.sort_values('Data')
            df_fluxo['Saldo Acumulado'] = df_fluxo['Saldo'].cumsum()
            
            # Gráfico de barras - Entradas vs Saídas
            fig = px.bar(
                df_fluxo,
                x='Data',
                y=['Entradas', 'Saídas'],
                title='Fluxo de Caixa - Entradas vs Saídas',
                barmode='group',
                color_discrete_map={'Entradas': '#48bb78', 'Saídas': '#f56565'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Gráfico de linha - Saldo Acumulado
            fig2 = px.line(
                df_fluxo,
                x='Data',
                y='Saldo Acumulado',
                title='Saldo Acumulado',
                markers=True
            )
            fig2.update_traces(line_color='#667eea', line_width=3)
            st.plotly_chart(fig2, use_container_width=True)
            
            # Tabela resumo
            st.subheader("📋 Resumo do Período")
            total_entradas = df_fluxo['Entradas'].sum()
            total_saidas = df_fluxo['Saídas'].sum()
            saldo_final = total_entradas - total_saidas
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("💰 Total Entradas", Formatador.formatar_moeda(total_entradas))
            with col2:
                st.metric("💸 Total Saídas", Formatador.formatar_moeda(total_saidas))
            with col3:
                st.metric(
                    "📊 Saldo Final",
                    Formatador.formatar_moeda(saldo_final),
                    delta=f"{saldo_final:.2f}",
                    delta_color="normal" if saldo_final >= 0 else "inverse"
                )
        else:
            st.info("📭 Sem dados de fluxo de caixa")

def show_relatorios():
    st.title("📊 Relatórios Avançados")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📈 Análise ABC", "🎯 Metas", "⚠️ Alertas Inteligentes"])
    
    with tab1:
        st.subheader("📈 Análise ABC de Produtos")
        st.info("🚧 Relatório em desenvolvimento - Classificação ABC por faturamento")
        
        produtos = st.session_state.db.get_produtos_mais_vendidos(50)
        
        if produtos:
            df = pd.DataFrame(produtos)
            df = df.sort_values('receita_total', ascending=False)
            df['percentual'] = (df['receita_total'] / df['receita_total'].sum() * 100).round(2)
            df['acumulado'] = df['percentual'].cumsum()
            
            # Classificar
            df['classe'] = df['acumulado'].apply(
                lambda x: 'A' if x <= 80 else ('B' if x <= 95 else 'C')
            )
            
            # Mostrar gráfico
            fig = px.bar(
                df.head(20),
                x='nome',
                y='receita_total',
                color='classe',
                title='Top 20 Produtos - Classificação ABC',
                color_discrete_map={'A': '#48bb78', 'B': '#ed8936', 'C': '#f56565'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Resumo por classe
            st.subheader("📊 Resumo por Classe")
            resumo = df.groupby('classe').agg({
                'nome': 'count',
                'receita_total': 'sum',
                'percentual': 'sum'
            }).round(2)
            resumo.columns = ['Quantidade', 'Receita Total', 'Participação %']
            st.dataframe(resumo, use_container_width=True)
        else:
            st.info("📭 Sem dados para análise ABC")
    
    with tab2:
        st.subheader("🎯 Metas de Vendas")
        
        # Definir meta
        with st.expander("➕ Definir Nova Meta"):
            with st.form("form_meta"):
                col1, col2 = st.columns(2)
                
                with col1:
                    meta_valor = st.number_input("Valor da Meta (R$)", min_value=0.01, format="%.2f")
                    meta_mes = st.selectbox("Mês", [
                        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
                    ])
                
                with col2:
                    meta_ano = st.number_input("Ano", min_value=2020, max_value=2030, value=2025)
                
                if st.form_submit_button("💾 Salvar Meta", use_container_width=True):
                    st.success("✅ Meta salva! (funcionalidade em desenvolvimento)")
        
        # Mostrar progresso da meta atual
        st.markdown("---")
        st.subheader("📊 Progresso do Mês Atual")
        
        mes_atual = pd.Timestamp.now().month
        ano_atual = pd.Timestamp.now().year
        
        data_inicio = f"{ano_atual}-{mes_atual:02d}-01"
        data_fim = Periodo.fim_mes()
        
        resumo = st.session_state.db.get_resumo_vendas(data_inicio, data_fim)
        receita_atual = resumo['receita_total']
        
        # Meta exemplo (idealmente viria do banco)
        meta_mensal = 10000.00
        progresso = (receita_atual / meta_mensal * 100) if meta_mensal > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🎯 Meta do Mês", Formatador.formatar_moeda(meta_mensal))
        with col2:
            st.metric("💰 Realizado", Formatador.formatar_moeda(receita_atual))
        with col3:
            st.metric("📊 Progresso", f"{progresso:.1f}%")
        
        # Barra de progresso
        st.progress(min(progresso / 100, 1.0))
        
        if progresso >= 100:
            st.success("🎉 Parabéns! Meta atingida!")
        elif progresso >= 75:
            st.warning("⚠️ Falta pouco para atingir a meta!")
        else:
            faltam = meta_mensal - receita_atual
            st.info(f"💡 Faltam {Formatador.formatar_moeda(faltam)} para atingir a meta")
    
    with tab3:
        st.subheader("⚠️ Alertas Inteligentes")
        
        # Produtos com estoque baixo
        alertas_estoque = st.session_state.db.produtos_estoque_baixo()
        if alertas_estoque:
            st.warning(f"📦 **{len(alertas_estoque)} produtos** com estoque abaixo do mínimo!")
            with st.expander("Ver Produtos"):
                for p in alertas_estoque:
                    st.write(f"- **{p['nome']}**: {p['estoque']} unidades (mín: {p['estoque_minimo']})")
        
        # Produtos sem venda recente (últimos 30 dias)
        st.markdown("---")
        vendas_recentes = st.session_state.db.listar_vendas(
            (pd.Timestamp.now() - pd.Timedelta(days=30)).strftime("%Y-%m-%d"),
            pd.Timestamp.now().strftime("%Y-%m-%d")
        )
        produtos_vendidos = set(v['produto_id'] for v in vendas_recentes)
        todos_produtos = st.session_state.db.listar_produtos()
        produtos_parados = [p for p in todos_produtos if p['id'] not in produtos_vendidos and p.get('ativo', True)]
        
        if produtos_parados:
            st.warning(f"🔴 **{len(produtos_parados)} produtos** sem vendas nos últimos 30 dias!")
            with st.expander("Ver Produtos Parados"):
                for p in produtos_parados:
                    valor_parado = p['preco_custo'] * p['estoque']
                    st.write(f"- **{p['nome']}**: {p['estoque']} un. | Valor parado: {Formatador.formatar_moeda(valor_parado)}")
        else:
            st.success("✅ Todos os produtos estão vendendo!")
        
        # Despesas altas
        st.markdown("---")
        despesas_mes = st.session_state.db.listar_despesas(Periodo.inicio_mes(), Periodo.fim_mes())
        if despesas_mes:
            total_despesas = sum(d['valor'] for d in despesas_mes)
            vendas_mes = st.session_state.db.listar_vendas(Periodo.inicio_mes(), Periodo.fim_mes())
            receita_mes = sum(v['valor_total'] for v in vendas_mes) if vendas_mes else 0
            
            if receita_mes > 0:
                percentual_despesas = (total_despesas / receita_mes * 100)
                if percentual_despesas > 50:
                    st.error(f"🚨 **Despesas altas!** {percentual_despesas:.1f}% da receita está em despesas!")
                elif percentual_despesas > 30:
                    st.warning(f"⚠️ **Atenção!** Despesas representam {percentual_despesas:.1f}% da receita")
                else:
                    st.success(f"✅ Despesas controladas: {percentual_despesas:.1f}% da receita")

def show_configuracoes():
    st.title("⚙️ Configurações")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["🏷️ Categorias", "🎯 Metas", "💾 Backup"])
    
    with tab1:
        st.subheader("🏷️ Gestão de Categorias")
        
        # Adicionar categoria
        with st.expander("➕ Nova Categoria"):
            with st.form("form_categoria"):
                nome_cat = st.text_input("Nome da Categoria*", placeholder="Ex: Eletrônicos, Roupas...")
                
                if st.form_submit_button("💾 Salvar", use_container_width=True):
                    if nome_cat:
                        try:
                            st.session_state.db.adicionar_categoria(nome_cat)
                            st.success("✅ Categoria criada!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erro: {str(e)}")
                    else:
                        st.error("❌ Nome é obrigatório!")
        
        # Listar categorias
        st.markdown("---")
        categorias = st.session_state.db.listar_categorias()
        
        if categorias:
            st.write(f"**Total: {len(categorias)} categorias**")
            
            for cat in categorias:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"🏷️ **{cat['nome']}**")
                with col2:
                    if st.button("🗑️", key=f"del_cat_{cat['id']}"):
                        st.warning("⚠️ Funcionalidade em desenvolvimento")
        else:
            st.info("📭 Nenhuma categoria cadastrada")
    
    with tab2:
        st.subheader("🎯 Gerenciar Metas")
        st.info("🚧 Gestão de metas em desenvolvimento")
        
        st.write("""
        **Funcionalidades planejadas:**
        - Definir metas mensais e anuais
        - Acompanhar progresso em tempo real
        - Alertas de desempenho
        - Histórico de metas
        """)
    
    with tab3:
        st.subheader("💾 Backup do Sistema")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Fazer Backup**")
            if st.button("📥 Baixar Backup do Banco de Dados", use_container_width=True):
                try:
                    import shutil
                    from datetime import datetime
                    
                    # Copiar arquivo do banco
                    backup_name = f"backup_dgtech_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
                    shutil.copy2("database.db", backup_name)
                    
                    with open(backup_name, "rb") as file:
                        st.download_button(
                            label="💾 Download Backup",
                            data=file,
                            file_name=backup_name,
                            mime="application/octet-stream",
                            use_container_width=True
                        )
                    st.success("✅ Backup criado!")
                except Exception as e:
                    st.error(f"❌ Erro ao criar backup: {str(e)}")
        
        with col2:
            st.write("**Restaurar Backup**")
            uploaded_file = st.file_uploader("Selecione o arquivo de backup (.db)", type=['db'])
            
            if uploaded_file and st.button("📤 Restaurar", use_container_width=True):
                st.warning("⚠️ Funcionalidade em desenvolvimento")
                st.info("🔒 Por segurança, o restore precisa ser feito manualmente")

# Roteamento de páginas
page = st.session_state.page

if "Dashboard" in page:
    show_dashboard()
elif "Produtos" in page:
    show_produtos()
elif "Vendas" in page:
    show_vendas()
elif "Financeiro" in page:
    show_financeiro()
elif "Relatórios" in page:
    show_relatorios()
elif "Configurações" in page:
    show_configuracoes()
