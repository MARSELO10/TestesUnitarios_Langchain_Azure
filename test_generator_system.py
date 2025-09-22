#!/usr/bin/env python3
"""
Sistema de Geração de Testes Unitários com LangChain e Azure ChatGPT
Versão simplificada e funcional

Autor: Edson Gomes
Email: edsgom@gmail.com
Bootcamp: DIO + BairesDev Machine Learning
Data: Janeiro 2025
"""

import os
import sys
import json
import logging
import ast
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
import argparse
from dotenv import load_dotenv

# Configuração básica de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SimulatedLLM:
    """LLM simulado para demonstração quando Azure não está configurado."""
    
    def __init__(self):
        self.temperature = 0.1
    
    def invoke(self, prompt):
        """Simula uma resposta do LLM."""
        # Analisa o código no prompt para gerar testes relevantes
        if "def " in prompt or "class " in prompt:
            return self._generate_mock_tests(prompt)
        return "# Testes simulados - Configure Azure OpenAI para funcionalidade completa"
    
    def _generate_mock_tests(self, prompt):
        """Gera testes simulados baseados no código fornecido."""
        test_template = '''import pytest
import unittest
from unittest.mock import Mock, patch

# Testes gerados automaticamente (SIMULAÇÃO)
# Configure Azure OpenAI para geração real de testes

"""
Este é um exemplo de como os testes seriam gerados.
Para funcionalidade completa, configure:
- AZURE_OPENAI_API_KEY
- AZURE_OPENAI_ENDPOINT 
- AZURE_OPENAI_DEPLOYMENT_NAME
"""

class TestGeneratedCode:
    """Classe de teste gerada automaticamente."""
    
    def setup_method(self):
        """Configuração inicial dos testes."""
        pass
    
    def test_basic_functionality(self):
        """Teste básico de funcionalidade."""
        # Este seria um teste real gerado pela IA
        assert True
    
    def test_edge_cases(self):
        """Teste de casos extremos."""
        # Casos de borda seriam testados aqui
        assert True
    
    def test_error_conditions(self):
        """Teste de condições de erro."""
        # Testes de exceções seriam gerados aqui
        with pytest.raises(Exception):
            # Código que deve gerar exceção
            pass

# Testes parametrizados seriam gerados automaticamente
@pytest.mark.parametrize("input_val,expected", [
    (1, 1),
    (2, 2),
    (3, 3),
])
def test_parametrized_function(input_val, expected):
    """Teste parametrizado de exemplo."""
    assert input_val == expected

if __name__ == "__main__":
    pytest.main([__file__])
'''
        return test_template

class ConfigManager:
    """Gerenciador de configurações simplificado."""
    
    def __init__(self):
        """Inicializa configurações."""
        load_dotenv()
        
        self.azure_config = {
            'api_key': os.getenv('AZURE_OPENAI_API_KEY', ''),
            'endpoint': os.getenv('AZURE_OPENAI_ENDPOINT', ''),
            'api_version': os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-01'),
            'deployment_name': os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', 'gpt-4'),
            'temperature': float(os.getenv('TEMPERATURE', '0.1')),
            'max_tokens': int(os.getenv('MAX_TOKENS', '2000'))
        }
        
        self.test_config = {
            'framework': os.getenv('TEST_FRAMEWORK', 'pytest'),
            'include_fixtures': os.getenv('INCLUDE_FIXTURES', 'true').lower() == 'true',
            'test_edge_cases': os.getenv('TEST_EDGE_CASES', 'true').lower() == 'true',
            'min_coverage': int(os.getenv('MIN_COVERAGE', '80'))
        }
        
        self.system_config = {
            'output_directory': os.getenv('OUTPUT_DIRECTORY', 'generated_tests'),
            'log_level': os.getenv('LOG_LEVEL', 'INFO'),
            'debug_mode': os.getenv('DEBUG_MODE', 'false').lower() == 'true'
        }
        
        # Verificar se está em modo simulação
        self.simulate_mode = not (self.azure_config['api_key'] and 
                                 self.azure_config['endpoint'] and
                                 self.azure_config['api_key'] != 'sua_chave_azure_aqui')
    
    def create_directories(self):
        """Cria diretórios necessários."""
        Path(self.system_config['output_directory']).mkdir(exist_ok=True)
        Path('logs').mkdir(exist_ok=True)
        Path('metrics').mkdir(exist_ok=True)
    
    def get_config_summary(self):
        """Retorna resumo das configurações."""
        return f"""
Configurações do Sistema
=======================
Modo: {'Simulação' if self.simulate_mode else 'Azure OpenAI'}
Framework: {self.test_config['framework']}
Cobertura Mínima: {self.test_config['min_coverage']}%
Diretório de Saída: {self.system_config['output_directory']}
Debug: {self.system_config['debug_mode']}
"""

class CodeAnalyzer:
    """Analisador de código Python."""
    
    def __init__(self):
        """Inicializa o analisador."""
        pass
    
    def analyze_code(self, source_code: str) -> Dict[str, Any]:
        """Analisa código Python e extrai informações."""
        try:
            tree = ast.parse(source_code)
            
            functions = []
            classes = []
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        'name': node.name,
                        'parameters': [arg.arg for arg in node.args.args],
                        'line': node.lineno,
                        'is_async': isinstance(node, ast.AsyncFunctionDef)
                    })
                elif isinstance(node, ast.ClassDef):
                    methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    classes.append({
                        'name': node.name,
                        'methods': methods,
                        'line': node.lineno
                    })
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        imports.extend([alias.name for alias in node.names])
                    else:
                        module = node.module or ''
                        imports.extend([f"{module}.{alias.name}" for alias in node.names])
            
            statistics = {
                'total_functions': len(functions),
                'total_classes': len(classes),
                'total_methods': sum(len(cls['methods']) for cls in classes),
                'total_lines': len(source_code.splitlines()),
                'complexity': self._calculate_complexity(tree)
            }
            
            return {
                'functions': functions,
                'classes': classes,
                'imports': imports,
                'statistics': statistics,
                'recommendations': self._generate_recommendations(statistics)
            }
            
        except SyntaxError as e:
            return {'error': f'Erro de sintaxe: {e}'}
        except Exception as e:
            return {'error': f'Erro na análise: {e}'}
    
    def _calculate_complexity(self, tree) -> int:
        """Calcula complexidade ciclomática básica."""
        complexity = 1  # Complexidade base
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, (ast.ExceptHandler, ast.With, ast.AsyncWith)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity
    
    def _generate_recommendations(self, stats: Dict) -> List[str]:
        """Gera recomendações baseadas nas estatísticas."""
        recommendations = []
        
        if stats['complexity'] > 15:
            recommendations.append("Considere refatorar - complexidade alta detectada")
        
        if stats['total_functions'] == 0 and stats['total_classes'] == 0:
            recommendations.append("Nenhuma função ou classe encontrada para testar")
        
        if stats['total_functions'] > 10:
            recommendations.append("Muitas funções - considere organizar em classes")
        
        return recommendations

def quick_analyze(source_code: str) -> Dict[str, Any]:
    """Análise rápida de código."""
    try:
        tree = ast.parse(source_code)
        functions = len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)])
        classes = len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])
        return {'functions': functions, 'classes': classes}
    except:
        return {'error': 'Código inválido'}

class TestValidator:
    """Validador de testes gerados."""
    
    def __init__(self):
        """Inicializa o validador."""
        pass
    
    def validate_test_code(self, test_code: str) -> Dict[str, Any]:
        """Valida código de teste."""
        try:
            tree = ast.parse(test_code)
            
            test_functions = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                    test_functions.append(node.name)
            
            return {
                'is_valid': True,
                'test_count': len(test_functions),
                'test_functions': test_functions,
                'coverage_score': min(len(test_functions) * 10, 100),
                'issues': []
            }
        except Exception as e:
            return {
                'is_valid': False,
                'error': str(e),
                'test_count': 0,
                'coverage_score': 0
            }

class TestGeneratorAgent:
    """Agente principal para geração de testes."""
    
    def __init__(self, config_manager: ConfigManager):
        """Inicializa o agente."""
        self.config = config_manager
        self.analyzer = CodeAnalyzer()
        self.validator = TestValidator()
        
        if self.config.simulate_mode:
            self.llm = SimulatedLLM()
            logger.info("Modo simulação ativado")
        else:
            try:
                from langchain_openai import AzureChatOpenAI
                self.llm = AzureChatOpenAI(**self.config.azure_config)
                logger.info("Azure OpenAI configurado")
            except ImportError:
                logger.warning("LangChain não instalado, usando simulação")
                self.llm = SimulatedLLM()
                self.config.simulate_mode = True
    
    def generate_tests(self, source_code: str) -> Dict[str, Any]:
        """Gera testes para código fornecido."""
        try:
            # Analisar código
            code_analysis = self.analyzer.analyze_code(source_code)
            
            if 'error' in code_analysis:
                return {
                    'success': False,
                    'error': code_analysis['error']
                }
            
            # Gerar prompt
            prompt = self._create_generation_prompt(source_code, code_analysis)
            
            # Gerar testes
            test_code = self.llm.invoke(prompt)
            
            # Validar testes
            validation = self.validator.validate_test_code(test_code)
            
            return {
                'success': True,
                'test_code': test_code,
                'code_analysis': code_analysis,
                'validation': validation,
                'simulate_mode': self.config.simulate_mode
            }
            
        except Exception as e:
            logger.error(f"Erro na geração de testes: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _create_generation_prompt(self, source_code: str, analysis: Dict) -> str:
        """Cria prompt para geração de testes."""
        stats = analysis['statistics']
        
        prompt = f"""
Você é um especialista em testes unitários Python. Analise o código fornecido e gere testes completos usando {self.config.test_config['framework']}.

CÓDIGO A TESTAR:
{source_code}

ESTATÍSTICAS:
- Funções: {stats['total_functions']}
- Classes: {stats['total_classes']}
- Complexidade: {stats['complexity']}

REQUISITOS:
1. Use {self.config.test_config['framework']} como framework
2. Inclua testes para casos normais e extremos
3. Teste tratamento de exceções
4. Adicione fixtures se necessário
5. Use parametrização quando apropriado
6. Cobertura mínima: {self.config.test_config['min_coverage']}%

GERE TESTES COMPLETOS E FUNCIONAIS:
"""
        return prompt
    
    def batch_generate_tests(self, code_files: List[tuple]) -> Dict[str, Any]:
        """Gera testes para múltiplos arquivos."""
        results = []
        successful = 0
        failed = 0
        start_time = datetime.now()
        
        for file_path, source_code in code_files:
            logger.info(f"Processando: {file_path}")
            
            result = self.generate_tests(source_code)
            result['file_path'] = file_path
            results.append(result)
            
            if result['success']:
                successful += 1
            else:
                failed += 1
        
        total_time = (datetime.now() - start_time).total_seconds()
        
        return {
            'results': results,
            'summary': {
                'total_files': len(code_files),
                'successful': successful,
                'failed': failed,
                'total_execution_time': total_time
            }
        }
    
    def improve_existing_tests(self, test_code: str, original_code: str) -> Dict[str, Any]:
        """Melhora testes existentes."""
        try:
            # Analisar código original e testes atuais
            code_analysis = self.analyzer.analyze_code(original_code)
            test_validation = self.validator.validate_test_code(test_code)
            
            # Criar prompt para melhoria
            prompt = f"""
Analise os testes existentes e o código original. Melhore os testes adicionando:
1. Casos de teste ausentes
2. Melhor cobertura
3. Testes de edge cases
4. Correção de problemas

CÓDIGO ORIGINAL:
{original_code}

TESTES ATUAIS:
{test_code}

GERE VERSÃO MELHORADA DOS TESTES:
"""
            
            improved_tests = self.llm.invoke(prompt)
            new_validation = self.validator.validate_test_code(improved_tests)
            
            return {
                'success': True,
                'improved_tests': improved_tests,
                'improvements': {
                    'coverage_improvement': new_validation['coverage_score'] - test_validation['coverage_score'],
                    'new_test_count': new_validation['test_count'] - test_validation['test_count'],
                    'issues_resolved': len(test_validation.get('issues', []))
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

class TestGeneratorCLI:
    """Interface de linha de comando principal."""
    
    def __init__(self):
        """Inicializa a CLI."""
        self.config_manager = ConfigManager()
        self.agent = TestGeneratorAgent(self.config_manager)
        self.statistics = {
            'total_generations': 0,
            'successful_generations': 0,
            'failed_generations': 0,
            'start_time': datetime.now()
        }
        
        # Criar diretórios
        self.config_manager.create_directories()
    
    def display_banner(self):
        """Exibe banner do sistema."""
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                     SISTEMA DE GERAÇÃO DE TESTES UNITÁRIOS                  ║
║                          LangChain + Azure ChatGPT                          ║
║                                                                              ║
║  Desenvolvido por: Edson Gomes                                              ║
║  Bootcamp: DIO + BairesDev Machine Learning                                 ║
║  GitHub: @edsongom1                                                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
        
        if self.config_manager.simulate_mode:
            print("⚠️  MODO SIMULAÇÃO ATIVO")
            print("   Configure as variáveis Azure OpenAI para usar o modo completo")
        
        print()
    
    def display_main_menu(self):
        """Exibe menu principal."""
        print("OPÇÕES DISPONÍVEIS:")
        print("─" * 50)
        print("1. 📝 Gerar testes para código Python")
        print("2. 📁 Processar arquivo(s) de código")
        print("3. 🔍 Analisar código (sem gerar testes)")
        print("4. ✨ Melhorar testes existentes")
        print("5. ⚙️  Configurações do sistema")
        print("6. 📊 Estatísticas e relatórios")
        print("7. 🧪 Executar exemplo de demonstração")
        print("8. ❓ Ajuda e documentação")
        print("9. 🚪 Sair")
        print()
    
    def get_user_choice(self, max_option: int = 9) -> int:
        """Obtém escolha do usuário."""
        while True:
            try:
                choice = input(f"Escolha uma opção (1-{max_option}): ").strip()
                choice_int = int(choice)
                if 1 <= choice_int <= max_option:
                    return choice_int
                else:
                    print(f"❌ Por favor, escolha um número entre 1 e {max_option}")
            except ValueError:
                print("❌ Por favor, digite um número válido")
            except KeyboardInterrupt:
                print("\n\n👋 Programa interrompido pelo usuário")
                sys.exit(0)
    
    def run(self):
        """Executa o loop principal da CLI."""
        self.display_banner()
        
        while True:
            self.display_main_menu()
            choice = self.get_user_choice(9)
            
            if choice == 1:
                self.generate_tests_interactive()
            elif choice == 2:
                self.process_files()
            elif choice == 3:
                self.analyze_code_only()
            elif choice == 4:
                self.improve_existing_tests()
            elif choice == 5:
                self.show_system_configuration()
            elif choice == 6:
                self.show_statistics()
            elif choice == 7:
                self.run_demonstration()
            elif choice == 8:
                self.show_help()
            elif choice == 9:
                self._safe_exit()
                break
    
    def generate_tests_interactive(self):
        """Gera testes de forma interativa."""
        print("\n" + "=" * 60)
        print("📝 GERAÇÃO DE TESTES INTERATIVA")
        print("=" * 60)
        
        print("\nCole ou digite seu código Python abaixo.")
        print("Para finalizar a entrada, digite 'END' em uma linha separada:")
        print("─" * 40)
        
        code_lines = []
        while True:
            try:
                line = input()
                if line.strip().upper() == 'END':
                    break
                code_lines.append(line)
            except KeyboardInterrupt:
                print("\n❌ Entrada cancelada pelo usuário")
                return
        
        source_code = '\n'.join(code_lines).strip()
        
        if not source_code:
            print("❌ Nenhum código fornecido")
            return
        
        # Análise rápida
        quick_stats = quick_analyze(source_code)
        if 'error' in quick_stats:
            print("❌ Código com erro de sintaxe")
            return
        
        print(f"\n🔍 Código analisado: {quick_stats['functions']} funções, {quick_stats['classes']} classes")
        
        # Confirmar geração
        confirm = input("Continuar com a geração de testes? (S/n): ").strip().lower()
        if confirm in ['n', 'no', 'não']:
            print("❌ Geração cancelada")
            return
        
        print("\n🔄 Gerando testes...")
        self._process_code_generation(source_code)
    
    def process_files(self):
        """Processa arquivos de código."""
        print("\n" + "=" * 60)
        print("📁 PROCESSAMENTO DE ARQUIVOS")
        print("=" * 60)
        
        print("\nOpções:")
        print("1. Processar arquivo único")
        print("2. Processar diretório")
        print("3. Voltar ao menu principal")
        
        choice = self.get_user_choice(3)
        
        if choice == 1:
            self._process_single_file()
        elif choice == 2:
            self._process_directory()
    
    def _process_single_file(self):
        """Processa um arquivo único."""
        file_path = input("\n📄 Caminho do arquivo Python (.py): ").strip()
        
        if not file_path:
            print("❌ Caminho não fornecido")
            return
        
        path = Path(file_path)
        
        if not path.exists():
            print(f"❌ Arquivo não encontrado: {file_path}")
            return
        
        if not path.suffix == '.py':
            print("❌ Arquivo deve ter extensão .py")
            return
        
        try:
            source_code = path.read_text(encoding='utf-8')
            print(f"✅ Arquivo carregado: {path.name}")
            
            self._process_code_generation(source_code, path.stem)
            
        except Exception as e:
            print(f"❌ Erro ao ler arquivo: {e}")
    
    def _process_directory(self):
        """Processa diretório com arquivos Python."""
        dir_path = input("\n📁 Caminho do diretório: ").strip()
        
        if not dir_path:
            print("❌ Caminho não fornecido")
            return
        
        path = Path(dir_path)
        
        if not path.exists() or not path.is_dir():
            print(f"❌ Diretório não encontrado: {dir_path}")
            return
        
        # Encontrar arquivos Python
        py_files = list(path.glob("**/*.py"))
        
        if not py_files:
            print("❌ Nenhum arquivo Python encontrado")
            return
        
        print(f"📄 Encontrados {len(py_files)} arquivo(s) Python:")
        for i, file in enumerate(py_files[:10], 1):
            print(f"  {i}. {file.name}")
        
        if len(py_files) > 10:
            print(f"  ... e mais {len(py_files) - 10} arquivo(s)")
        
        confirm = input(f"\nProcessar {len(py_files)} arquivo(s)? (S/n): ").strip().lower()
        if confirm in ['n', 'no', 'não']:
            return
        
        # Processar em lote
        code_files = []
        for file_path in py_files:
            try:
                source_code = file_path.read_text(encoding='utf-8')
                code_files.append((str(file_path), source_code))
            except Exception as e:
                print(f"⚠️  Erro ao ler {file_path.name}: {e}")
        
        if code_files:
            print(f"\n🔄 Processando {len(code_files)} arquivo(s)...")
            self._process_batch_generation(code_files)
    
    def _process_code_generation(self, source_code: str, filename: Optional[str] = None):
        """Processa geração de testes para código."""
        start_time = datetime.now()
        
        try:
            result = self.agent.generate_tests(source_code)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            print(f"\n{'✅' if result['success'] else '❌'} Geração {'concluída' if result['success'] else 'falhou'}")
            print(f"⏱️  Tempo de execução: {execution_time:.2f}s")
            
            if result['success']:
                # Mostrar estatísticas
                stats = result['code_analysis'].get('statistics', {})
                validation = result['validation']
                
                print(f"📊 Estatísticas:")
                print(f"   Funções: {stats.get('total_functions', 0)}")
                print(f"   Classes: {stats.get('total_classes', 0)}")
                print(f"   Testes gerados: {validation.get('test_count', 0)}")
                print(f"   Cobertura estimada: {validation.get('coverage_score', 0):.1f}%")
                
                # Mostrar código dos testes
                self._display_generated_tests(result['test_code'])
                
                # Opção de salvar
                self._offer_save_tests(result['test_code'], filename)
                
                self.statistics['successful_generations'] += 1
            else:
                print(f"💥 Erro: {result['error']}")
                self.statistics['failed_generations'] += 1
                
            self.statistics['total_generations'] += 1
            
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            self.statistics['failed_generations'] += 1
            self.statistics['total_generations'] += 1
    
    def _process_batch_generation(self, code_files: List[tuple]):
        """Processa geração em lote."""
        try:
            batch_result = self.agent.batch_generate_tests(code_files)
            
            summary = batch_result['summary']
            print(f"\n📊 RESULTADO DO PROCESSAMENTO EM LOTE")
            print(f"=" * 50)
            print(f"Total de arquivos: {summary['total_files']}")
            print(f"Sucessos: {summary['successful']}")
            print(f"Falhas: {summary['failed']}")
            print(f"Tempo total: {summary['total_execution_time']:.2f}s")
            
            # Atualizar estatísticas
            self.statistics['successful_generations'] += summary['successful']
            self.statistics['failed_generations'] += summary['failed']
            self.statistics['total_generations'] += summary['total_files']
            
        except Exception as e:
            print(f"❌ Erro no processamento em lote: {e}")
    
    def analyze_code_only(self):
        """Analisa código sem gerar testes."""
        print("\n" + "=" * 60)
        print("🔍 ANÁLISE DE CÓDIGO")
        print("=" * 60)
        
        print("\nCole seu código Python abaixo (digite 'END' para finalizar):")
        
        code_lines = []
        while True:
            try:
                line = input()
                if line.strip().upper() == 'END':
                    break
                code_lines.append(line)
            except KeyboardInterrupt:
                print("\n❌ Análise cancelada")
                return
        
        source_code = '\n'.join(code_lines).strip()
        
        if not source_code:
            print("❌ Nenhum código fornecido")
            return
        
        try:
            analyzer = CodeAnalyzer()
            analysis = analyzer.analyze_code(source_code)
            
            if 'error' in analysis:
                print(f"❌ Erro na análise: {analysis['error']}")
                return
            
            self._display_code_analysis(analysis)
            
        except Exception as e:
            print(f"❌ Erro inesperado na análise: {e}")
    
    def improve_existing_tests(self):
        """Melhora testes existentes."""
        print("\n" + "=" * 60)
        print("✨ MELHORIA DE TESTES EXISTENTES")
        print("=" * 60)
        
        print("\nEsta funcionalidade requer código original e testes existentes.")
        print("Cole o código original primeiro (digite 'END' para finalizar):")
        
        original_lines = []
        while True:
            try:
                line = input()
                if line.strip().upper() == 'END':
                    break
                original_lines.append(line)
            except KeyboardInterrupt:
                print("\n❌ Melhoria cancelada")
                return
        
        original_code = '\n'.join(original_lines).strip()
        
        if not original_code:
            print("❌ Nenhum código original fornecido")
            return
        
        print("\nAgora cole os testes existentes (digite 'END' para finalizar):")
        
        test_lines = []
        while True:
            try:
                line = input()
                if line.strip().upper() == 'END':
                    break
                test_lines.append(line)
            except KeyboardInterrupt:
                print("\n❌ Melhoria cancelada")
                return
        
        test_code = '\n'.join(test_lines).strip()
        
        if not test_code:
            print("❌ Nenhum código de teste fornecido")
            return
        
        self._process_test_improvement(test_code, original_code)
    
    def _process_test_improvement(self, test_code: str, original_code: str):
        """Processa melhoria de testes."""
        print("\n🔄 Processando melhoria de testes...")
        
        try:
            result = self.agent.improve_existing_tests(test_code, original_code)
            
            if result['success']:
                print("✅ Testes melhorados com sucesso!")
                
                improvements = result['improvements']
                print(f"\n📈 Melhorias:")
                print(f"  Cobertura: +{improvements['coverage_improvement']:.1f}%")
                print(f"  Problemas resolvidos: {improvements['issues_resolved']}")
                print(f"  Novos testes: {improvements['new_test_count']}")
                
                # Mostrar testes melhorados
                self._display_generated_tests(result['improved_tests'])
                
                # Opção de salvar
                self._offer_save_tests(result['improved_tests'], "improved_tests")
                
            else:
                print(f"❌ Erro na melhoria: {result['error']}")
                
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
    
    def show_system_configuration(self):
        """Mostra configurações do sistema."""
        print("\n" + "=" * 60)
        print("⚙️ CONFIGURAÇÕES DO SISTEMA")
        print("=" * 60)
        
        print(self.config_manager.get_config_summary())
        
        if self.config_manager.simulate_mode:
            print("\n🔧 Para ativar Azure OpenAI, configure:")
            print("  - AZURE_OPENAI_API_KEY=sua_chave")
            print("  - AZURE_OPENAI_ENDPOINT=https://seu-recurso.openai.azure.com/")
            print("  - AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4")
    
    def show_statistics(self):
        """Mostra estatísticas e relatórios."""
        print("\n" + "=" * 60)
        print("📊 ESTATÍSTICAS E RELATÓRIOS")
        print("=" * 60)
        
        # Calcular tempo de execução
        runtime = datetime.now() - self.statistics['start_time']
        success_rate = 0
        if self.statistics['total_generations'] > 0:
            success_rate = (self.statistics['successful_generations'] / 
                          self.statistics['total_generations']) * 100
        
        print(f"\n📈 ESTATÍSTICAS GERAIS:")
        print(f"   Tempo de execução: {str(runtime).split('.')[0]}")
        print(f"   Total de gerações: {self.statistics['total_generations']}")
        print(f"   Gerações bem-sucedidas: {self.statistics['successful_generations']}")
        print(f"   Gerações falharam: {self.statistics['failed_generations']}")
        print(f"   Taxa de sucesso: {success_rate:.1f}%")
    
    def run_demonstration(self):
        """Executa exemplo de demonstração."""
        print("\n" + "=" * 60)
        print("🧪 DEMONSTRAÇÃO DO SISTEMA")
        print("=" * 60)
        
        demo_code = '''def calcular_area_retangulo(largura, altura):
    """Calcula a área de um retângulo."""
    if largura <= 0 or altura <= 0:
        raise ValueError("Largura e altura devem ser positivas")
    return largura * altura

def calcular_perimetro_retangulo(largura, altura):
    """Calcula o perímetro de um retângulo."""
    if largura <= 0 or altura <= 0:
        raise ValueError("Largura e altura devem ser positivas")
    return 2 * (largura + altura)

class ContaBancaria:
    def __init__(self, saldo_inicial=0):
        if saldo_inicial < 0:
            raise ValueError("Saldo inicial não pode ser negativo")
        self._saldo = saldo_inicial
    
    def depositar(self, valor):
        if valor <= 0:
            raise ValueError("Valor deve ser positivo")
        self._saldo += valor
        return self._saldo
    
    def sacar(self, valor):
        if valor <= 0:
            raise ValueError("Valor deve ser positivo")
        if valor > self._saldo:
            raise ValueError("Saldo insuficiente")
        self._saldo -= valor
        return self._saldo
    
    @property
    def saldo(self):
        return self._saldo'''
        
        print("Código de demonstração:")
        print("─" * 30)
        print(demo_code[:300] + "..." if len(demo_code) > 300 else demo_code)
        print("─" * 30)
        
        confirm = input("\nProsseguir com a demonstração? (S/n): ").strip().lower()
        if confirm in ['n', 'no', 'não']:
            return
        
        print("\n🔄 Gerando testes de demonstração...")
        self._process_code_generation(demo_code, "demo")
    
    def show_help(self):
        """Mostra ajuda e documentação."""
        print("\n" + "=" * 60)
        print("❓ AJUDA E DOCUMENTAÇÃO")
        print("=" * 60)
        
        help_text = """
COMO USAR O SISTEMA:

1. 📝 GERAR TESTES INTERATIVAMENTE:
   - Cole seu código Python
   - Digite 'END' para finalizar
   - O sistema analisará e gerará testes automaticamente

2. 📁 PROCESSAR ARQUIVOS:
   - Especifique arquivo único ou diretório
   - Suporte para processamento em lote
   - Resultados salvos automaticamente

3. 🔍 ANÁLISE DE CÓDIGO:
   - Apenas analisa sem gerar testes
   - Identifica funções, classes e complexidade

4. ✨ MELHORAR TESTES EXISTENTES:
   - Analisa testes atuais
   - Sugere melhorias de cobertura
   - Adiciona casos de teste ausentes

CONFIGURAÇÃO AZURE (opcional):
- AZURE_OPENAI_API_KEY: Sua chave de API
- AZURE_OPENAI_ENDPOINT: URL do endpoint
- AZURE_OPENAI_DEPLOYMENT_NAME: Nome do modelo

MODO SIMULAÇÃO:
- Funciona sem Azure OpenAI
- Gera templates de teste básicos
- Ideal para testes e demonstrações

SUPORTE:
- GitHub: @edsongom1
- Email: edsgom@gmail.com
        """
        
        print(help_text)
    
    def _display_generated_tests(self, test_code: str):
        """Mostra código dos testes gerados."""
        print(f"\n🧪 CÓDIGO DOS TESTES GERADOS:")
        print("─" * 60)
        
        # Limitar exibição se muito longo
        if len(test_code) > 1500:
            print(test_code[:1500])
            print(f"\n... (código truncado - {len(test_code)} caracteres totais)")
            
            show_full = input("\nMostrar código completo? (s/N): ").strip().lower()
            if show_full in ['s', 'sim', 'y', 'yes']:
                print(test_code)
        else:
            print(test_code)
        
        print("─" * 60)
    
    def _display_code_analysis(self, analysis: Dict):
        """Exibe análise detalhada do código."""
        print(f"\n🔍 ANÁLISE DETALHADA DO CÓDIGO:")
        print("─" * 50)
        
        # Estatísticas gerais
        stats = analysis.get('statistics', {})
        print(f"📊 Estatísticas:")
        print(f"   Funções encontradas: {stats.get('total_functions', 0)}")
        print(f"   Classes encontradas: {stats.get('total_classes', 0)}")
        print(f"   Métodos encontrados: {stats.get('total_methods', 0)}")
        print(f"   Linhas de código: {stats.get('total_lines', 0)}")
        print(f"   Complexidade ciclomática: {stats.get('complexity', 0)}")
        
        # Funções encontradas
        functions = analysis.get('functions', [])
        if functions:
            print(f"\n📋 Funções ({len(functions)}):")
            for func in functions:
                visibility = "🔒" if func['name'].startswith('_') else "🔓"
                params = ', '.join(func['parameters'])
                print(f"   {visibility} {func['name']}({params})")
        
        # Classes encontradas
        classes = analysis.get('classes', [])
        if classes:
            print(f"\n📦 Classes ({len(classes)}):")
            for cls in classes:
                print(f"   🏗️  {cls['name']}")
                if cls['methods']:
                    for method in cls['methods'][:3]:
                        visibility = "🔒" if method.startswith('_') else "🔓"
                        print(f"      {visibility} {method}()")
                    if len(cls['methods']) > 3:
                        print(f"      ... e mais {len(cls['methods']) - 3} método(s)")
        
        # Imports encontrados
        imports = analysis.get('imports', [])
        if imports:
            print(f"\n📥 Imports ({len(imports)}):")
            for imp in imports[:5]:
                print(f"   📦 {imp}")
            if len(imports) > 5:
                print(f"   ... e mais {len(imports) - 5} import(s)")
        
        # Recomendações
        recommendations = analysis.get('recommendations', [])
        if recommendations:
            print(f"\n💡 Recomendações:")
            for rec in recommendations:
                print(f"   • {rec}")
    
    def _offer_save_tests(self, test_code: str, base_filename: Optional[str] = None):
        """Oferece opção de salvar testes gerados."""
        save = input("\n💾 Deseja salvar os testes em arquivo? (S/n): ").strip().lower()
        if save not in ['n', 'no', 'não']:
            if base_filename:
                filename = f"test_{base_filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
            else:
                filename = f"test_generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
            
            try:
                # Criar diretório de testes se não existir
                test_dir = Path(self.config_manager.system_config['output_directory'])
                test_dir.mkdir(parents=True, exist_ok=True)
                
                file_path = test_dir / filename
                file_path.write_text(test_code, encoding='utf-8')
                print(f"✅ Testes salvos em: {file_path}")
                    
            except Exception as e:
                print(f"❌ Erro ao salvar arquivo: {e}")
    
    def _safe_exit(self):
        """Sai do programa de forma segura."""
        print("\n👋 Finalizando sistema...")
        
        # Mostrar estatísticas finais
        if self.statistics['total_generations'] > 0:
            runtime = datetime.now() - self.statistics['start_time']
            success_rate = (self.statistics['successful_generations'] / 
                          self.statistics['total_generations']) * 100
            
            print(f"📊 Estatísticas da sessão:")
            print(f"   Tempo total: {str(runtime).split('.')[0]}")
            print(f"   Gerações: {self.statistics['total_generations']}")
            print(f"   Taxa de sucesso: {success_rate:.1f}%")
        
        print("✅ Sistema finalizado com sucesso")


def create_argument_parser():
    """Cria parser para argumentos de linha de comando."""
    parser = argparse.ArgumentParser(
        description='Sistema de Geração de Testes Unitários com LangChain e Azure ChatGPT',
        epilog='Desenvolvido por Edson Gomes - Bootcamp DIO + BairesDev'
    )
    
    parser.add_argument(
        '--file', '-f',
        type=str,
        help='Arquivo Python para gerar testes'
    )
    
    parser.add_argument(
        '--directory', '-d',
        type=str,
        help='Diretório com arquivos Python para processar'
    )
    
    parser.add_argument(
        '--simulate',
        action='store_true',
        help='Executar em modo simulação (sem Azure API)'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='Sistema de Geração de Testes v1.0.0'
    )
    
    return parser


def process_command_line_args(args):
    """Processa argumentos de linha de comando."""
    cli = TestGeneratorCLI()
    
    if args.file:
        # Processar arquivo único
        file_path = Path(args.file)
        if file_path.exists() and file_path.suffix == '.py':
            source_code = file_path.read_text(encoding='utf-8')
            cli._process_code_generation(source_code, file_path.stem)
        else:
            print(f"❌ Arquivo não encontrado ou inválido: {args.file}")
            return 1
    
    elif args.directory:
        # Processar diretório
        dir_path = Path(args.directory)
        if dir_path.exists() and dir_path.is_dir():
            py_files = list(dir_path.glob("**/*.py"))
            if py_files:
                code_files = []
                for file_path in py_files:
                    try:
                        source_code = file_path.read_text(encoding='utf-8')
                        code_files.append((str(file_path), source_code))
                    except Exception as e:
                        print(f"⚠️  Erro ao ler {file_path}: {e}")
                
                if code_files:
                    cli._process_batch_generation(code_files)
            else:
                print(f"❌ Nenhum arquivo Python encontrado em: {args.directory}")
                return 1
        else:
            print(f"❌ Diretório não encontrado: {args.directory}")
            return 1
    
    else:
        # Executar interface interativa
        cli.run()
    
    return 0


def main():
    """Função principal do programa."""
    try:
        parser = create_argument_parser()
        args = parser.parse_args()
        
        # Processar argumentos ou executar interativamente
        exit_code = process_command_line_args(args)
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        logger.error(f"Erro fatal: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
