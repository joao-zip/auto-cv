# Arquitetura do Sistema — AutoCV

O AutoCV é projetado como um pipeline determinístico de geração de documentos a partir de uma fonte única de dados estruturados.

```
                  ┌──────────────────────┐
                  │  data/profile.yaml   │
                  │   (Master Profile)   │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │   src/validator.py   │  ──> Validação de tipos, chaves
                  └──────────┬───────────┘      obrigatórias e paridade pt/en
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
   [ Modo Padrão ]                     [ Modo Tailor ]
   `generate`                          `tailor` + `ats_analyzer.py`
            │                                 │
            │                          (Extrai keywords da JD,
            │                           calcula scores por tag,
            │                           ranqueia bullets e projetos)
            │                                 │
            └────────────────┬────────────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │   src/generator.py   │
                  │  (Montagem Typst)    │
                  └──────────┬───────────┘
                             │  Injeta layout, fontes locais,
                             │  estilos e texto sanitizado
                             ▼
                  ┌──────────────────────┐
                  │     typst compile    │
                  └──────────┬───────────┘
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
   output/CV_portugues.pdf           output/CV_english.pdf
            │                                 │
            └────────────────┬────────────────┘
                             │
                             ▼
                ┌─────────────────────────┐
                │   GitHub Actions CI/CD  │
                │     (GitHub Release)    │
                └────────────┬────────────┘
                             │
                             ▼
                joao-zip.github.io (Site Pessoal)
```

---

## Componentes Principais

### 1. `data/profile.yaml` (Master Profile)
A única fonte de verdade. Contém informações pessoais, educação, experiências profissionais, liderança, projetos, competências técnicas e certificações.

### 2. `src/validator.py` (Garantia de Qualidade de Dados)
Executado antes de compilações críticas ou deploys. Garante que:
- Chaves essenciais existam (`personal.name`, `personal.email`, etc.).
- Todos os campos textuais possuam equivalentes bilíngues não-vazios (`pt` e `en`).
- Listas de bullets e tags estejam preenchidas.

### 3. `src/ats_analyzer.py` (Inteligência ATS e Matching Léxico)
- Mantém um vocabulário técnico categorizado (`TECH_TAXONOMY`) com suporte a regex para identificar linguagens, frameworks, bancos, práticas e arquiteturas.
- Mapeia tags internas dos bullets e projetos para palavras-chave (`TAG_TO_KEYWORDS`).
- Calcula pontuação de aderência (`match_score`), palavras-chave atendidas e termos ausentes.

### 4. `src/generator.py` (Engine Typst)
- Lê os dados validados.
- Aplica regras de preset (`tech`, `trainee`, `full`):
  - **`tech`**: Foco em stack de desenvolvimento, backend, engenharia de software e projetos de código. 1 página rígida.
  - **`trainee`**: Inclui liderança comunitária/militar e projetos com apelo acadêmico/institucional. 1 página rígida.
  - **`full`**: Versão estendida completa sem limite rígido de 1 página.
- Gera o código-fonte Typst em memória (ou arquivo temporário) e invoca o binário `typst compile` apontando para o diretório de fontes `fonts/`.

### 5. `templates/resume.typ`
Contém definições de layout reutilizáveis em Typst:
- Formatação de títulos de seção (`#section_heading`).
- Grids de duas colunas para alinhamento de datas e instituições/empresas.
- Definição de margens e paleta de cores neutra (tons de cinza e azul escuro) otimizada para legibilidade ATS e impressão.
