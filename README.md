# Fóscolo & Company Edições

Site editorial independente, em português, inglês, espanhol, francês e chinês.

Publicado em https://www.foscolo.com.br pelo GitHub Pages. A branch `main` contém o site pronto: não há dependência de framework, banco de dados ou serviço de formulário.

## Editar e publicar

1. Edite os textos em `content/{pt,en,es,fr,zh}.json`.
2. Edite a estrutura compartilhada em `scripts/build.py`, os estilos em `assets/site.css` e o menu em `assets/site.js`.
3. Execute `python3 scripts/build.py` para gerar as páginas e o sitemap.
4. Execute `python3 tests/check_site.py` para verificar destinos locais, idiomas, imagens e metadados.
5. Confira o site com `python3 -m http.server 8080`.
6. Envie o código-fonte e as páginas geradas juntos ao GitHub.

As URLs anteriores permanecem disponíveis. `content/legacy.json` preserva o ensaio inaugural e o manifesto nos cinco idiomas. Imagens antigas continuam nos endereços originais para não quebrar referências externas; o novo layout usa `assets/images/`.

## Conteúdo de setembro de 2026

- Catálogo e páginas próprias para **Notes on Care, Risk & Knowledge** e **Todos ou nenhum? — Livro I: A matéria aprende a respirar**.
- Notes: edição brasileira em inglês, miolo de 64 páginas e formato 10 × 15 cm; ofertas internacionais separadas. Preço e estoque ficam no anúncio da Amazon.
- Todos ou nenhum?: 13 poemas e 3 crônicas ensaísticas; obra em preparação, sem data ou venda inventada. As imagens são da prova editorial, não uma capa final.
- Caderno: índice, ensaio inaugural preservado e novo texto sobre o prólogo de Todos ou nenhum?.
- Repertório, projetos, autora, imprensa e contato.
- Sem inscrição de newsletter enquanto não houver serviço configurado.

## Decisões técnicas

- HTML estático completo: leitura e navegação funcionam sem JavaScript.
- Uma folha de estilos e um menu progressivamente aprimorado.
- Fontes Bebas Neue, Libre Baskerville e Noto Serif SC hospedadas localmente, com licenças OFL incluídas.
- Imagens WebP, dimensões explícitas, carregamento adiado fora do destaque.
- Navegação por teclado, link para pular ao conteúdo, preferência de movimento reduzido e impressão.
- Canonical, hreflang, Open Graph, JSON-LD e sitemap gerados a partir das mesmas rotas.

Contato: contato@foscolo.com — endereço mantido conforme a atualização institucional do repositório de 11/08/2026.

## Verificação no navegador

Com Playwright instalado, execute `CHROMIUM_PATH=/caminho/do/chromium node tests/browser.cjs`. O teste percorre as 71 rotas do sitemap em 390 e 1440 pixels e verifica menu, Escape e navegação sem JavaScript. A fonte chinesa inclui os caracteres usados no conteúdo de setembro; amplie o subconjunto local ao adicionar novos caracteres.
