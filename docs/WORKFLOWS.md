# Workflows Operacionais — AutoCV

Instruções práticas para agentes de IA e desenvolvedores realizarem as operações mais frequentes no repositório.

---

## Workflow 1: Adicionar ou Atualizar uma Experiência

1. **Abrir `data/profile.yaml`**:
   - Localize a chave `experience`.
   - Adicione o item seguindo o schema: `id`, `company`, `role` (pt/en), `period` (pt/en), `location` (pt/en), `tech_stack` e `bullets`.
   - Certifique-se de que cada bullet tenha `tags` expressivas e textos em `pt` e `en`.

2. **Validar o arquivo**:
   ```bash
   python3 autocv.py validate
   ```
   *Se houver erros, corrija as chaves antes de prosseguir.*

3. **Gerar e Verificar Visualmente**:
   ```bash
   python3 autocv.py generate --all
   ```

4. **Verificar Limite de 1 Página**:
   - Se o número de páginas for maior que 1, execute o ajuste fino (ver Workflow 4).

---

## Workflow 2: Customizar CV para uma Vaga Específica (Tailoring)

Quando o usuário fornecer a descrição de uma vaga (Job Description - JD):

1. **Salvar a descrição ou passar via CLI**:
   Salve o texto em um arquivo temporário (ex: `vaga.txt`) ou passe via `--jd`.

2. **Executar o Tailor**:
   ```bash
   python3 autocv.py tailor --jd vaga.txt --lang en --company "NomeEmpresa"
   ```

3. **Analisar o Relatório ATS gerado no terminal**:
   - Observe o `ATS Match Score (%)`.
   - Verifique `Missing / Unmatched Keywords`.
   - Se houver competências ausentes que o João de fato possui, edite `data/profile.yaml` para incorporar os termos ou tags adequadas e rode novamente.

4. **PDF gerado**:
   O arquivo final estará em `output/CV_Joao_Oliveira_NomeEmpresa_EN.pdf`.

---

## Workflow 3: Diagnosticar e Corrigir Overflow de Página (1 Página Rígida)

Se o CV gerado ultrapassar 1 página:

1. **Opção A (Controle de Bullets no CLI)**:
   Passe `--max-bullets 3` ou `--max-bullets 2` no comando:
   ```bash
   python3 autocv.py generate --all --max-bullets 3
   ```

2. **Opção B (Seleção de Projetos)**:
   No preset `tech`, selecione apenas os 2 projetos mais relevantes:
   ```bash
   python3 autocv.py generate --all --projects wiredpanda,goblin
   ```

3. **Opção C (Ajuste de Tipografia/Margens no `src/generator.py`)**:
   - No método `render_typst` de `src/generator.py`, ajuste os parâmetros do preset:
     - `font_size`: reduzir de `10.2pt` para `10pt` ou `9.8pt`.
     - `line_leading`: reduzir de `0.43em` para `0.40em`.
     - `margins`: ajustar `top: 0.8cm, bottom: 0.8cm`.
     - Espaçamentos verticais `#v(-3pt)`.
