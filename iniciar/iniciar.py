"""
Script de inicialização rápida do DGTECH GESTÃO
Execute este arquivo para iniciar o sistema
"""

import subprocess
import sys
import os

def iniciar_sistema():
    print("=" * 50)
    print("  DGTECH GESTÃO - Sistema de Vendas")
    print("=" * 50)
    print()
    
    # Caminho do Python do ambiente virtual
    venv_python = os.path.join(".venv", "Scripts", "python.exe")
    
    # Verificar se existe
    if not os.path.exists(venv_python):
        print("❌ Ambiente virtual não encontrado!")
        print("Execute primeiro: python -m venv .venv")
        print("Depois: .venv\\Scripts\\pip install -r requirements.txt")
        input("\nPressione Enter para sair...")
        sys.exit(1)
    
    # Executar main.py
    try:
        subprocess.run([venv_python, "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro ao executar o sistema: {e}")
        input("\nPressione Enter para sair...")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n✅ Sistema encerrado pelo usuário.")
        sys.exit(0)

if __name__ == "__main__":
    iniciar_sistema()
