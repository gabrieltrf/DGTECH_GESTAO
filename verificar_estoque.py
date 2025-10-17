"""
Script para verificar o cálculo de capital em estoque
"""

import sqlite3

def verificar_estoque():
    conn = sqlite3.connect('gestao_vendas.db')
    cursor = conn.cursor()
    
    # Buscar todos os produtos com estoque
    cursor.execute('''
        SELECT 
            id,
            nome,
            preco_custo,
            estoque,
            (preco_custo * estoque) as valor_investido,
            ativo
        FROM produtos
        ORDER BY ativo DESC, nome
    ''')
    
    produtos = cursor.fetchall()
    
    print("=" * 100)
    print("📊 VERIFICAÇÃO DE CAPITAL EM ESTOQUE")
    print("=" * 100)
    print()
    
    total_geral = 0
    total_ativos = 0
    total_inativos = 0
    
    print("🟢 PRODUTOS ATIVOS:")
    print("-" * 100)
    print(f"{'ID':<5} {'Nome':<30} {'Preço Custo':<15} {'Estoque':<10} {'Valor Investido':<20} {'Status':<10}")
    print("-" * 100)
    
    for produto in produtos:
        id_prod, nome, preco_custo, estoque, valor_investido, ativo = produto
        status = "✅ Ativo" if ativo == 1 else "❌ Inativo"
        
        if ativo == 1 and estoque > 0:
            print(f"{id_prod:<5} {nome:<30} R$ {preco_custo:<12.2f} {estoque:<10} R$ {valor_investido:<17.2f} {status}")
            total_ativos += valor_investido
        
        if estoque > 0:
            total_geral += valor_investido
            if ativo == 0:
                total_inativos += valor_investido
    
    print("-" * 100)
    print(f"{'SUBTOTAL ATIVOS:':<47} {'':>28} R$ {total_ativos:>17.2f}")
    print()
    
    # Produtos inativos com estoque
    produtos_inativos = [p for p in produtos if p[5] == 0 and p[3] > 0]
    if produtos_inativos:
        print()
        print("🔴 PRODUTOS INATIVOS COM ESTOQUE:")
        print("-" * 100)
        for produto in produtos_inativos:
            id_prod, nome, preco_custo, estoque, valor_investido, ativo = produto
            print(f"{id_prod:<5} {nome:<30} R$ {preco_custo:<12.2f} {estoque:<10} R$ {valor_investido:<17.2f} ❌ Inativo")
        
        print("-" * 100)
        print(f"{'SUBTOTAL INATIVOS:':<47} {'':>28} R$ {total_inativos:>17.2f}")
    
    print()
    print("=" * 100)
    print(f"{'💰 TOTAL CAPITAL EM ESTOQUE (TODOS):':<47} {'':>28} R$ {total_geral:>17.2f}")
    print(f"{'   • Apenas Ativos:':<47} {'':>28} R$ {total_ativos:>17.2f}")
    if total_inativos > 0:
        print(f"{'   • Apenas Inativos:':<47} {'':>28} R$ {total_inativos:>17.2f}")
    print("=" * 100)
    print()
    
    # Verificar se o valor esperado está correto
    valor_esperado = 623.00
    diferenca = abs(valor_esperado - total_geral)
    
    if diferenca < 0.01:
        print(f"✅ CORRETO! O valor calculado (R$ {total_geral:.2f}) corresponde ao esperado (R$ {valor_esperado:.2f})")
    else:
        print(f"⚠️ ATENÇÃO! Diferença encontrada:")
        print(f"   • Valor esperado: R$ {valor_esperado:.2f}")
        print(f"   • Valor calculado: R$ {total_geral:.2f}")
        print(f"   • Diferença: R$ {diferenca:.2f}")
        print()
        print("💡 Possíveis causas:")
        print("   1. Produtos inativos não foram incluídos no cálculo anterior")
        print("   2. Algum produto foi editado recentemente")
        print("   3. Existe alguma venda não contabilizada no estoque")
    
    print()
    
    conn.close()

if __name__ == "__main__":
    try:
        verificar_estoque()
    except Exception as e:
        print(f"❌ Erro ao verificar estoque: {str(e)}")
        import traceback
        traceback.print_exc()
