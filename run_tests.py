#!/usr/bin/env python3
"""
Script para executar todos os testes do projeto Fin-Assist
"""

import unittest
import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_tests():
    """Executa todos os testes"""
    # Descobre e executa todos os testes
    loader = unittest.TestLoader()
    start_dir = project_root / 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Executa os testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Retorna código de saída baseado no resultado
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    print("=" * 60)
    print("Executando testes do Fin-Assist")
    print("=" * 60)
    
    exit_code = run_tests()
    
    print("\n" + "=" * 60)
    if exit_code == 0:
        print("✅ Todos os testes passaram!")
    else:
        print("❌ Alguns testes falharam!")
    print("=" * 60)
    
    sys.exit(exit_code)
