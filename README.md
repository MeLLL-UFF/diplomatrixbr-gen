# Diplomatrix-BR 🎓📝

[![Dataset](https://img.shields.io/badge/%F0%9F%A4%97%20Dataset-Hugging%20Face-yellow)](https://huggingface.co/datasets/melll-uff/diplomatrixbr-gen)

Desenvolvido ao longo do trabalho **Diplomatrix-BR: Um Corpus Paralelo de Redações de Autoria Humana e de LLMs no Concurso de Diplomacia Brasileira**, este corpus contém redações escritas com base nos enunciados e temas apresentados nas provas do CACD (Concurso de Admissão à Carreira Diplomática), sendo 390 geradas por 13 LLMs - `gen_essays` e 88 de candidatos aprovados - `base_essays`. Além disso, este repositório também conta com o código implementado e os resultados obtidos.

**Autores:** Rodrigo Cavalcanti João (UFF), Gabriela Casini (UFF), Gabriel Assis (UFF), Livy Real (IComp/UFAM), Daniela Vianna, Paulo Mann (UFRJ), Aline Paes (UFF)

## Índice 📚

- [Visão Geral](#visão-geral)
- [Estrutura do Repositório](#estrutura-do-repositório)
- [Dados](#dados)
- [Modelos de Linguagem](#modelos-de-linguagem)
- [Instalação e Configuração](#instalação-e-configuração)
- [Como Usar](#como-usar)
- [Métricas e Análises](#métricas-e-análises)
- [Resultados](#resultados)
- [Scripts Disponíveis](#scripts-disponíveis)
- [Estrutura dos Dados](#estrutura-dos-dados)

## Visão Geral 🔍

O Diplomatrix-BR é um corpus paralelo que contém redações dissertativo-argumentativas baseadas em questões dos concursos do Instituto Rio Branco (CACD) de 2013 a 2023. O corpus permite comparações sistemáticas entre textos produzidos por candidatos humanos aprovados e textos gerados por diferentes modelos de linguagem.

### Características principais:
- **478 redações** no total (390 geradas + 88 humanas)
- **10 anos** de questões do CACD (2013-2023)
- **13 modelos de linguagem** diferentes
- **Múltiplas temperaturas** de geração (0.3, 0.5, 0.7)
- **Métricas linguísticas abrangentes** (BLEU, BERT-Score, ROUGE, CTC)
- **Análises de correlação** entre métricas automáticas e avaliação humana

## Estrutura do Repositório 📁

```
diplomatrixbr-gen/
├── base_essays/              # Redações de candidatos aprovados
│   ├── 2013.json
│   ├── 2014.json
│   └── ...                   # Um arquivo por ano (2013-2023)
├── results/
│   ├── gen_essays/          # Redações geradas por LLMs
│   │   ├── 2013/
│   │   │   ├── CHATGPT-4o/
│   │   │   ├── COMMAND-R+/
│   │   │   ├── GEMMA-27b/
│   │   │   └── ...          # Um diretório por modelo
│   │   └── ...              # Um diretório por ano
│   ├── metrics/             # Métricas calculadas por ano
│   ├── plots/              # Gráficos e visualizações
│   └── correlations/       # Análises de correlação
│       ├── KendallCorrelation.csv
│       ├── PearsonCorrelation.csv
│       └── SpearmanCorrelation.csv
├── scripts/
│   ├── essayGeneration/    # Scripts para geração de redações
│   ├── datasetCreation/    # Scripts para criação de datasets
│   ├── generateMetrics.py  # Cálculo de métricas automáticas
│   ├── correlationMetricScore.py # Análise de correlações
│   ├── radarCharts.py      # Geração de gráficos radar
│   └── funcs.py           # Funções auxiliares
├── Diplomatrix.json        # Dataset completo com métricas
├── requirements.txt        # Dependências do projeto
├── gen.sh                 # Script de geração automatizada
└── run.sh                # Script principal de execução
```

## Dados 📊

### Redações Humanas (`base_essays/`)
- **88 redações** de candidatos aprovados no CACD
- Distribuídas ao longo de **10 anos** (2013-2023)
- Incluem **notas atribuídas** pelos avaliadores
- Contêm **métricas linguísticas** pré-calculadas

### Redações Geradas (`results/gen_essays/`)
- **390 redações** geradas por 13 modelos diferentes
- **3 temperaturas** de geração por modelo (0.3, 0.5, 0.7)

### Atenção:
As redações geradas por modelos grandes (>9b) foram obtidas através da plataforma **[LMArena](https://lmarena.ai/)**.
Não nos responsabilizamos pela geração de redações de modelos sem o uso de APIs

As redações usadas durante o desenvolvimento da pesquisa estão disponíveis neste repositório para fins de reprodução de experimentos

## Modelos de Linguagem 🤖

O corpus inclui redações geradas pelos seguintes modelos:

1. **ChatGPT-4o** (OpenAI)
2. **Command R+** (Cohere)
3. **Gemma-27b** (Google)
4. **Gemma-9b** (Google)
5. **Llama-405b** (Meta)
6. **Llama-8b** (Meta)
7. **Mixtral-8x22b** (Mistral AI)
8. **Mixtral-8x7b** (Mistral AI)
9. **Phi-3-Mini** (Microsoft)
10. **Phi-4** (Microsoft)
11. **Qwen2-72b** (Alibaba)
12. **Qwen2-7b** (Alibaba)
13. **Sabia** (Maritaca AI)

## Instalação e Configuração ⚙️

### Pré-requisitos
- Python 3.8+
- CUDA (opcional, para aceleração GPU)
- Tokens de API para modelos proprietários

### Instalação
```bash
# Clone o repositório
git clone https://github.com/MeLLL-UFF/diplomatrixbr-gen.git
cd diplomatrixbr-gen

# Instale as dependências
pip install -r requirements.txt
```

### Configuração de APIs
Configure as chaves de API necessárias:
- **Hugging Face Token** para modelos open-source
- **OpenAI API Key** para ChatGPT
- **Cohere API Key** para Command R+
- **Maritalk API Key** para Sabia

## Como Usar 🚀
### Observação:
**Verifique se o comando está adequado ao seu sistema operacional!**

No Windows:
```bash
python run/this/python_script.py...
```

No Linux/MacOS:
```bash
python3 run/this/python_script.py...
```

### Geração de Redações
```bash
# Para gerar redações com múltiplos modelos
chmod +x gen.sh
./gen.sh

# Para gerar com um modelo específico
python3 -m scripts.essayGeneration.gen --model_id "microsoft/Phi-3-small-8k-instruct" --hf_token YOUR_TOKEN --temps 0.3 0.5 0.7 --output_path "PHI-3-SMALL/"
```

### Cálculo de Métricas
```bash
# Calcular métricas para todas as redações
python scripts/generateMetrics.py

# Análise de correlações
python scripts/correlationMetricScore.py
```

### Visualizações
```bash
# Gerar gráficos radar
python scripts/radarCharts.py
```

## Métricas e Análises 📈

### Métricas Automáticas
- **BLEU:** Precisão baseada em n-gramas
- **BERT-Score:** Similaridade semântica usando embeddings
- **ROUGE:** Recall baseado em n-gramas e sequências
- **CTC (Factual Consistency):** Consistência factual do texto

### Análises de Correlação
- **Pearson:** Correlação linear
- **Spearman:** Correlação por ranking
- **Kendall:** Concordância por pares

### Visualizações Disponíveis
- Gráficos radar por modelo e ano
- Análises de correlação entre métricas
- Distribuições de scores por temperatura

## Scripts Disponíveis 🛠️

### Geração de Redações
- `scripts/essayGeneration/gen.py` - Geração com modelos Hugging Face
- `scripts/essayGeneration/generate_chatgpt_essays.py` - Geração com ChatGPT
- `scripts/essayGeneration/generate_command_essays.py` - Geração com Command R+
- `scripts/essayGeneration/generate_sabia_essays.py` - Geração com Sabia

### Processamento de Dados
- `scripts/datasetCreation/criacao_dfs_modelos.py` - Criação de datasets dos modelos
- `scripts/datasetCreation/criacao_dfs_redacoes.py` - Criação de datasets das redações
- `scripts/generateMetrics.py` - Cálculo de métricas automáticas
- `scripts/correlationMetricScore.py` - Análise de correlações

### Visualização
- `scripts/radarCharts.py` - Geração de gráficos radar
- `scripts/extraction.ipynb` - Notebook para análise exploratória

### Utilitários
- `scripts/funcs.py` - Funções auxiliares e constantes

## Estrutura dos Dados 🗃️

### Formato JSON das Redações Base
```json
{
  "Maximum_Score": 60.0,
  "Question_Statement": "...",
  "Candidates": [
    {
      "Name": "Nome do Candidato",
      "Score": 52.5,
      "Essay": "Texto da redação...",
    }
  ]
}
```

### Dataset Consolidado
O arquivo `Diplomatrix.json` contém todo o corpus estruturado com:
- Redações de candidatos com notas e métricas
- Questões e enunciados por ano
- Metadados temporais e contextuais

## Citação 📚

Se você usar este corpus em sua pesquisa, por favor cite:

```bibtex
@article{diplomatrixbr2024,
  title={Diplomatrix-BR: Um Corpus Paralelo de Redações de Autoria Humana e de LLMs no Concurso de Diplomacia Brasileira},
  author={João, Rodrigo Cavalcanti and Casini, Gabriela and Assis, Gabriel and Real, Livy and Vianna, Daniela and Mann, Paulo and Paes, Aline},
  year={2024}
}
```