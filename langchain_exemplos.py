# ====================================================================
# requirements.txt
# ====================================================================

langchain>=0.1.0
langchain-openai>=0.1.0
langchain-core>=0.1.0
openai>=1.0.0
python-dotenv>=1.0.0
pytest>=7.0.0
black>=23.0.0
ast-tools>=0.2.0
tiktoken>=0.5.0

# ====================================================================
# .env.example
# ====================================================================

# Configurações Azure OpenAI
AZURE_OPENAI_API_KEY=sua_chave_azure_aqui
AZURE_OPENAI_ENDPOINT=https://seu-recurso.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4

# Configurações do Sistema
MAX_TOKENS=2000
TEMPERATURE=0.1
DEBUG_MODE=True

# ====================================================================
# exemplos_langchain.py - Baseado nas imagens fornecidas
# ====================================================================

from langchain.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.tools.python.tool import PythonREPLTool
import os

def exemplo_basic_prompt():
    """Exemplo básico de prompt baseado na primeira imagem."""
    
    # Configuração do prompt template
    prompt = PromptTemplate(
        input_variables=["text"],
        template="""Traduzir para francês:
        {text}"""
    )
    
    # Configuração do LLM (baseado na imagem)
    llm = AzureChatOpenAI(
        temperature=0,
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")
    )
    
    # Criar chain
    chain = prompt | llm
    
    # Executar
    response = chain.invoke({"text": "Hello world"})
    print(f"Resposta: {response.content}")

def exemplo_agent_com_tools():
    """Exemplo de agente com ferramentas baseado na segunda imagem."""
    
    # Configurar LLM
    llm = AzureChatOpenAI(
        temperature=0,
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    )
    
    # Configurar ferramentas
    tools = [
        Tool(
            name="ExecCode",
            func=PythonREPLTool().run,
            description="Executa código Python"
        )
    ]
    
    # Inicializar agente
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
    )
    
    # Executar
    result = agent.run("Calculate 2+2 in Python")
    print(f"Resultado: {result}")

def exemplo_gerador_testes_completo():
    """Exemplo completo para geração de testes unitários."""
    
    # Código de exemplo para gerar testes
    codigo_exemplo = '''
def validar_email(email):
    """Valida se um email tem formato correto."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def calcular_desconto(preco, percentual):
    """Calcula desconto sobre um preço."""
    if preco < 0:
        raise ValueError("Preço não pode ser negativo")
    if percentual < 0 or percentual > 100:
        raise ValueError("Percentual deve estar entre 0 e 100")
    return preco * (1 - percentual / 100)

class Produto:
    def __init__(self, nome, preco):
        if not nome or not isinstance(nome, str):
            raise ValueError("Nome deve ser uma string não vazia")
        if preco <= 0:
            raise ValueError("Preço deve ser positivo")
        self.nome = nome
        self.preco = preco
    
    def aplicar_desconto(self, percentual):
        """Aplica desconto ao produto."""
        self.preco = calcular_desconto(self.preco, percentual)
    
    def __str__(self):
        return f"{self.nome}: R$ {self.preco:.2f}"
'''
    
    # Configurar sistema de geração
    llm = AzureChatOpenAI(
        temperature=0.1,
        max_tokens=2000,
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    )
    
    # Template de prompt para geração de testes
    prompt_template = PromptTemplate(
        input_variables=["codigo"],
        template="""
Você é um especialista em testes unitários Python. Analise o código fornecido e gere testes completos usando pytest.

CÓDIGO:
{codigo}

Gere testes que incluam:
1. Casos normais de uso
2. Casos extremos e de borda  
3. Testes de exceções
4. Fixtures quando necessário
5. Parametrização quando apropriado

Use boas práticas de nomenclatura e documentação.

TESTES GERADOS:
"""
    )
    
    # Configurar ferramentas
    python_tool = PythonREPLTool()
    
    tools = [
        Tool(
            name="PythonREPL",
            func=python_tool.run,
            description="Executa código Python para validação"
        ),
        Tool(
            name="ValidateTest",
            func=lambda x: "Teste validado" if "def test_" in x else "Teste inválido",
            description="Valida se o código contém testes válidos"
        )
    ]
    
    # Criar agente
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    
    # Gerar prompt
    prompt = prompt_template.format(codigo=codigo_exemplo)
    
    # Executar geração
    resultado = agent.run(prompt)
    
    return resultado

# ====================================================================
# demo_completo.py - Demonstração prática do sistema
# ====================================================================

import os
from dotenv import load_dotenv

def executar_demo():
    """Executa demonstração completa do sistema."""
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    print("=" * 60)
    print("DEMO: SISTEMA DE GERAÇÃO DE TESTES COM LANGCHAIN")
    print("=" * 60)
    
    # Verificar configuração
    if not os.getenv("AZURE_OPENAI_API_KEY"):
        print("⚠️  Modo demonstração - configurações Azure não encontradas")
        print("💡 Configure o arquivo .env para usar Azure OpenAI")
        demonstrar_funcionalidades_basicas()
    else:
        print("✅ Configurações Azure encontradas")
        demonstrar_com_azure()

def demonstrar_funcionalidades_basicas():
    """Demonstra funcionalidades básicas sem Azure."""
    
    print
