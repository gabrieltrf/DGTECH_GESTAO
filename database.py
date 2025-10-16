"""
Módulo de gerenciamento do banco de dados SQLite
Gerencia produtos, vendas, despesas, categorias e histórico de preços
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import os

class Database:
    def __init__(self, db_name="gestao_vendas.db"):
        """Inicializa a conexão com o banco de dados"""
        self.db_name = db_name
        self.create_tables()
    
    def get_connection(self):
        """Retorna uma conexão com o banco de dados"""
        return sqlite3.connect(self.db_name)
    
    def create_tables(self):
        """Cria as tabelas necessárias no banco de dados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela de categorias
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                descricao TEXT,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de produtos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                categoria_id INTEGER,
                preco_custo REAL NOT NULL,
                preco_venda REAL NOT NULL,
                estoque INTEGER DEFAULT 0,
                estoque_minimo INTEGER DEFAULT 10,
                imagem_path TEXT,
                ativo INTEGER DEFAULT 1,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (categoria_id) REFERENCES categorias(id)
            )
        ''')
        
        # Tabela de vendas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                preco_unitario REAL NOT NULL,
                valor_total REAL NOT NULL,
                cliente TEXT,
                data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                observacoes TEXT,
                FOREIGN KEY (produto_id) REFERENCES produtos(id)
            )
        ''')
        
        # Tabela de despesas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS despesas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL,
                categoria TEXT,
                data_despesa DATE NOT NULL,
                data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                observacoes TEXT
            )
        ''')
        
        # Tabela de histórico de preços
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historico_precos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                preco_custo_anterior REAL,
                preco_custo_novo REAL,
                preco_venda_anterior REAL,
                preco_venda_novo REAL,
                data_alteracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                motivo TEXT,
                FOREIGN KEY (produto_id) REFERENCES produtos(id)
            )
        ''')
        
        # Tabela de configurações
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS configuracoes (
                chave TEXT PRIMARY KEY,
                valor TEXT NOT NULL,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de metas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                valor_meta REAL NOT NULL,
                periodo TEXT NOT NULL,
                data_inicio DATE NOT NULL,
                data_fim DATE NOT NULL,
                ativo INTEGER DEFAULT 1,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Criar índices para melhor performance
        self.criar_indices()
        
        # Inserir configurações padrão
        self.init_default_configs()
    
    def criar_indices(self):
        """Cria índices para otimizar consultas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Índices para melhorar performance
        indices = [
            "CREATE INDEX IF NOT EXISTS idx_produtos_categoria ON produtos(categoria_id)",
            "CREATE INDEX IF NOT EXISTS idx_produtos_ativo ON produtos(ativo)",
            "CREATE INDEX IF NOT EXISTS idx_vendas_produto ON vendas(produto_id)",
            "CREATE INDEX IF NOT EXISTS idx_vendas_data ON vendas(data_venda)",
            "CREATE INDEX IF NOT EXISTS idx_despesas_data ON despesas(data_despesa)",
            "CREATE INDEX IF NOT EXISTS idx_historico_produto ON historico_precos(produto_id)"
        ]
        
        for idx in indices:
            try:
                cursor.execute(idx)
            except:
                pass  # Índice já existe
        
        conn.commit()
        conn.close()
    
    def init_default_configs(self):
        """Inicializa configurações padrão"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        configs = [
            ('tema', 'dark'),
            ('estoque_alerta', '10'),
            ('margem_padrao', '30')
        ]
        
        for chave, valor in configs:
            cursor.execute('''
                INSERT OR IGNORE INTO configuracoes (chave, valor)
                VALUES (?, ?)
            ''', (chave, valor))
        
        conn.commit()
        conn.close()
    
    # ==================== CATEGORIAS ====================
    
    def adicionar_categoria(self, nome: str, descricao: str = "") -> int:
        """Adiciona uma nova categoria"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO categorias (nome, descricao)
            VALUES (?, ?)
        ''', (nome, descricao))
        conn.commit()
        categoria_id = cursor.lastrowid
        conn.close()
        return categoria_id
    
    def listar_categorias(self) -> List[Dict]:
        """Lista todas as categorias"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM categorias ORDER BY nome')
        categorias = []
        for row in cursor.fetchall():
            categorias.append({
                'id': row[0],
                'nome': row[1],
                'descricao': row[2],
                'data_criacao': row[3]
            })
        conn.close()
        return categorias
    
    # ==================== PRODUTOS ====================
    
    def adicionar_produto(self, nome: str, descricao: str, categoria_id: int,
                         preco_custo: float, preco_venda: float, estoque: int = 0,
                         estoque_minimo: int = 10, imagem_path: str = "") -> int:
        """Adiciona um novo produto"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO produtos (nome, descricao, categoria_id, preco_custo, 
                                preco_venda, estoque, estoque_minimo, imagem_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nome, descricao, categoria_id, preco_custo, preco_venda, 
              estoque, estoque_minimo, imagem_path))
        conn.commit()
        produto_id = cursor.lastrowid
        conn.close()
        return produto_id
    
    def atualizar_produto(self, produto_id: int, **kwargs):
        """Atualiza um produto existente"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Buscar valores antigos para histórico de preços
        cursor.execute('SELECT preco_custo, preco_venda FROM produtos WHERE id = ?', (produto_id,))
        row = cursor.fetchone()
        if row:
            preco_custo_antigo, preco_venda_antigo = row
        
        # Atualizar produto
        campos = []
        valores = []
        for campo, valor in kwargs.items():
            campos.append(f"{campo} = ?")
            valores.append(valor)
        
        valores.append(datetime.now())
        valores.append(produto_id)
        
        query = f"UPDATE produtos SET {', '.join(campos)}, data_atualizacao = ? WHERE id = ?"
        cursor.execute(query, valores)
        
        # Registrar histórico de preços se houver mudança
        if 'preco_custo' in kwargs or 'preco_venda' in kwargs:
            novo_custo = kwargs.get('preco_custo', preco_custo_antigo)
            nova_venda = kwargs.get('preco_venda', preco_venda_antigo)
            
            cursor.execute('''
                INSERT INTO historico_precos 
                (produto_id, preco_custo_anterior, preco_custo_novo,
                 preco_venda_anterior, preco_venda_novo, motivo)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (produto_id, preco_custo_antigo, novo_custo,
                  preco_venda_antigo, nova_venda, 'Atualização manual'))
        
        conn.commit()
        conn.close()
    
    def remover_produto(self, produto_id: int):
        """Remove (desativa) um produto"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE produtos SET ativo = 0 WHERE id = ?', (produto_id,))
        conn.commit()
        conn.close()
    
    def listar_produtos(self, apenas_ativos: bool = True) -> List[Dict]:
        """Lista todos os produtos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT p.*, c.nome as categoria_nome
            FROM produtos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
        '''
        if apenas_ativos:
            query += ' WHERE p.ativo = 1'
        query += ' ORDER BY p.nome'
        
        cursor.execute(query)
        produtos = []
        for row in cursor.fetchall():
            produtos.append({
                'id': row[0],
                'nome': row[1],
                'descricao': row[2],
                'categoria_id': row[3],
                'preco_custo': row[4],
                'preco_venda': row[5],
                'estoque': row[6],
                'estoque_minimo': row[7],
                'imagem_path': row[8],
                'ativo': row[9],
                'data_criacao': row[10],
                'data_atualizacao': row[11],
                'categoria_nome': row[12] if len(row) > 12 else None
            })
        conn.close()
        return produtos
    
    def buscar_produto(self, produto_id: int) -> Optional[Dict]:
        """Busca um produto específico"""
        produtos = self.listar_produtos(apenas_ativos=False)
        for produto in produtos:
            if produto['id'] == produto_id:
                return produto
        return None
    
    def produtos_estoque_baixo(self) -> List[Dict]:
        """Retorna produtos com estoque abaixo do mínimo"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM produtos 
            WHERE estoque <= estoque_minimo AND ativo = 1
            ORDER BY estoque ASC
        ''')
        produtos = []
        for row in cursor.fetchall():
            produtos.append({
                'id': row[0],
                'nome': row[1],
                'estoque': row[6],
                'estoque_minimo': row[7]
            })
        conn.close()
        return produtos
    
    def atualizar_estoque(self, produto_id: int, quantidade: int):
        """Atualiza o estoque de um produto"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE produtos SET estoque = estoque + ?, data_atualizacao = ?
            WHERE id = ?
        ''', (quantidade, datetime.now(), produto_id))
        conn.commit()
        conn.close()
    
    # ==================== VENDAS ====================
    
    def registrar_venda(self, produto_id: int, quantidade: int, cliente: str = "",
                       observacoes: str = "") -> int:
        """Registra uma nova venda e atualiza o estoque"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Buscar preço do produto
        cursor.execute('SELECT preco_venda, estoque FROM produtos WHERE id = ?', (produto_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            raise ValueError("Produto não encontrado")
        
        preco_unitario, estoque_atual = row
        
        if estoque_atual < quantidade:
            conn.close()
            raise ValueError("Estoque insuficiente")
        
        valor_total = preco_unitario * quantidade
        
        # Registrar venda
        cursor.execute('''
            INSERT INTO vendas (produto_id, quantidade, preco_unitario, 
                              valor_total, cliente, observacoes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (produto_id, quantidade, preco_unitario, valor_total, cliente, observacoes))
        
        # Atualizar estoque
        cursor.execute('''
            UPDATE produtos SET estoque = estoque - ?, data_atualizacao = ?
            WHERE id = ?
        ''', (quantidade, datetime.now(), produto_id))
        
        conn.commit()
        venda_id = cursor.lastrowid
        conn.close()
        return venda_id
    
    def listar_vendas(self, data_inicio: str = None, data_fim: str = None) -> List[Dict]:
        """Lista vendas com filtros opcionais"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT v.*, p.nome as produto_nome
            FROM vendas v
            JOIN produtos p ON v.produto_id = p.id
            WHERE 1=1
        '''
        params = []
        
        if data_inicio:
            query += ' AND DATE(v.data_venda) >= ?'
            params.append(data_inicio)
        
        if data_fim:
            query += ' AND DATE(v.data_venda) <= ?'
            params.append(data_fim)
        
        query += ' ORDER BY v.data_venda DESC'
        
        cursor.execute(query, params)
        vendas = []
        for row in cursor.fetchall():
            vendas.append({
                'id': row[0],
                'produto_id': row[1],
                'quantidade': row[2],
                'preco_unitario': row[3],
                'valor_total': row[4],
                'cliente': row[5],
                'data_venda': row[6],
                'observacoes': row[7],
                'produto_nome': row[8]
            })
        conn.close()
        return vendas
    
    def excluir_venda(self, venda_id: int) -> bool:
        """
        Exclui uma venda e devolve o estoque
        Retorna True se bem-sucedido, False caso contrário
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Buscar dados da venda antes de excluir
            cursor.execute('''
                SELECT produto_id, quantidade 
                FROM vendas 
                WHERE id = ?
            ''', (venda_id,))
            
            venda = cursor.fetchone()
            if not venda:
                conn.close()
                return False
            
            produto_id, quantidade = venda
            
            # Devolver o estoque ao produto
            cursor.execute('''
                UPDATE produtos 
                SET estoque = estoque + ?, 
                    data_atualizacao = ?
                WHERE id = ?
            ''', (quantidade, datetime.now(), produto_id))
            
            # Excluir a venda
            cursor.execute('DELETE FROM vendas WHERE id = ?', (venda_id,))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            conn.rollback()
            conn.close()
            print(f"Erro ao excluir venda: {e}")
            return False
    
    # ==================== DESPESAS ====================
    
    def adicionar_despesa(self, descricao: str, valor: float, categoria: str,
                         data_despesa: str, observacoes: str = "") -> int:
        """Adiciona uma nova despesa"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO despesas (descricao, valor, categoria, data_despesa, observacoes)
            VALUES (?, ?, ?, ?, ?)
        ''', (descricao, valor, categoria, data_despesa, observacoes))
        conn.commit()
        despesa_id = cursor.lastrowid
        conn.close()
        return despesa_id
    
    def listar_despesas(self, data_inicio: str = None, data_fim: str = None) -> List[Dict]:
        """Lista despesas com filtros opcionais"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM despesas WHERE 1=1'
        params = []
        
        if data_inicio:
            query += ' AND data_despesa >= ?'
            params.append(data_inicio)
        
        if data_fim:
            query += ' AND data_despesa <= ?'
            params.append(data_fim)
        
        query += ' ORDER BY data_despesa DESC'
        
        cursor.execute(query, params)
        despesas = []
        for row in cursor.fetchall():
            despesas.append({
                'id': row[0],
                'descricao': row[1],
                'valor': row[2],
                'categoria': row[3],
                'data_despesa': row[4],
                'data_registro': row[5],
                'observacoes': row[6]
            })
        conn.close()
        return despesas
    
    def remover_despesa(self, despesa_id: int):
        """Remove uma despesa"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM despesas WHERE id = ?', (despesa_id,))
        conn.commit()
        conn.close()
    
    # ==================== RELATÓRIOS E ESTATÍSTICAS ====================
    
    def get_resumo_vendas(self, data_inicio: str = None, data_fim: str = None) -> Dict:
        """Retorna resumo das vendas em um período"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT SUM(valor_total), COUNT(*), AVG(valor_total) FROM vendas WHERE 1=1'
        params = []
        
        if data_inicio:
            query += ' AND DATE(data_venda) >= ?'
            params.append(data_inicio)
        
        if data_fim:
            query += ' AND DATE(data_venda) <= ?'
            params.append(data_fim)
        
        cursor.execute(query, params)
        row = cursor.fetchone()
        
        resumo = {
            'receita_total': row[0] if row[0] else 0,
            'total_vendas': row[1] if row[1] else 0,
            'ticket_medio': row[2] if row[2] else 0
        }
        
        conn.close()
        return resumo
    
    def get_lucro_periodo(self, data_inicio: str = None, data_fim: str = None) -> Dict:
        """Calcula lucro líquido em um período"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Calcular lucro de vendas (preço venda - preço custo)
        query = '''
            SELECT SUM((v.preco_unitario - p.preco_custo) * v.quantidade)
            FROM vendas v
            JOIN produtos p ON v.produto_id = p.id
            WHERE 1=1
        '''
        params = []
        
        if data_inicio:
            query += ' AND DATE(v.data_venda) >= ?'
            params.append(data_inicio)
        
        if data_fim:
            query += ' AND DATE(v.data_venda) <= ?'
            params.append(data_fim)
        
        cursor.execute(query, params)
        lucro_bruto = cursor.fetchone()[0] or 0
        
        # Calcular despesas
        query_despesas = 'SELECT SUM(valor) FROM despesas WHERE 1=1'
        params_despesas = []
        
        if data_inicio:
            query_despesas += ' AND data_despesa >= ?'
            params_despesas.append(data_inicio)
        
        if data_fim:
            query_despesas += ' AND data_despesa <= ?'
            params_despesas.append(data_fim)
        
        cursor.execute(query_despesas, params_despesas)
        total_despesas = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'lucro_bruto': lucro_bruto,
            'despesas': total_despesas,
            'lucro_liquido': lucro_bruto - total_despesas
        }
    
    def get_produtos_mais_vendidos(self, limite: int = 10) -> List[Dict]:
        """Retorna os produtos mais vendidos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.nome, SUM(v.quantidade) as total_vendido, 
                   SUM(v.valor_total) as receita_total
            FROM vendas v
            JOIN produtos p ON v.produto_id = p.id
            GROUP BY v.produto_id
            ORDER BY total_vendido DESC
            LIMIT ?
        ''', (limite,))
        
        produtos = []
        for row in cursor.fetchall():
            produtos.append({
                'nome': row[0],
                'quantidade_vendida': row[1],
                'receita_total': row[2]
            })
        
        conn.close()
        return produtos
    
    def get_valor_estoque_total(self) -> float:
        """Calcula o valor total do estoque"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT SUM(preco_custo * estoque)
            FROM produtos
            WHERE ativo = 1
        ''')
        valor = cursor.fetchone()[0] or 0
        conn.close()
        return valor
    
    # ==================== CONFIGURAÇÕES ====================
    
    def get_config(self, chave: str) -> Optional[str]:
        """Obtém uma configuração"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT valor FROM configuracoes WHERE chave = ?', (chave,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None
    
    def set_config(self, chave: str, valor: str):
        """Define uma configuração"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO configuracoes (chave, valor, data_atualizacao)
            VALUES (?, ?, ?)
        ''', (chave, valor, datetime.now()))
        conn.commit()
        conn.close()
    
    # ==================== METAS ====================
    
    def adicionar_meta(self, tipo: str, valor_meta: float, periodo: str,
                      data_inicio: str, data_fim: str) -> int:
        """Adiciona uma nova meta"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO metas (tipo, valor_meta, periodo, data_inicio, data_fim)
            VALUES (?, ?, ?, ?, ?)
        ''', (tipo, valor_meta, periodo, data_inicio, data_fim))
        conn.commit()
        meta_id = cursor.lastrowid
        conn.close()
        return meta_id
    
    def listar_metas(self, apenas_ativas: bool = True) -> List[Dict]:
        """Lista metas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM metas'
        if apenas_ativas:
            query += ' WHERE ativo = 1'
        query += ' ORDER BY data_criacao DESC'
        
        cursor.execute(query)
        metas = []
        for row in cursor.fetchall():
            metas.append({
                'id': row[0],
                'tipo': row[1],
                'valor_meta': row[2],
                'periodo': row[3],
                'data_inicio': row[4],
                'data_fim': row[5],
                'ativo': row[6],
                'data_criacao': row[7]
            })
        conn.close()
        return metas
    
    def desativar_meta(self, meta_id: int):
        """Desativa uma meta"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE metas SET ativo = 0 WHERE id = ?', (meta_id,))
        conn.commit()
        conn.close()
    
    def progresso_meta(self, meta_id: int) -> Dict:
        """Calcula progresso de uma meta"""
        metas = self.listar_metas(apenas_ativas=False)
        meta = next((m for m in metas if m['id'] == meta_id), None)
        
        if not meta:
            return {}
        
        data_inicio = meta['data_inicio']
        data_fim = meta['data_fim']
        
        if meta['tipo'] == 'RECEITA':
            resumo = self.get_resumo_vendas(data_inicio, data_fim)
            valor_atual = resumo['receita_total']
        elif meta['tipo'] == 'LUCRO':
            lucro_data = self.get_lucro_periodo(data_inicio, data_fim)
            valor_atual = lucro_data['lucro_liquido']
        elif meta['tipo'] == 'VENDAS':
            resumo = self.get_resumo_vendas(data_inicio, data_fim)
            valor_atual = resumo['total_vendas']
        else:
            valor_atual = 0
        
        valor_meta = meta['valor_meta']
        percentual = (valor_atual / valor_meta * 100) if valor_meta > 0 else 0
        
        return {
            'meta': meta,
            'valor_atual': valor_atual,
            'valor_meta': valor_meta,
            'percentual': percentual,
            'atingido': valor_atual >= valor_meta,
            'falta': max(0, valor_meta - valor_atual)
        }
