# Especificação do Schema — data/profile.yaml

O arquivo `data/profile.yaml` deve seguir rigorosamente a especificação abaixo.

---

## 1. Estrutura Geral das Seções

```yaml
personal:
  name: str
  email: str
  phone: str
  links:
    - name: str
      url: str
      display: str

education:
  institution: str
  degree: { pt: str, en: str }
  period: { pt: str, en: str }
  location: { pt: str, en: str }
  coursework: { pt: str, en: str }
  tcc: { pt: str, en: str }

experience:
  - id: str
    company: str
    role: { pt: str, en: str }
    period: { pt: str, en: str }
    location: { pt: str, en: str }
    tech_stack: [str, ...]
    bullets:
      - id: str
        tags: [str, ...]
        pt: str
        en: str

leadership: # (opcional, usado em trainee/full)
  - id: str
    name: { pt: str, en: str } # ou str simples
    role: { pt: str, en: str }
    period: { pt: str, en: str }
    location: { pt: str, en: str }
    tags: [str, ...]
    bullets:
      - id: str
        tags: [str, ...]
        pt: str
        en: str

projects: # (opcional)
  - id: str
    name: str
    role: { pt: str, en: str }
    link: { url: str, display: str } # opcional
    tech_stack: [str, ...]
    tags: [str, ...]
    bullets:
      - pt: str
        en: str

skills:
  languages: { pt: str, en: str }
  frameworks_tech: { pt: str, en: str }
  databases: { pt: str, en: str }
  practices: { pt: str, en: str }
  technologies: { pt: str, en: str }

awards: # (opcional)
  pt: [str, ...]
  en: [str, ...]
```

---

## 2. Padrão de Redação de Bullets (Impacto + Contexto + Métricas)

Ao redigir novos bullets para experiências e projetos, siga a fórmula clássica de engenharia:
> **[Verbo de ação no passado] + [O que foi construído/implementado] + [Tecnologias utilizadas] + [Impacto quantitativo ou qualitativo gerado].**

### Exemplo em Português (`pt`):
> *"Desenvolvi rotinas assíncronas escaláveis utilizando Azure Functions e RabbitMQ para processamento em background e desacoplamento de documentos contábeis;"*

### Exemplo em Inglês (`en`):
> *"Developed scalable asynchronous background processing pipelines using Azure Functions and RabbitMQ for decoupled accounting document ingestion;"*

---

## 3. Taxonomia de Tags para Matching ATS

Cada bullet e projeto possui uma lista de `tags`. O `src/ats_analyzer.py` faz a ponte entre essas tags e os requisitos de vagas. Utilize sempre que possível as tags padronizadas:

| Categoria | Tags Recomendadas |
|---|---|
| **Linguagens** | `csharp`, `golang`, `cplusplus`, `python`, `typescript`, `javascript`, `sql`, `c` |
| **Backend & Web** | `backend`, `fullstack`, `vue`, `react`, `rest api`, `desktop`, `regex` |
| **Cloud & DevOps** | `cloud`, `azure`, `docker`, `kubernetes`, `ci/cd`, `linux`, `rabbitmq` |
| **Arquitetura & Qualidade** | `architecture`, `ddd`, `clean_code`, `testing`, `tdd`, `distributed`, `microservices` |
| **Sistemas & Compiladores** | `compilers`, `ast`, `systems`, `automation` |
| **Liderança & Social** | `leadership`, `teamwork`, `discipline`, `social-impact`, `mentorship`, `education` |
