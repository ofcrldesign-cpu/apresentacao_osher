# OSHER Açaí Shop — Brandkit & Apresentação Interativa

> **Açaí + Sorvete. Do seu jeito.**  
> Landing Page institucional e apresentação interativa da marca OSHER Açaí Shop, reunindo identidade visual, posicionamento estratégico de mercado, personas, catálogo de produtos e aplicações reais de delivery e mídias sociais.

---

## 📋 Sumário
- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades Principais](#-funcionalidades-principais)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Pré-requisitos](#-pré-requisitos)
- [Como Executar Localmente](#-como-executar-localmente)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Validação e Testes](#-validação-e-testes)
- [Publicação em Produção](#-publicação-em-produção)
- [Estrutura de Diretórios](#-estrutura-de-diretórios)
- [Licença e Créditos](#-licença-e-créditos)

---

## 📖 Sobre o Projeto

A **OSHER Açaí Shop** é uma marca de alimentação rápida e premium sediada no Distrito Federal (Guará/Brasília), combinando açaí artesanal de altíssima cremosidade, sorvetes finos e personalização total pelo cliente.

Esta aplicação web foi desenvolvida com foco em alta performance visual, microinterações refinadas e fidelidade estética às diretrizes de marca (Brandkit), proporcionando uma experiência imersiva para clientes, parceiros e investidores.

---

## ✨ Funcionalidades Principais

- **🎨 Brandkit Completo & Interativo:**
  - Visualização da logo oficial nas versões Dark, Light, Monocromática e Símbolo (SVGs responsivos).
  - Tabela de regras de uso da marca, zona de proteção e exemplos de cores incorretas.
  - Paleta de cores oficial (Roxo Açaí Profundo, Creme Vanilla, Dourado Ouro, etc.) com botão de cópia de código HEX em 1 clique.
  - Sandbox de tipografia interativa para teste em tempo real das fontes da marca (*Cormorant Garamond*, *Montserrat* e *Outfit*).

- **📱 Simulador de Mídias Sociais & Stories:**
  - Player interativo de Stories com barra de progresso animada, controle de play/pause e mute/unmute.
  - Grid de postagens do Feed do Instagram com efeito hover e overlay informativo.

- **🍧 Vitrine de Produtos & Delivery:**
  - Filtro interativo por categorias de produtos (Copos Especiais, Tigelas/Bowls, Combos e Embalagens).
  - Simulador de aplicativo de delivery com abas temáticas (iFood, Keeta, 99Food) e mockups em alta definição.

- **👥 Pesquisa de Mercado & Mapeamento de Personas:**
  - Apresentação visual detalhada das personas do público-alvo (jovens estudantes, casais esportistas, famílias).

- **🖼️ Lightbox Modal & Engine Parallax:**
  - Visualizador Lightbox em tela cheia com navegação rápida via teclado (`ESC`) para fotos e mockups.
  - Motor suave de profundidade parallax baseado em `requestAnimationFrame`.
  - Animações de entrada com *Intersection Observer* e barra superior de progresso de leitura.

---

## 🛠️ Tecnologias Utilizadas

- **HTML5 Semântico:** Estruturação acessível, tags semânticas e metatags para SEO e redes sociais (OpenGraph).
- **CSS3 Moderno:** Custom properties (variáveis CSS), design system responsivo, glassmorphism e animações via `@keyframes`.
- **JavaScript Puro (Vanilla ES6+):** Lógica modular e reativa, sem dependências de frameworks pesados, garantindo carregamento instantâneo.
- **Tipografia:** Google Fonts (*Cormorant Garamond*, *Montserrat*, *Outfit*).
- **Formatos Gráficos:** SVGs otimizados, WebP/JPG/PNG em alta resolução.

---

## ⚙️ Pré-requisitos

Para visualizar e testar o projeto localmente, você precisa apenas de:
- Um navegador web moderno atualizado (Google Chrome, Mozilla Firefox, Microsoft Edge ou Safari).
- *(Opcional)* Python 3.x ou Node.js para rodar um servidor HTTP local.

---

## 🚀 Como Executar Localmente

Como a aplicação é 100% estática, não há necessidade de etapas complexas de compilação:

### Opção 1: Via Servidor Python (Recomendado)
```bash
# Na raiz do projeto, inicie um servidor HTTP local:
python -m http.server 3000
```
Em seguida, abra seu navegador no endereço: [http://localhost:3000](http://localhost:3000)

### Opção 2: Via Node.js (npx serve)
```bash
# Executa sem necessidade de instalar dependências globais:
npx serve .
```

### Opção 3: Extensão Live Server (VS Code)
1. Abra a pasta do projeto no VS Code.
2. Clique com o botão direito no arquivo `index.html`.
3. Selecione **Open with Live Server**.

### Opção 4: Abertura Direta
Dê um duplo clique no arquivo `index.html` para abri-lo diretamente em seu navegador padrão.

---

## 🔐 Variáveis de Ambiente

O projeto é executado inteiramente no navegador e não requer variáveis confidenciais para funcionar.  
Consulte o arquivo [.env.example](.env.example) para configurações opcionais em caso de deploy ou integrações externas futuras.

---

## 🧪 Validação e Testes

O repositório inclui um script de integridade estática que analisa o `index.html` e a presença de todos os assets referenciados:

```bash
# Executar validação de estrutura e links de assets:
python check_html.py
```

Também é possível verificar a sintaxe do arquivo JavaScript:
```bash
# Validação sintática do app.js:
node -c app.js
```

---

## 🌐 Publicação em Produção

O projeto está pronto para ser hospedado gratuitamente em qualquer provedor de hospedagem estática:

- **GitHub Pages:**
  1. Vá em **Settings** > **Pages** no repositório GitHub.
  2. Em **Source**, selecione a branch `main` e a pasta `/ (root)`.
  3. Salve e aguarde a publicação automática da URL.

- **Vercel / Netlify / Cloudflare Pages:**
  - Basta conectar o repositório do GitHub. Não é necessário comando de build (*Leave build command empty*), e o diretório raiz é `.`.

---

## 📁 Estrutura de Diretórios

```text
├── index.html          # Documento principal da Landing Page e Brandkit
├── style.css           # Folha de estilos unificada, tokens e design system
├── app.js              # Lógica interativa (Parallax, Stories, Lightbox, Filtros)
├── check_html.py       # Script utilitário de validação e integridade
├── .gitignore          # Regras de exclusão para o Git
├── .env.example        # Arquivo de exemplo para configurações opcionais
├── README.md           # Documentação técnica e operacional do projeto
├── assets/             # Logotipos SVG, mockups, fotos de produtos e mídias
│   ├── osher_logo_h_dark.svg
│   ├── osher_logo_h_light.svg
│   ├── osher_logo_symbol.svg
│   ├── osher_store_ambiance.jpg
│   └── ...
└── .docs/              # Documentos de apoio e referências originais de design
```

---

## 📄 Licença e Créditos

Desenvolvido para **OSHER Açaí Shop**.  
Todos os direitos reservados à marca e seus criadores.
