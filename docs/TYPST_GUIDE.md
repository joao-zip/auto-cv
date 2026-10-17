# Guia Typst & Tipografia — AutoCV

O AutoCV utiliza o **Typst** para gerar PDFs vetoriais com precisão tipográfica, tempos de compilação na ordem de milissegundos e layout estruturado.

---

## 1. Fontes Tipográficas

O projeto inclui fontes no diretório `fonts/`, passadas via `--font-path fonts` para a compilação:

- **Crimson Pro** (`fonts/CrimsonPro-Variable.ttf`, `fonts/CrimsonPro-Italic-Variable.ttf`):
  Fonte serifada elegante e profissional para títulos, nomes e corpo de texto.
- **FontAwesome** (`fonts/fa-brands-400.ttf`, `fonts/fa-solid-900.ttf`, `fonts/fa-regular-400.ttf`):
  Ícones de contato (email, telefone, LinkedIn, GitHub, site) no cabeçalho.

---

## 2. Parâmetros de Layout por Preset

Definidos em `src/generator.py`:

| Parâmetro | Preset `tech` | Preset `trainee` | Preset `full` |
|---|---|---|---|
| **Tamanho da Fonte Base** | `10.2pt` | `10pt` | `10.5pt` |
| **Leading (Entrelinha)** | `0.43em` | `0.41em` | `0.45em` |
| **Margens Laterais (X)** | `1.25cm` | `1.25cm` | `1.25cm` |
| **Margens Top/Bottom** | `0.85cm` | `0.9cm` | `0.9cm` |
| **Liderança Inclusa** | `False` (por padrão) | `True` | `True` |
| **Projetos Padrão** | `wiredpanda`, `goblin` | `wiredpanda` | Todos |

---

## 3. Práticas Recomendadas de Estilização em Typst

1. **Espaçamento Negativo Controlado**:
   O Typst utiliza `#v(...)` para espaçamento vertical. Quando necessário compactar linhas para caber estritamente em 1 página, reduções sutis como `#v(-2pt)` ou `#v(-3pt)` entre cabeçalhos e listas de bullets são permitidas.

2. **Sanitização de Caracteres**:
   Caracteres com significado especial em Typst (`#`, `@`) devem ser escapados pelo método `_sanitize()` em `src/generator.py`.

3. **Links e Acessibilidade**:
   Links para LinkedIn, GitHub e Portfólio utilizam `#link("url")[texto]`, garantindo que o PDF contenha links clicáveis e legíveis por parsers de texto.
