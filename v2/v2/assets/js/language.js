const LANGUAGES = {
  pt: {
    home: "index.html",
    about: "sobre.html",
    publications: "publicacoes.html",
    projects: "projetos.html",
    manifesto: "manifesto.html",
    contact: "contato.html"
  },
  en: {
    home: "index.html",
    about: "about.html",
    publications: "publications.html",
    projects: "projects.html",
    manifesto: "manifesto.html",
    contact: "contact.html"
  },
  es: {
    home: "index.html",
    about: "sobre.html",
    publications: "publicaciones.html",
    projects: "proyectos.html",
    manifesto: "manifiesto.html",
    contact: "contacto.html"
  },
  fr: {
    home: "index.html",
    about: "a-propos.html",
    publications: "publications.html",
    projects: "projets.html",
    manifesto: "manifeste.html",
    contact: "contact.html"
  },
  zh: {
    home: "index.html",
    about: "about.html",
    publications: "publications.html",
    projects: "projects.html",
    manifesto: "manifesto.html",
    contact: "contact.html"
  }
};

function getCurrentLanguage(){
  const path = window.location.pathname;

  if(path.includes("/pt/")) return "pt";
  if(path.includes("/en/")) return "en";
  if(path.includes("/es/")) return "es";
  if(path.includes("/fr/")) return "fr";
  if(path.includes("/zh/")) return "zh";

  return "pt";
}

function getCurrentPage(){
  const file = window.location.pathname.split("/").pop() || "index.html";

  const currentLang = getCurrentLanguage();
  const pages = LANGUAGES[currentLang];

  for(const key in pages){
    if(pages[key] === file){
      return key;
    }
  }

  return "home";
}

function changeLanguage(language){
  localStorage.setItem("foscolo_language", language);

  const page = getCurrentPage();
  const targetFile = LANGUAGES[language][page];

  window.location.href = "../" + language + "/"