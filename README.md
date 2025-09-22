# Sistema de Geração de Testes Unitários
### Automatização de Testes com LangChain e Azure OpenAI

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-green.svg)](https://python.langchain.com/)
[![Azure OpenAI](https://img.shields.io/badge/Azure-OpenAI-blue.svg)](https://azure.microsoft.com/products/cognitive-services/openai-service)
[![Pytest](https://img.shields.io/badge/Framework-Pytest-orange.svg)](https://pytest.org/)

---

## 📋 Visão Geral

O **Sistema de Geração de Testes Unitários** é uma solução inovadora que combina a potência do **LangChain** com o **Azure OpenAI** para automatizar completamente a criação de testes unitários Python. Desenvolvido como projeto do bootcamp **DIO + BairesDev Machine Learning**, este sistema revoluciona o processo de desenvolvimento orientado a testes (TDD).

### 🎯 Objetivos

- **Automatizar** a geração de testes unitários de alta qualidade
- **Acelerar** o desenvolvimento com TDD automatizado
- **Garantir cobertura** abrangente de cenários de teste
- **Padronizar** a qualidade dos testes em projetos Python
- **Integrar** IA generativa ao workflow de desenvolvimento
- **Democratizar** as melhores práticas de teste

---

## 🗂️ Estrutura do Projeto

```
sistema-geracao-testes/
├── src/
│   ├── agents/
│   │   └── test_generator_agent.py      # Agente principal LangChain
│   ├── config/
│   │   └── azure_config_module.py       # Configurações Azure OpenAI
│   ├── prompts/
│   │   └── test_generation_prompts.py   # Templates de prompts especializados
│   ├── tools/
│   │   ├── code_analyzer.py             # Analisador de código Python
│   │   ├── test_validator.py            # Validador de testes gerados
│   │   └── python_executor.py           # Executor seguro de código
│   └── utils/
├── tests/
│   ├── unit/                           # Testes unitários do sistema
│   ├── integration/                    # Testes de integração
│   └── generated/                      # Testes gerados pelo sistema
├── examples/                           # Exemplos de uso
├── docs/                              # Documentação técnica
├── logs/                              # Logs de execução
├── results/                           # Resultados de processamento em lote
├── main_cli.py                        # Interface CLI principal
├── requirements.txt                   # Dependências do projeto
├── .env.example                       # Template de variáveis de ambiente
└── README.md
```

---

## 🚀 Tecnologias Utilizadas

### **Core Technologies**
- **Python 3.8+** - Linguagem principal
- **LangChain** - Framework para aplicações com LLM
- **Azure OpenAI** - Modelo de linguagem GPT-4
- **AST (Abstract Syntax Tree)** - Análise estática de código

### **Frameworks de Teste**
- **Pytest** - Framework principal (padrão)
- **Unittest** - Suporte nativo Python
- **Parametrização** - Testes baseados em dados
- **Fixtures** - Setup/teardown automatizado

### **Ferramentas de Desenvolvimento**
- **Logging** - Sistema robusto de logs
- **Argparse** - Interface de linha de comando
- **JSON/YAML** - Configurações e relatórios
- **Pathlib** - Manipulação moderna de arquivos

---

## 📦 Instalação e Configuração

### **1. Clonar o Repositório**
```bash
git clone https://github.com/edsongom1/sistema-geracao-testes.git
cd sistema-geracao-testes
```

### **2. Criar Ambiente Virtual**
```bash
# Python venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Ou usando conda
conda create -n test-generator python=3.9
conda activate test-generator
```

### **3. Instalar Dependências**
```bash
pip install -r requirements.txt
```

### **4. Configurar Variáveis de Ambiente (Opcional)**
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais Azure (opcional para modo simulação):
```bash
# Configurações Azure OpenAI (opcional)
AZURE_OPENAI_API_KEY=sua_chave_aqui
AZURE_OPENAI_ENDPOINT=https://seu-endpoint.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4

# Configurações do Sistema
LOG_LEVEL=INFO
MAX_TOKENS=2000
TEMPERATURE=0.1
```

### **5. Verificar Instalação**
```bash
python main_cli.py --version
```

---

## 🎮 Como Executar

### **Interface CLI Interativa**
```bash
python main_cli.py
```

### **Modo Simulação (sem Azure)**
```bash
python main_cli.py --simulate
```

### **Processar Arquivo Único**
```bash
python main_cli.py --file exemplo.py --output tests/
```

### **Processar Diretório**
```bash
python main_cli.py --directory src/ --output tests/
```

### **Modo Silencioso**
```bash
python main_cli.py --quiet --file codigo.py
```

---

## 🖥️ Demonstração Prática

### **Tela Inicial do Sistema**
O sistema apresenta uma interface CLI intuitiva com menu principal:

```

⚠️  MODO SIMULAÇÃO ATIVO
   Configure as variáveis Azure OpenAI para usar o modo completo

OPÇÕES DISPONÍVEIS:
──────────────────────────────────────────────────
1. 📝 Gerar testes para código Python
2. 📁 Processar arquivo(s) de código
3. 🔍 Analisar código (sem gerar testes)
4. ✨ Melhorar testes existentes
5. ⚙️  Configurações do sistema
6. 📊 Estatísticas e relatórios
7. 🧪 Executar exemplo de demonstração
8. ❓ Ajuda e documentação
9. 🚪 Sair
```

### **Opção 1: Geração Interativa de Testes**

Permite colar código Python diretamente no terminal:

```
============================================================
📝 GERAÇÃO DE TESTES INTERATIVA
============================================================

Cole ou digite seu código Python abaixo.
Para finalizar a entrada, digite 'END' em uma linha separada:
────────────────────────────────────────
```

### **Opção 2: Processamento de Arquivos**

Processa arquivos ou diretórios inteiros:

```
============================================================
📁 PROCESSAMENTO DE ARQUIVOS
============================================================

📁 Caminho do diretório: C:\devpython\projetos\dio-bairesdev-ml\...
📄 Encontrados 1 arquivo(s) Python:
  1. transfer_learning_cats_dogs.py

Processar 1 arquivo(s)? (S/n): s

📊 RESULTADO DO PROCESSAMENTO EM LOTE
==================================================
Total de arquivos: 1
Sucessos: 0
Falhas: 1
Tempo total: 0.03s
```

### **Opção 3: Análise de Código**

Analisa estrutura do código sem gerar testes:

```
============================================================
🔍 ANÁLISE DE CÓDIGO
============================================================

🔍 ANÁLISE DETALHADA DO CÓDIGO:
──────────────────────────────────────────

📊 Estatísticas:
   Funções encontradas: 4
   Classes encontradas: 1
   Métodos encontrados: 4
   Linhas de código: 23
   Complexidade ciclomática: 5

📋 Funções (4):
   🔒 __init__(self, saldo_inicial)
   🔒 depositar(self, valor)
   🔒 sacar(self, valor)
   🔒 saldo(self)

📦 Classes (1):
   🗂️  ContaBancaria
      🔒 __init__()
      🔒 depositar()
      🔒 sacar()
      ... e mais 1 método(s)
```

---

## 💡 Exemplos de Código para Teste

### **1. Funções Simples**
```python
def calcular_quadrado(numero):
    return numero * numero

def eh_par(numero):
    return numero % 2 == 0
END
```

### **2. Funções com Validação**
```python
def dividir(a, b):
    if b == 0:
        raise ValueError("Divisão por zero não permitida")
    return a / b

def validar_email(email):
    return "@" in email and "." in email
END
```

### **3. Classes Simples**
```python
class Calculadora:
    def somar(self, a, b):
        return a + b
    
    def subtrair(self, a, b):
        return a - b
    
    def multiplicar(self, a, b):
        return a * b
END
```

### **4. Código Mais Complexo**
```python
class ContaBancaria:
    def __init__(self, saldo_inicial=0):
        if saldo_inicial < 0:
            raise ValueError("Saldo não pode ser negativo")
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
END
```

---

## 📊 Resultados Esperados

### **Análise de Código**
O sistema fornece análise detalhada do código fornecido:

```python
# Input: Função simples
def dividir(a, b):
    if b == 0:
        raise ZeroDivisionError("Divisão por zero")
    return a / b

# Output: Análise estruturada
{
    "functions": [
        {
            "name": "dividir",
            "parameters": ["a", "b"],
            "complexity": "low",
            "raises": ["ZeroDivisionError"]
        }
    ],
    "estimated_test_count": 3,
    "complexity_score": 2.5
}
```

### **Testes Gerados (Exemplo)**
```python
import pytest

def test_dividir_casos_normais():
    """Testa divisão com valores normais."""
    assert dividir(10, 2) == 5.0
    assert dividir(9, 3) == 3.0
    assert dividir(1, 1) == 1.0

def test_dividir_numeros_negativos():
    """Testa divisão com números negativos."""
    assert dividir(-10, 2) == -5.0
    assert dividir(10, -2) == -5.0
    assert dividir(-10, -2) == 5.0

def test_dividir_divisao_por_zero():
    """Testa exceção para divisão por zero."""
    with pytest.raises(ZeroDivisionError, match="Divisão por zero"):
        dividir(10, 0)

@pytest.mark.parametrize("a,b,esperado", [
    (10, 2, 5.0),
    (15, 3, 5.0),
    (100, 10, 10.0),
])
def test_dividir_parametrizado(a, b, esperado):
    """Testa divisão com múltiplos casos."""
    assert dividir(a, b) == esperado
```

### **Métricas de Qualidade**
```json
{
    "cobertura_estimada": 95.2,
    "testes_gerados": 12,
    "casos_extremos": 4,
    "testes_excecao": 2,
    "qualidade_score": 8.7,
    "tempo_execucao": 3.2
}
```

---

## ✨ Benefícios

### **Para Desenvolvedores**
- ⚡ **Acelera desenvolvimento** - Geração automática de testes em segundos
- 🎯 **Melhora qualidade** - Testes seguem melhores práticas
- 📈 **Aumenta cobertura** - Identifica cenários não considerados
- 📄 **Padroniza código** - Estrutura consistente de testes
- 🧠 **Reduz carga cognitiva** - IA pensa nos casos de teste

### **Para Equipes**
- 📊 **Relatórios detalhados** - Métricas de cobertura e qualidade  
- 🔍 **Análise de código** - Identifica complexidade e dependências
- 📚 **Documentação automática** - Testes servem como documentação
- ⚙️ **Integração fácil** - CLI e API para automação
- 🎮 **Modo demonstração** - Funciona sem configuração Azure

### **Para Projetos**
- 🚀 **ROI imediato** - Redução drástica no tempo de criação de testes
- 🛡️ **Maior confiabilidade** - Detecção precoce de bugs
- 📋 **Compliance** - Atende padrões de qualidade de código
- 🔧 **Manutenibilidade** - Testes facilitam refatoração
- 📚 **Conhecimento preservado** - Casos de teste documentam comportamento

---

## 🛠 Troubleshooting

### **Problemas Comuns**

**1. Erro de Importação LangChain**
```bash
# Solução
pip install --upgrade langchain langchain-openai
```

**2. Credenciais Azure Inválidas**
```bash
# Verificar variáveis
echo $AZURE_OPENAI_API_KEY
echo $AZURE_OPENAI_ENDPOINT

# Usar modo simulação
python main_cli.py --simulate
```

**3. Código com Sintaxe Inválida**
```python
# Sistema detecta automaticamente e reporta erros
{
    "success": false,
    "error": "SyntaxError: invalid syntax (line 5)"
}
```

---

## 🧪 Executando Testes

### **Testes do Sistema**
```bash
# Todos os testes
pytest tests/

# Testes unitários
pytest tests/unit/

# Testes com cobertura
pytest --cov=src tests/

# Testes de integração
pytest tests/integration/ -v
```

---

## 🤝 Contribuindo

### **Como Contribuir**
1. Fork do repositório
2. Criar branch para feature: `git checkout -b feature/nova-funcionalidade`
3. Commit das mudanças: `git commit -m 'Adiciona nova funcionalidade'`
4. Push para branch: `git push origin feature/nova-funcionalidade`
5. Abrir Pull Request

### **Áreas para Contribuição**
- 🌐 **Integração com outras LLMs** (OpenAI, Anthropic, etc.)
- 🧪 **Novos frameworks de teste** (unittest, nose2, etc.)
- 🎨 **Interface web** (FastAPI + React)
- 📊 **Dashboards de métricas** (Grafana, Streamlit)
- 🔌 **Plugins para IDEs** (VSCode, PyCharm)

---

## 📋 Roadmap

### **Versão 2.0** (Q2 2025)
- [ ] Interface web completa
- [ ] Suporte a múltiplas LLMs
- [ ] Integração CI/CD nativa
- [ ] Plugin para VSCode
- [ ] Dashboard de métricas

### **Versão 2.1** (Q3 2025)
- [ ] Geração de testes de integração
- [ ] Suporte a FastAPI/Django
- [ ] Análise de performance
- [ ] Geração de documentação
- [ ] API REST completa

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 🎓 Agradecimentos

Este projeto foi desenvolvido como parte do bootcamp **Machine Learning** oferecido pela parceria **DIO.me** e **BairesDev**.

### **Agradecimentos Especiais**
- **[DIO.me](https://dio.me)** - Por proporcionar educação tecnológica de qualidade e democratizar o acesso ao conhecimento em programação e machine learning
- **[BairesDev](https://www.bairesdev.com/)** - Por apoiar iniciativas educacionais e oferecer oportunidades de crescimento profissional na área de tecnologia
- **Comunidade Python** - Por criar e manter as ferramentas que tornaram este projeto possível
- **Equipe LangChain** - Pelo framework revolucionário que simplifica aplicações com LLM
- **Microsoft Azure** - Por disponibilizar acesso ao Azure OpenAI Service
