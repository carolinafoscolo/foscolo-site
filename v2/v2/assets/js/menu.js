const MENU_TEXT = {
  pt: {
    about: "Sobre",
    publications: "Publicações",
    projects: "Projetos",
    manifesto: "Manifesto",
    contact: "Contato"
  },
  en: {
    about: "About",
    publications: "Publications",
    projects: "Projects",
    manifesto: "Manifesto",
    contact: "Contact"
  },
  es: {
    about: "Sobre",
    publications: "Publicaciones",
    projects: "Proyectos",
    manifesto: "Manifiesto",
    contact: "Contacto"
  },
  fr: {
    about: "À propos",
    publications: "Publications",
    projects: "Projets",
    manifesto: "Manifeste",
    contact: "Contact"
  },
  zh: {
    about: "关于",
    publications: "出版物",
    projects: "项目",
    manifesto: "宣言",
    contact: "联系"
  }
};

function loadMenu(){
  const lang = getCurrentLanguage();
  const pages = LANGUAGES[lang];
  const text = MENU_TEXT[lang];

  document.getElementById("site-header").innerHTML = `
    <header class="site-header">
      <div class="topbar">
        <a href="${pages.home}">
          <img src="../assets/images/logo-horizontal.png" class="logo" alt="Fóscolo & Company">
        </a>

        <button class="menu-toggle" onclick="toggleMenu()">☰</button>

        <nav id="main-menu">
          <a href="${pages.about}">${text.about}</a>
          <a href="${pages.publications}">${text.publications}</a>
          <a href="${pages.projects}">${text.projects}</a>
          <a href="${pages.manifesto}">${text.manifesto}</a>
          <a href="${pages.contact}">${text.contact}</a>

          <div class="language-switcher">
            <button onclick="changeLanguage('pt')">PT</button>
            <button onclick="changeLanguage('en')">EN</button>
            <button onclick="changeLanguage('es')">ES</button>
            <button onclick="changeLanguage('fr')">FR</button>
            <button onclick="changeLanguage('zh')">中文</button>
          </div>
        </nav>
      </div>
    </header>
  `;
}

function toggleMenu(){
  document.getElementById("main-menu").classList.toggle("open");
}

document.addEventListener("DOMContentLoaded", loadMenu);