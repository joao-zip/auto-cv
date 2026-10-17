# AGENTS.md — Guia de Desenvolvimento para Agentes de IA

> **Propósito Único deste Repositório:** Gerar currículos (CVs) de alta performance, visualmente profissionais, determinísticos e otimizados para sistemas ATS (Applicant Tracking Systems) em Português e Inglês para **João Pedro Martins Oliveira**.

---

## 1. Regras de Ouro (Invioláveis)

1. **Restrição Estrita de 1 Página (Single Page):**
   - Os presets principais (`tech` e `trainee`) devem caber **estritamente em 1 página A4**.
   - Qualquer edição que empurre o conteúdo para uma segunda página com 1 ou 2 linhas é considerada **falha crítica**.
   - Para controlar o tamanho: use `max_bullets`, filtre projetos menos relevantes ou ajuste espaçamento vertical conforme [docs/TYPST_GUIDE.md](docs/TYPST_GUIDE.md).

2. **Paridade Bilíngue Obrigatória (`pt` e `en`):**
   - Todas as informações de experiência, papéis, períodos, descrições, bullets e habilidades **devem** ser mantidas simultaneamente em Português (`pt`) e Inglês (`en`).
   - Nunca adicione um campo em `pt` sem seu equivalente formal e idiomático em `en`.

3. **Single Source of Truth (`data/profile.yaml`):**
   - **Nunca** codifique textos ou dados biográficos diretamente nos templates Typst ou em arquivos Python.
   - Todos os dados vêm de [data/profile.yaml](data/profile.yaml).

4. **Validação Antes de Qualquer Conclusão:**
   - Sempre execute `python3 autocv.py validate` após alterar dados.
   - Sempre compile ambas as versões (`python3 autocv.py generate --all`) para assegurar que não há quebra de sintaxe Typst ou overflow de página.

5. **Política de Git:**
   - **Nunca execute `git commit` ou `git push` por iniciativa própria.**
   - Apenas execute commits ou push sob autorização explícita do usuário.

---

## 2. Mapa do Repositório

```
auto-cv/
├── AGENTS.md                     # Este guia rápido para agentes
├── README.md                     # Documentação geral do usuário
├── autocv.py                     # CLI principal (validate, generate, tailor, score)
├── data/
│   ├── profile.yaml              # Master Profile (todos os dados do candidato)
│   └── sample_jd.txt             # Exemplo de Job Description para testes
├── docs/                         # Documentação profunda de contexto
│   ├── ARCHITECTURE.md           # Pipeline e fluxo de dados
│   ├── DATA_SCHEMA.md            # Schema detalhado e taxonomia de tags
│   ├── WORKFLOWS.md              # Playbooks passo a passo para tarefas
│   └── TYPST_GUIDE.md            # Guia de layout e tipografia Typst
├── fonts/                        # Fontes locais usadas na compilação (Crimson Pro, FontAwesome)
├── output/                       # PDFs compilados finais
├── src/
│   ├── ats_analyzer.py           # Análise léxica de JDs, keywords e scoring
│   ├── generator.py              # Engine Typst, ordenação semântica e compilação PDF
│   └── validator.py              # Validador de schema e integridade bilíngue
└── templates/
    ├── resume.typ                # Template Typst base
    └── cover_letter_kuri.typ     # Template de cover letter (referência)
```

---

## 3. Comandos Principais

```bash
# 1. Validar integridade do profile.yaml
python3 autocv.py validate

# 2. Gerar CVs padrão (tech preset, 1 página) em PT e EN
python3 autocv.py generate --all

# 3. Gerar CV individual
python3 autocv.py generate --lang pt --preset tech
python3 autocv.py generate --lang en --preset tech

# 4. Customizar CV para uma vaga específica (Tailoring com ATS)
python3 autocv.py tailor --jd vaga.txt --lang en --company "NomeEmpresa"

# 5. Apenas avaliar compatibilidade ATS com uma vaga
python3 autocv.py score --jd vaga.txt
```

---

## 4. Estratégia de Tailoring e ATS

O `src/ats_analyzer.py` e o `src/generator.py` trabalham em conjunto:
- O analisador extrai termos técnicos da Job Description contra a `TECH_TAXONOMY`.
- O gerador calcula a relevância de cada bullet point e projeto baseando-se nas `tags` declaradas no `profile.yaml`.
- Bullets com maior aderência sobem para o topo; projetos mais alinhados são priorizados.
- Se o usuário pedir para focar em uma vaga, você pode criar uma versão tailorada ou ajustar os `tags` e `bullets` no YAML para aumentar o match score.

Consulte a documentação completa em `docs/` para detalhes de implementação e esquemas.
