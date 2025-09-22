# ====================================================================
# requirements.txt - Dependências do Sistema de Geração de Testes
# Sistema de Geração de Testes Unitários com LangChain e Azure ChatGPT
# Autor: Marcelo José Vieira Filho - DIO + BairesDev Bootcamp
# ====================================================================

# Core LangChain
langchain>=0.1.0
langchain-openai>=0.1.0
langchain-core>=0.1.0
langchain-community>=0.0.13

# Azure OpenAI Integration
openai>=1.0.0
azure-identity>=1.15.0

# Environment and Configuration
python-dotenv>=1.0.0
pydantic>=2.0.0
pydantic-settings>=2.0.0

# Testing Framework
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0

# Code Analysis and Formatting
ast-tools>=0.2.0
black>=23.0.0
isort>=5.12.0
flake8>=6.0.0

# Token Management
tiktoken>=0.5.0

# Data Handling
pandas>=2.0.0
numpy>=1.24.0

# Logging and Monitoring
loguru>=0.7.0

# CLI Interface
click>=8.1.0
rich>=13.0.0
typer>=0.9.0

# File Processing
pathlib2>=2.3.7

# JSON and YAML
pyyaml>=6.0
jsonschema>=4.17.0

# Development Tools (optional)
jupyter>=1.0.0
ipython>=8.0.0

# Testing Utilities
factory-boy>=3.2.0
faker>=19.0.0
