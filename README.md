# AutoCV - ATS-Friendly & Multilingual CV Generator

Gerador automatizado de currículos em Português e Inglês, customizados por vaga técnica e otimizados para conformidade com sistemas ATS (Applicant Tracking Systems).

Construído com Typst para compilação determinística e PDFs vetoriais estruturados.

---

## Estrutura do Projeto

```
auto-cv/
├── autocv.py             # CLI principal (generate, tailor, score)
├── data/
│   ├── profile.yaml      # Master Profile: experiências, projetos e habilidades
│   └── sample_jd.txt     # Exemplo de descrição de vaga
├── src/
│   ├── generator.py      # Engine de renderização Typst e compilação PDF
│   └── ats_analyzer.py   # Extrator de keywords e cálculo de score ATS
├── templates/
│   └── resume.typ        # Definições base do template Typst
└── output/               # PDFs finais gerados
```

---

## Como Usar

### 1. Gerar CV Padrão (Português ou Inglês)

```bash
# Versão em Português
./autocv.py generate --lang pt

# Versão em Inglês
./autocv.py generate --lang en
```

Os arquivos compilados são salvos em `output/CV_Joao_Oliveira_PT.pdf` e `output/CV_Joao_Oliveira_EN.pdf`.

---

### 2. Customizar CV para uma Vaga (tailor)

Informe o texto da vaga em arquivo ou diretamente via linha de comando:

```bash
./autocv.py tailor --jd vaga.txt --lang en --company "Empresa"
```

O comando executa:
1. Extração léxica de requisitos e tecnologias da descrição da vaga.
2. Cálculo da taxa de aderência ATS (%).
3. Identificação de palavras-chave correspondentes e termos faltantes.
4. Compilação do PDF otimizado em 1 página (`output/CV_Joao_Oliveira_Empresa_EN.pdf`).

---

### 3. Avaliar Score ATS sem Compilar PDF (score)

```bash
./autocv.py score --jd vaga.txt
```

---

## Gerenciamento de Dados

Para adicionar ou atualizar informações, edite `data/profile.yaml`. O schema suporta:
- Campos bilíngues (`pt` e `en`).
- Tags de especialidade por experiência e projeto.
- Dicionário estruturado de linguagens, frameworks, bancos e práticas de engenharia.

---

## Tecnologias

- Typst: Tipografia vetorial e compilação em tempo real.
- Python 3: Processamento de dados e análise de keywords.
- PyYAML: Formato estruturado de perfil mestre.
