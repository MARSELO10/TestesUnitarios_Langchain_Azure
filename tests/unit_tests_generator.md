# 🧪 Sistema de Geração de Testes Unitários com LangChain e Azure ChatGPT

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-green.svg)](https://langchain.com)
[![Azure](https://img.shields.io/badge/Azure-ChatGPT-orange.svg)](https://azure.microsoft.com)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 📋 Descrição do Projeto

Este projeto implementa um **sistema automatizado de geração de testes unitários** utilizando **LangChain** e **Azure ChatGPT**. O sistema analisa código Python e gera automaticamente testes unitários completos seguindo boas práticas de **Test-Driven Development (TDD)** e metodologias ágeis.

## 🎯 Objetivos do Desafio

- Automatizar a criação de testes unitários para código Python
- Implementar agentes inteligentes usando LangChain
- Integrar Azure ChatGPT para geração de código
- Aplicar conceitos de TDD e testes automatizados
- Documentar processos técnicos de forma estruturada

## 🏗️ Arquitetura do Sistema

```
unit-tests-generator/
├── 📁 src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── test_generator_agent.py    # Agente principal
│   │   └── code_analyzer_agent.py     # Analisador de código
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── python_executor.py         # Executor Python
│   │   └── test_validator.py          # Validador de testes
│   ├── prompts/
│   │   ├── __init__.py
│   │   └── test_generation_prompts.py # Templates de prompts
│   └── config/
│       ├── __init__.py
│       └── azure_config.py            # Configurações Azure
├── 📁 tests/
│   ├── test_generator/
│   ├── sample_code/                   # Código de exemplo
│   └── generated_tests/               # Testes gerados
├── 📁 examples/
│   ├── basic_usage.py
│   └── advanced_examples.py
├── 📁 docs/
│   ├── architecture.md
│   └── api_reference.md
├── requirements.txt
├── .env.example
└── README.md
```

## 🛠️ Tecnologias Utilizadas

### Frameworks Principais
- **LangChain**: Framework para desenvolvimento de aplicações com LLMs
- **Azure OpenAI**: Serviço ChatGPT da Microsoft Azure
- **Python 3.8+**: Linguagem de programação principal

### Bibliotecas Específicas
- **langchain-openai**: Integração LangChain com Azure OpenAI
- **langchain-core**: Componentes centrais do LangChain
- **pytest**: Framework de testes unitários
- **ast**: Análise sintática de código Python
- **black**: Formatação automática de código

## 📦 Instalação e Configuração

### 1. Pré-requisitos

```bash
# Verificar versão do Python
python --version  # Deve ser 3.8+

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 2. Instalação das Dependências

```bash
# Instalar dependências principais
pip install langchain langchain-openai langchain-core
pip install pytest black ast-tools
pip install python-dotenv tiktoken

# Ou usar requirements.txt
pip install -r requirements.txt
```

### 3. Configuração do Azure OpenAI

```bash
# Copiar arquivo de configuração
cp .env.example .env

# Editar .env com suas credenciais
nano .env
```

**.env**:
```env
# Configurações Azure OpenAI
AZURE_OPENAI_API_KEY=sua_chave_aqui
AZURE_OPENAI_ENDPOINT=https://seu-endpoint.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4

# Configurações do Sistema
MAX_TOKENS=2000
TEMPERATURE=0.1
DEBUG_MODE=True
```

## 🚀 Como Usar

### Uso Básico

```python
from src.agents.test_generator_agent import TestGeneratorAgent
from src.config.azure_config import AzureConfig

# Inicializar configuração
config = AzureConfig()

# Criar agente gerador de testes
agent = TestGeneratorAgent(config)

# Código de exemplo para testar
sample_code = '''
def calcular_area_retangulo(largura, altura):
    """Calcula a área de um retângulo."""
    if largura <= 0 or altura <= 0:
        raise ValueError("Largura e altura devem ser positivas")
    return largura * altura

def calcular_perimetro_retangulo(largura, altura):
    """Calcula o perímetro de um retângulo."""
    return 2 * (largura + altura)
'''

# Gerar testes automaticamente
testes_gerados = agent.generate_tests(sample_code)
print(testes_gerados)
```

### Uso Avançado com Validação

```python
from src.agents.test_generator_agent import TestGeneratorAgent
from src.tools.test_validator import TestValidator

# Gerar e validar testes
agent = TestGeneratorAgent()
validator = TestValidator()

# Analisar código complexo
codigo_complexo = '''
class ContaBancaria:
    def __init__(self, saldo_inicial=0):
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
        return self._saldo
'''

# Gerar testes
testes = agent.generate_tests(codigo_complexo)

# Validar testes gerados
resultado_validacao = validator.validate_tests(testes, codigo_complexo)
print(f"Testes válidos: {resultado_validacao['valid']}")
print(f"Cobertura: {resultado_validacao['coverage']}%")
```

## 🤖 Implementação dos Agentes

### Agente Principal: TestGeneratorAgent

```python
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate

class TestGeneratorAgent:
    def __init__(self, config):
        self.llm = AzureChatOpenAI(
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
            api_key=config.AZURE_OPENAI_API_KEY,
            api_version=config.AZURE_OPENAI_API_VERSION,
            deployment_name=config.AZURE_OPENAI_DEPLOYMENT_NAME,
            temperature=0.1
        )
        
        self.tools = self._setup_tools()
        self.agent = self._initialize_agent()
    
    def _setup_tools(self):
        """Configura ferramentas do agente."""
        return [
            Tool(
                name="CodeAnalyzer",
                func=self._analyze_code,
                description="Analisa código Python e identifica funções para testar"
            ),
            Tool(
                name="TestGenerator",
                func=self._generate_unit_tests,
                description="Gera testes unitários para código Python"
            ),
            Tool(
                name="PythonREPL",
                func=self._execute_python,
                description="Executa código Python para validação"
            )
        ]
    
    def _initialize_agent(self):
        """Inicializa agente com tipo ZERO_SHOT_REACT_DESCRIPTION."""
        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )
    
    def generate_tests(self, source_code):
        """Gera testes unitários para o código fornecido."""
        prompt = f"""
        Analise o seguinte código Python e gere testes unitários completos:
        
        {source_code}
        
        Os testes devem seguir as melhores práticas:
        1. Usar pytest como framework
        2. Testar casos normais e de borda
        3. Incluir testes de exceções quando aplicável
        4. Usar nomenclatura clara e descritiva
        5. Incluir docstrings nos testes
        """
        
        return self.agent.run(prompt)
```

### Ferramenta de Execução Python

```python
from langchain.tools.python.tool import PythonREPLTool

class CustomPythonREPL(PythonREPLTool):
    """Ferramenta customizada para execução de código Python."""
    
    def __init__(self):
        super().__init__()
        self.name = "PythonExecutor"
        self.description = """
        Executa código Python de forma segura.
        Útil para validar testes gerados e verificar se o código funciona.
        """
    
    def _run(self, query: str) -> str:
        """Executa código Python com tratamento de erros."""
        try:
            return super()._run(query)
        except Exception as e:
            return f"Erro na execução: {str(e)}"
```

## 📋 Templates de Prompts

### Prompt para Geração de Testes

```python
TEST_GENERATION_TEMPLATE = """
Você é um especialista em testes unitários Python. Analise o código fornecido e gere testes unitários completos.

CÓDIGO PARA ANÁLISE:
{source_code}

INSTRUÇÕES:
1. Use pytest como framework de teste
2. Crie testes para todos os métodos públicos
3. Inclua casos de teste positivos e negativos
4. Teste tratamento de exceções quando aplicável
5. Use fixtures quando necessário
6. Mantenha alta cobertura de código

FORMATO DE SAÍDA:
- Código de teste completo
- Comentários explicativos
- Imports necessários
- Assertions apropriados

EXEMPLO DE ESTRUTURA:
```python
import pytest
from module import ClassName

class TestClassName:
    def test_method_normal_case(self):
        # Teste caso normal
        pass
    
    def test_method_edge_case(self):
        # Teste caso extremo
        pass
    
    def test_method_exception_case(self):
        # Teste exceções
        with pytest.raises(ExceptionType):
            pass
```

Gere os testes agora:
"""

ANALYSIS_TEMPLATE = """
Analise o código Python fornecido e identifique:

CÓDIGO:
{code}

ANÁLISE REQUERIDA:
1. Funções públicas para testar
2. Classes e métodos principais
3. Casos de borda identificados
4. Exceções que devem ser testadas
5. Dependências necessárias

Forneça um resumo estruturado da análise.
"""
```

## 🧪 Exemplos de Testes Gerados

### Exemplo 1: Função Simples

**Código Original:**
```python
def dividir(a, b):
    """Divide dois números."""
    if b == 0:
        raise ZeroDivisionError("Divisão por zero não permitida")
    return a / b
```

**Teste Gerado:**
```python
import pytest

def test_dividir_numeros_positivos():
    """Testa divisão com números positivos."""
    resultado = dividir(10, 2)
    assert resultado == 5.0

def test_dividir_numeros_negativos():
    """Testa divisão com números negativos."""
    resultado = dividir(-10, 2)
    assert resultado == -5.0

def test_dividir_por_zero():
    """Testa divisão por zero - deve levantar exceção."""
    with pytest.raises(ZeroDivisionError, match="Divisão por zero não permitida"):
        dividir(10, 0)

def test_dividir_zero_por_numero():
    """Testa divisão de zero por número."""
    resultado = dividir(0, 5)
    assert resultado == 0.0
```

### Exemplo 2: Classe Complexa

**Código Original:**
```python
class CalculadoraFinanceira:
    def __init__(self):
        self.historico = []
    
    def juros_simples(self, capital, taxa, tempo):
        if capital <= 0 or taxa < 0 or tempo <= 0:
            raise ValueError("Parâmetros inválidos")
        
        juros = capital * taxa * tempo
        total = capital + juros
        
        self.historico.append({
            'operacao': 'juros_simples',
            'capital': capital,
            'taxa': taxa,
            'tempo': tempo,
            'resultado': total
        })
        
        return total
```

**Teste Gerado:**
```python
import pytest
from calculadora_financeira import CalculadoraFinanceira

class TestCalculadoraFinanceira:
    @pytest.fixture
    def calc(self):
        """Fixture para criar instância da calculadora."""
        return CalculadoraFinanceira()
    
    def test_juros_simples_caso_normal(self, calc):
        """Testa cálculo de juros simples - caso normal."""
        resultado = calc.juros_simples(1000, 0.1, 2)
        assert resultado == 1200.0
        
        # Verifica se foi adicionado ao histórico
        assert len(calc.historico) == 1
        assert calc.historico[0]['operacao'] == 'juros_simples'
    
    def test_juros_simples_capital_invalido(self, calc):
        """Testa juros simples com capital inválido."""
        with pytest.raises(ValueError, match="Parâmetros inválidos"):
            calc.juros_simples(-1000, 0.1, 2)
    
    def test_juros_simples_taxa_negativa(self, calc):
        """Testa juros simples com taxa negativa."""
        with pytest.raises(ValueError, match="Parâmetros inválidos"):
            calc.juros_simples(1000, -0.1, 2)
    
    def test_historico_multiplas_operacoes(self, calc):
        """Testa acúmulo de histórico em múltiplas operações."""
        calc.juros_simples(1000, 0.1, 1)
        calc.juros_simples(2000, 0.05, 3)
        
        assert len(calc.historico) == 2
        assert calc.historico[0]['capital'] == 1000
        assert calc.historico[1]['capital'] == 2000
```

## 📊 Validação e Métricas

### Sistema de Validação

```python
class TestValidator:
    """Valida testes gerados automaticamente."""
    
    def validate_tests(self, test_code, original_code):
        """Valida se os testes gerados são válidos."""
        validation_result = {
            'valid': True,
            'coverage': 0,
            'issues': [],
            'suggestions': []
        }
        
        try:
            # Executa análise sintática
            ast.parse(test_code)
            
            # Verifica estrutura dos testes
            coverage = self._calculate_coverage(test_code, original_code)
            validation_result['coverage'] = coverage
            
            # Verifica boas práticas
            issues = self._check_best_practices(test_code)
            validation_result['issues'] = issues
            
        except SyntaxError as e:
            validation_result['valid'] = False
            validation_result['issues'].append(f"Erro de sintaxe: {e}")
        
        return validation_result
    
    def _calculate_coverage(self, test_code, original_code):
        """Calcula cobertura aproximada dos testes."""
        # Análise simplificada - em produção usar coverage.py
        original_functions = self._extract_functions(original_code)
        tested_functions = self._extract_tested_functions(test_code)
        
        if not original_functions:
            return 100
        
        coverage = len(tested_functions) / len(original_functions) * 100
        return min(coverage, 100)
```

## 📈 Métricas de Performance

### Dashboard de Métricas

```python
class MetricsDashboard:
    """Dashboard para acompanhar métricas do sistema."""
    
    def __init__(self):
        self.metrics = {
            'tests_generated': 0,
            'success_rate': 0.0,
            'average_coverage': 0.0,
            'execution_time': 0.0
        }
    
    def update_metrics(self, generation_result):
        """Atualiza métricas após geração de testes."""
        self.metrics['tests_generated'] += 1
        
        if generation_result['valid']:
            success_count = self.metrics['tests_generated'] * self.metrics['success_rate']
            self.metrics['success_rate'] = (success_count + 1) / self.metrics['tests_generated']
        
        # Atualiza cobertura média
        current_avg = self.metrics['average_coverage']
        new_coverage = generation_result['coverage']
        total_tests = self.metrics['tests_generated']
        
        self.metrics['average_coverage'] = (
            (current_avg * (total_tests - 1) + new_coverage) / total_tests
        )
    
    def generate_report(self):
        """Gera relatório de métricas."""
        return f"""
        📊 RELATÓRIO DE MÉTRICAS
        ========================
        Testes Gerados: {self.metrics['tests_generated']}
        Taxa de Sucesso: {self.metrics['success_rate']:.2%}
        Cobertura Média: {self.metrics['average_coverage']:.1f}%
        Tempo Médio: {self.metrics['execution_time']:.2f}s
        """
```

## 🔧 Configuração Avançada

### Configurações Customizáveis

```python
# config/settings.py
GENERATION_SETTINGS = {
    # Configurações do LLM
    'temperature': 0.1,  # Criatividade vs Precisão
    'max_tokens': 2000,  # Tamanho máximo da resposta
    'top_p': 0.95,       # Diversidade do vocabulário
    
    # Configurações dos Testes
    'test_framework': 'pytest',  # pytest, unittest
    'include_fixtures': True,    # Usar fixtures
    'test_edge_cases': True,     # Testar casos extremos
    'test_exceptions': True,     # Testar exceções
    'use_parametrize': True,     # Usar parametrização
    
    # Configurações de Qualidade
    'min_coverage': 80,          # Cobertura mínima
    'max_complexity': 10,        # Complexidade máxima
    'require_docstrings': True,  # Exigir docstrings
}
```

## 🚀 Deploy e Integração

### Integração com CI/CD

```yaml
# .github/workflows/auto-tests.yml
name: Auto Generate Tests

on:
  push:
    paths:
      - '**.py'
  pull_request:
    paths:
      - '**.py'

jobs:
  generate-tests:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Generate Tests
      run: |
        python scripts/auto_generate_tests.py
      env:
        AZURE_OPENAI_API_KEY: ${{ secrets.AZURE_OPENAI_API_KEY }}
        AZURE_OPENAI_ENDPOINT: ${{ secrets.AZURE_OPENAI_ENDPOINT }}
    
    - name: Run Generated Tests
      run: |
        pytest tests/generated/ -v --cov=src/
```

## 📚 Documentação Adicional

### API Reference

```python
# Principais classes e métodos
class TestGeneratorAgent:
    def generate_tests(source_code: str) -> str
    def analyze_code(source_code: str) -> dict
    def validate_output(test_code: str) -> bool

class TestValidator:
    def validate_tests(test_code: str, original_code: str) -> dict
    def check_best_practices(test_code: str) -> list
    def calculate_coverage(test_code: str, original_code: str) -> float

class MetricsDashboard:
    def update_metrics(generation_result: dict) -> None
    def generate_report() -> str
    def export_metrics(format: str) -> str
```

## 🐛 Troubleshooting

### Problemas Comuns

**1. Erro de Autenticação Azure:**
```bash
# Verificar credenciais
echo $AZURE_OPENAI_API_KEY
# Testar conectividade
curl -H "api-key: $AZURE_OPENAI_API_KEY" $AZURE_OPENAI_ENDPOINT/models
```

**2. Testes Gerados Inválidos:**
```python
# Ativar debug mode
DEBUG_MODE = True

# Verificar logs detalhados
tail -f logs/generation.log
```

**3. Performance Lenta:**
```python
# Otimizar configurações
GENERATION_SETTINGS['max_tokens'] = 1000
GENERATION_SETTINGS['temperature'] = 0.0
```

## 🎯 Próximos Passos

### Roadmap de Funcionalidades

- [ ] **Suporte a TypeScript/JavaScript**
- [ ] **Integração com IDEs** (VS Code, PyCharm)
- [ ] **Geração de Mocks automáticos**
- [ ] **Análise de performance dos testes**
- [ ] **Interface web para configuração**
- [ ] **Suporte a diferentes frameworks de teste**
- [ ] **Integração com SonarQube**
- [ ] **Geração de relatórios HTML**

## 📝 Conclusão

Este sistema demonstra como combinar **LangChain**, **Azure ChatGPT** e **agentes inteligentes** para automatizar uma tarefa complexa como a geração de testes unitários. A abordagem usando **AgentType.ZERO_SHOT_REACT_DESCRIPTION** permite que o agente "pense" sobre o problema e use ferramentas de forma inteligente.

### Principais Aprendizados

1. **Prompting Eficaz**: Templates bem estruturados são cruciais
2. **Validação Robusta**: Sempre validar código gerado
3. **Iteração Contínua**: Melhorar prompts baseado nos resultados
4. **Integração Prática**: Foco em soluções que funcionem no mundo real

### Impacto Esperado

- **Redução de 70-80%** no tempo de criação de testes
- **Melhoria na cobertura** de código de projetos
- **Padronização** de qualidade nos testes
- **Democratização** de boas práticas de TDD

---

### 🎓 Projeto Desenvolvido para:
**DIO + BairesDev - Bootcamp Machine Learning**  
**Desafio:** Gerando Testes Unitários com LangChain e Azure ChatGPT

---

⭐ **Se este projeto foi útil, considere dar uma estrela no repositório!**

**#LangChain #AzureChatGPT #TDD #TestesUnitarios #MachineLearning #DIO**
