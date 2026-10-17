// Cover Letter - Kuri
// Candidatura: Backend Ruby on Rails
// Candidato: João Pedro Martins Oliveira

#import "@preview/fontawesome:0.5.0": *

#let brand_color = rgb("#201235")
#let text_dark = rgb("#1e293b")
#let text_muted = rgb("#64748b")
#let border_color = rgb("#e2e8f0")

#set page(
  paper: "a4",
  margin: (x: 2.3cm, top: 2.4cm, bottom: 2.4cm),
)

#set text(
  font: ("Crimson Pro", "Libertinus Serif", "DejaVu Serif"),
  size: 11.5pt,
  fill: text_dark,
  lang: "pt",
  hyphenate: false,
)

#set par(
  justify: true,
  leading: 0.72em,
  spacing: 1.45em,
)

// Helper links
#let ext_link(url, content) = {
  link(url)[#content]
}

// ---------------- HEADER ----------------
#grid(
  columns: (1fr, auto),
  align: (left + horizon, right + horizon),
  [
    #text(size: 22pt, weight: "bold", fill: brand_color)[João Pedro Martins Oliveira]
  ],
  [
    #align(right)[
      #text(size: 9.5pt, fill: text_muted)[
        #fa-location-dot() São José dos Campos, SP \
        #link("mailto:oliveira.joaop@proton.me")[#fa-envelope() oliveira.joaop\@proton.me] \
        #fa-phone() +55 (12) 99669-1514
      ]
    ]
  ]
)

#v(2pt)

// Links line
#text(size: 9.5pt, fill: brand_color)[
  #link("https://linkedin.com/in/joao-zip")[#fa-linkedin() linkedin.com/in/joao-zip]
  #h(12pt)
  #link("https://github.com/joao-zip")[#fa-github() github.com/joao-zip]
  #h(12pt)
  #link("https://joao-zip.github.io")[#fa-globe() joao-zip.github.io]
]

#v(-3pt)
#line(length: 100%, stroke: 1.5pt + brand_color)
#v(6pt)

// ---------------- METADATA / RECIPIENT ----------------
#grid(
  columns: (1fr, auto),
  align: (left + top, right + top),
  [
    #text(size: 10pt, fill: text_muted)[Para:] \
    #text(size: 11.5pt, weight: "bold", fill: brand_color)[Kuri]
  ],
  [
    #text(size: 10pt, fill: text_muted)[Data:] \
    #text(size: 10.5pt, weight: "medium", fill: text_dark)[Setembro de 2026]
  ]
)

#v(6pt)

// Subject Badge / Block
#rect(
  width: 100%,
  fill: rgb("#201235").lighten(94%),
  stroke: (left: 3pt + brand_color, rest: 0.5pt + border_color),
  radius: (right: 4pt),
  inset: (x: 12pt, y: 8pt),
)[
  #text(size: 10.5pt, weight: "bold", fill: brand_color)[Assunto:]
  #h(6pt)
  #text(size: 10.5pt, weight: "semibold", fill: text_dark)[Candidatura — Vaga Backend Ruby on Rails]
]

#v(8pt)

// ---------------- LETTER BODY ----------------

Olá,

Meu nome é João, sou estudante de Ciência da Computação (já formado em ciência e tecnologia via dupla diplomação da UNIFESP) e atualmente estagio como desenvolvedor fullstack em ASP.Net Core (C\#/.Net). Vi a vaga de vocês e me interessei bastante pela proposta da Kuri, é um problema técnico interessante com um efeito prático bem concreto, e isso pesou na decisão de aplicar.

Sei que a vaga pede experiência sólida em Ruby on Rails, e para ser honesto, minha experiência prática é em .Net, não em Rails. Mas boa parte do que a vaga pede é relativo a conceitos e nisso eu creio já ter bagagem: construí APIs REST para integrar sistemas internos da empresa onde estagio, como a API consumida por um daemon desktop que também desenvolvi. Testes unitários e de integração fazem parte da minha rotina de entrega. No meu dia a dia do estágio, utilizo DDD e Clean Architecture, o que me deixa confortável com os outros requisitos da vaga.

Sobre Ruby especificamente: é uma linguagem que tenho vontade de explorar há um tempo, independente dessa vaga, e sei que a curva de aprendizado de sintaxe pesa menos do que capacidade de resolver problema e correr atrás sozinho. Estou disposto a me provar rápido nisso.

Fico à disposição para conversar e mostrar que consigo.

#v(14pt)

Atenciosamente, \
#v(2pt)
#text(size: 11.5pt, weight: "bold", fill: brand_color)[João]
