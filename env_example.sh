# ====================================================================
# .env.example - Arquivo de configuração de ambiente
# Sistema de Geração de Testes Unitários com LangChain e Azure ChatGPT
# 
# Instruções:
# 1. Copie este arquivo para .env
# 2. Preencha com suas credenciais Azure OpenAI
# 3. Ajuste as configurações conforme necessário
# ====================================================================

# Azure OpenAI Configurations
AZURE_OPENAI_API_KEY=sua_chave_azure_aqui
AZURE_OPENAI_ENDPOINT=https://seu-recurso.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4

# Alternative: Standard OpenAI (se não usar Azure)
# OPENAI_API_KEY=sua_chave_openai_aqui
# OPENAI_MODEL=gpt-4

# System Configurations
MAX_TOKENS=2000
TEMPERATURE=0.1
TOP_P=0.95
FREQUENCY_PENALTY=0.0
PRESENCE_PENALTY=0.0

# Test Generation Settings
TEST_FRAMEWORK=pytest
INCLUDE_FIXTURES=true
TEST_EDGE_CASES=true
TEST_EXCEPTIONS=true
USE_PARAMETRIZE=true
MIN_COVERAGE=80

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
LOG_FILE=logs/test_generator.log

# Development Settings
DEBUG_MODE=false
VERBOSE=true

# Agent Configuration
MAX_ITERATIONS=5
HANDLE_PARSING_ERRORS=true
AGENT_TYPE=ZERO_SHOT_REACT_DESCRIPTION

# Output Settings
OUTPUT_DIRECTORY=generated_tests
BACKUP_GENERATED_TESTS=true
AUTO_SAVE_RESULTS=true

# Performance Settings
REQUEST_TIMEOUT=30
MAX_RETRIES=3
RETRY_DELAY=1

# Quality Assurance
ENABLE_SYNTAX_CHECK=true
ENABLE_COVERAGE_ANALYSIS=true
ENABLE_BEST_PRACTICES_CHECK=true

# Metrics and Monitoring
ENABLE_METRICS=true
METRICS_FILE=metrics/generation_metrics.json
EXPORT_METRICS_FORMAT=json

# Security Settings
SAFE_MODE=true
ALLOWED_IMPORTS=pytest,unittest,mock,datetime,os,sys,json
RESTRICTED_OPERATIONS=exec,eval,import,__import__
