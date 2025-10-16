"""
Módulo de Análise Inteligente
Análise ABC, produtos parados, previsões e sugestões
"""

from typing import List, Dict, Tuple
from datetime import datetime, timedelta
from database import Database
from utils import Formatador
import statistics

class Analytics:
    def __init__(self, db: Database):
        self.db = db
    
    # ==================== ANÁLISE ABC ====================
    
    def analise_abc(self) -> Dict:
        """
        Análise ABC de produtos baseada em receita
        A: 80% da receita (top produtos)
        B: 15% da receita (produtos intermediários)
        C: 5% da receita (produtos de baixo giro)
        """
        produtos_vendas = self.db.get_produtos_mais_vendidos(1000)
        
        if not produtos_vendas:
            return {'A': [], 'B': [], 'C': [], 'sem_vendas': []}
        
        # Calcular receita total
        receita_total = sum(p['receita_total'] for p in produtos_vendas)
        
        # Ordenar por receita
        produtos_ordenados = sorted(
            produtos_vendas, 
            key=lambda x: x['receita_total'], 
            reverse=True
        )
        
        # Classificar
        abc = {'A': [], 'B': [], 'C': [], 'sem_vendas': []}
        acumulado = 0
        
        for produto in produtos_ordenados:
            participacao = (produto['receita_total'] / receita_total) * 100
            acumulado += participacao
            
            produto['participacao'] = participacao
            produto['acumulado'] = acumulado
            
            if acumulado <= 80:
                abc['A'].append(produto)
            elif acumulado <= 95:
                abc['B'].append(produto)
            else:
                abc['C'].append(produto)
        
        # Produtos sem vendas
        todos_produtos = self.db.listar_produtos()
        produtos_vendidos_ids = [p['nome'] for p in produtos_vendas]
        
        for produto in todos_produtos:
            if produto['nome'] not in produtos_vendidos_ids:
                abc['sem_vendas'].append(produto)
        
        return abc
    
    # ==================== PRODUTOS PARADOS ====================
    
    def produtos_baixa_rotatividade(self, dias: int = 30) -> List[Dict]:
        """
        Identifica produtos com baixa rotatividade (parados no estoque)
        """
        data_inicio = (datetime.now() - timedelta(days=dias)).strftime("%Y-%m-%d")
        vendas = self.db.listar_vendas(data_inicio)
        
        # Produtos vendidos no período
        produtos_vendidos = {}
        for venda in vendas:
            pid = venda['produto_id']
            if pid not in produtos_vendidos:
                produtos_vendidos[pid] = 0
            produtos_vendidos[pid] += venda['quantidade']
        
        # Produtos com estoque mas sem vendas ou vendas baixas
        todos_produtos = self.db.listar_produtos()
        produtos_parados = []
        
        for produto in todos_produtos:
            if produto['estoque'] > 0:
                qtd_vendida = produtos_vendidos.get(produto['id'], 0)
                rotatividade = (qtd_vendida / produto['estoque']) * 100 if produto['estoque'] > 0 else 0
                
                if rotatividade < 10:  # Menos de 10% de rotatividade
                    produtos_parados.append({
                        'id': produto['id'],
                        'nome': produto['nome'],
                        'estoque': produto['estoque'],
                        'qtd_vendida': qtd_vendida,
                        'rotatividade': rotatividade,
                        'valor_parado': produto['preco_custo'] * produto['estoque'],
                        'dias_sem_venda': dias
                    })
        
        return sorted(produtos_parados, key=lambda x: x['valor_parado'], reverse=True)
    
    # ==================== PREVISÃO DE REPOSIÇÃO ====================
    
    def previsao_reposicao(self, dias_historico: int = 90) -> List[Dict]:
        """
        Prevê quando produtos precisarão ser repostos
        """
        data_inicio = (datetime.now() - timedelta(days=dias_historico)).strftime("%Y-%m-%d")
        vendas = self.db.listar_vendas(data_inicio)
        
        # Calcular média de vendas por dia
        vendas_por_produto = {}
        for venda in vendas:
            pid = venda['produto_id']
            if pid not in vendas_por_produto:
                vendas_por_produto[pid] = []
            vendas_por_produto[pid].append(venda['quantidade'])
        
        previsoes = []
        produtos = self.db.listar_produtos()
        
        for produto in produtos:
            pid = produto['id']
            
            if pid in vendas_por_produto and vendas_por_produto[pid]:
                # Média diária
                media_diaria = sum(vendas_por_produto[pid]) / dias_historico
                
                if media_diaria > 0:
                    # Dias até acabar o estoque
                    dias_restantes = produto['estoque'] / media_diaria
                    
                    # Data prevista
                    data_reposicao = datetime.now() + timedelta(days=dias_restantes)
                    
                    # Quantidade sugerida (para 30 dias)
                    qtd_sugerida = int(media_diaria * 30)
                    
                    previsoes.append({
                        'produto_id': pid,
                        'produto_nome': produto['nome'],
                        'estoque_atual': produto['estoque'],
                        'media_diaria': round(media_diaria, 2),
                        'dias_restantes': int(dias_restantes),
                        'data_reposicao': data_reposicao.strftime("%Y-%m-%d"),
                        'qtd_sugerida': qtd_sugerida,
                        'urgencia': 'ALTA' if dias_restantes < 7 else 'MÉDIA' if dias_restantes < 15 else 'BAIXA'
                    })
        
        return sorted(previsoes, key=lambda x: x['dias_restantes'])
    
    # ==================== SUGESTÃO DE PREÇOS ====================
    
    def sugestao_precos(self, produto_id: int) -> Dict:
        """
        Sugere preços baseados em histórico e concorrência
        """
        produto = self.db.buscar_produto(produto_id)
        if not produto:
            return {}
        
        # Buscar histórico de preços
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT preco_venda_novo, data_alteracao
            FROM historico_precos
            WHERE produto_id = ?
            ORDER BY data_alteracao DESC
            LIMIT 10
        ''', (produto_id,))
        historico = cursor.fetchall()
        conn.close()
        
        if not historico:
            # Sem histórico, usar regras básicas
            preco_atual = produto['preco_venda']
            margem_atual = Formatador.calcular_margem(preco_atual, produto['preco_custo'])
            
            return {
                'preco_atual': preco_atual,
                'margem_atual': margem_atual,
                'sugestao_aumento': Formatador.calcular_preco_com_margem(produto['preco_custo'], margem_atual + 5),
                'sugestao_reducao': Formatador.calcular_preco_com_margem(produto['preco_custo'], margem_atual - 5),
                'sugestao_competitivo': Formatador.calcular_preco_com_margem(produto['preco_custo'], 30),
                'recomendacao': 'Manter preço atual'
            }
        
        # Análise com histórico
        precos = [h[0] for h in historico]
        preco_medio = statistics.mean(precos)
        preco_atual = produto['preco_venda']
        
        # Verificar vendas recentes
        vendas_recentes = self.db.listar_vendas(
            (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        )
        vendas_produto = [v for v in vendas_recentes if v['produto_id'] == produto_id]
        
        recomendacao = "Manter preço"
        if len(vendas_produto) < 5:
            recomendacao = "Considere reduzir preço (poucas vendas)"
        elif len(vendas_produto) > 20:
            recomendacao = "Produto vendendo bem, pode aumentar preço"
        
        margem_atual = Formatador.calcular_margem(preco_atual, produto['preco_custo'])
        
        return {
            'preco_atual': preco_atual,
            'preco_medio_historico': preco_medio,
            'margem_atual': margem_atual,
            'vendas_mes': len(vendas_produto),
            'sugestao_aumento': preco_atual * 1.10,
            'sugestao_reducao': preco_atual * 0.90,
            'sugestao_competitivo': Formatador.calcular_preco_com_margem(produto['preco_custo'], 25),
            'recomendacao': recomendacao
        }
    
    # ==================== PREVISÃO DE VENDAS ====================
    
    def previsao_vendas(self, dias_futuro: int = 30) -> Dict:
        """
        Prevê vendas futuras baseado em média móvel simples
        """
        # Buscar vendas dos últimos 90 dias
        data_inicio = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
        vendas = self.db.listar_vendas(data_inicio)
        
        if not vendas:
            return {
                'previsao_receita': 0,
                'previsao_lucro': 0,
                'confianca': 0,
                'tendencia': 'Sem dados'
            }
        
        # Agrupar por dia
        vendas_por_dia = {}
        for venda in vendas:
            data = venda['data_venda'][:10]
            if data not in vendas_por_dia:
                vendas_por_dia[data] = {'receita': 0, 'lucro': 0}
            
            vendas_por_dia[data]['receita'] += venda['valor_total']
            
            # Calcular lucro
            produto = self.db.buscar_produto(venda['produto_id'])
            if produto:
                lucro = (venda['preco_unitario'] - produto['preco_custo']) * venda['quantidade']
                vendas_por_dia[data]['lucro'] += lucro
        
        # Calcular médias
        receitas = [v['receita'] for v in vendas_por_dia.values()]
        lucros = [v['lucro'] for v in vendas_por_dia.values()]
        
        media_receita_dia = statistics.mean(receitas)
        media_lucro_dia = statistics.mean(lucros)
        
        # Previsão para período futuro
        previsao_receita = media_receita_dia * dias_futuro
        previsao_lucro = media_lucro_dia * dias_futuro
        
        # Calcular tendência
        primeira_metade = receitas[:len(receitas)//2]
        segunda_metade = receitas[len(receitas)//2:]
        
        media_primeira = statistics.mean(primeira_metade)
        media_segunda = statistics.mean(segunda_metade)
        
        if media_segunda > media_primeira * 1.1:
            tendencia = "CRESCIMENTO"
        elif media_segunda < media_primeira * 0.9:
            tendencia = "QUEDA"
        else:
            tendencia = "ESTÁVEL"
        
        # Confiança (baseado na variabilidade)
        desvio = statistics.stdev(receitas) if len(receitas) > 1 else 0
        cv = (desvio / media_receita_dia * 100) if media_receita_dia > 0 else 100
        confianca = max(0, 100 - cv)
        
        return {
            'previsao_receita': previsao_receita,
            'previsao_lucro': previsao_lucro,
            'media_diaria': media_receita_dia,
            'confianca': confianca,
            'tendencia': tendencia,
            'dias_analisados': len(vendas_por_dia),
            'dias_previsao': dias_futuro
        }
    
    # ==================== ALERTAS INTELIGENTES ====================
    
    def gerar_alertas_inteligentes(self) -> List[Dict]:
        """
        Gera alertas inteligentes baseados em análises
        """
        alertas = []
        
        # 1. Produtos vendendo muito (aumentar estoque)
        vendas_30dias = self.db.listar_vendas(
            (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        )
        
        vendas_por_produto = {}
        for venda in vendas_30dias:
            pid = venda['produto_id']
            if pid not in vendas_por_produto:
                vendas_por_produto[pid] = 0
            vendas_por_produto[pid] += venda['quantidade']
        
        produtos = self.db.listar_produtos()
        for produto in produtos:
            qtd_vendida = vendas_por_produto.get(produto['id'], 0)
            
            # Alta demanda
            if qtd_vendida > produto['estoque'] * 2:
                alertas.append({
                    'tipo': 'ALTA_DEMANDA',
                    'prioridade': 'ALTA',
                    'icone': '🔥',
                    'titulo': f'Alta demanda: {produto["nome"]}',
                    'mensagem': f'Vendeu {qtd_vendida} unidades em 30 dias. Estoque atual: {produto["estoque"]}',
                    'acao': 'Considere aumentar estoque'
                })
            
            # Produto parado
            elif qtd_vendida == 0 and produto['estoque'] > 10:
                alertas.append({
                    'tipo': 'PRODUTO_PARADO',
                    'prioridade': 'MÉDIA',
                    'icone': '⚠️',
                    'titulo': f'Produto parado: {produto["nome"]}',
                    'mensagem': f'Sem vendas em 30 dias. Estoque: {produto["estoque"]}',
                    'acao': 'Considere promoção ou redução de preço'
                })
        
        # 2. Produtos perto de acabar
        previsoes = self.previsao_reposicao(30)
        for prev in previsoes[:5]:  # Top 5 mais urgentes
            if prev['urgencia'] == 'ALTA':
                alertas.append({
                    'tipo': 'ESTOQUE_ACABANDO',
                    'prioridade': 'ALTA',
                    'icone': '📦',
                    'titulo': f'Repor: {prev["produto_nome"]}',
                    'mensagem': f'Estoque acaba em {prev["dias_restantes"]} dias',
                    'acao': f'Comprar {prev["qtd_sugerida"]} unidades'
                })
        
        # 3. Margem baixa
        for produto in produtos:
            margem = Formatador.calcular_margem(produto['preco_venda'], produto['preco_custo'])
            if margem < 15:
                alertas.append({
                    'tipo': 'MARGEM_BAIXA',
                    'prioridade': 'MÉDIA',
                    'icone': '💰',
                    'titulo': f'Margem baixa: {produto["nome"]}',
                    'mensagem': f'Margem atual: {margem:.1f}%',
                    'acao': 'Revisar preço de venda'
                })
        
        return sorted(alertas, key=lambda x: {'ALTA': 0, 'MÉDIA': 1, 'BAIXA': 2}[x['prioridade']])
    
    # ==================== SAZONALIDADE ====================
    
    def analise_sazonalidade(self) -> Dict:
        """
        Analisa sazonalidade das vendas (dia da semana, hora, mês)
        """
        vendas = self.db.listar_vendas()
        
        if not vendas:
            return {}
        
        vendas_por_dia_semana = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        vendas_por_mes = {i: 0 for i in range(1, 13)}
        vendas_por_hora = {i: 0 for i in range(24)}
        
        for venda in vendas:
            try:
                dt = datetime.strptime(venda['data_venda'], "%Y-%m-%d %H:%M:%S")
                
                # Dia da semana (0=segunda, 6=domingo)
                dia_semana = dt.weekday()
                vendas_por_dia_semana[dia_semana] += venda['valor_total']
                
                # Mês
                mes = dt.month
                vendas_por_mes[mes] += venda['valor_total']
                
                # Hora
                hora = dt.hour
                vendas_por_hora[hora] += venda['valor_total']
            except:
                pass
        
        # Converter para nomes
        dias_nomes = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
        meses_nomes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                      'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        
        return {
            'por_dia_semana': {
                'labels': dias_nomes,
                'valores': [vendas_por_dia_semana[i] for i in range(7)]
            },
            'por_mes': {
                'labels': meses_nomes,
                'valores': [vendas_por_mes[i] for i in range(1, 13)]
            },
            'por_hora': {
                'labels': [f'{i}h' for i in range(24)],
                'valores': [vendas_por_hora[i] for i in range(24)]
            }
        }
