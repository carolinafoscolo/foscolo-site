const FOOTER_TEXT = {
  pt: {
    name: "Fóscolo & Company Editora",
    slogan: "Ideias acendem. Histórias permanecem.",
    rights: "Todos os direitos reservados."
  },
  en: {
    name: "Fóscolo & Company Press",
    slogan: "Ideas ignite. Stories remain.",
    rights: "All rights reserved."
  },
  es: {
    name: "Fóscolo & Company Editorial",
    slogan: "Las ideas encienden. Las historias permanecen.",
    rights: "Todos los derechos reservados."
  },
  fr: {
    name: "Fóscolo & Company Éditions",
    slogan: "Les idées s’allument. Les histoires demeurent.",
    rights: "Tous droits réservés."
  },
  zh: {
    name: "Fóscolo & Company 出版社",
    slogan: "思想点燃。故事长存。",
    rights: "版权所有。"
  }
};

function loadFooter(){
  const lang = getCurrentLanguage();
  const text = FOOTER_TEXT[lang];

  document.getElementById("site-footer").innerHTML = `
    <footer>
      <img src="../assets/images/selo-editorial.png" alt="Fóscolo & Company">
      <p><strong>${text.name}</strong></p>
      <p>${text.slogan}</p>
      <p>© 2026 ${text.name}. ${text.rights}</p>
    </footer>
  `;
}

document.addEventListener("DOMContentLoaded", loadFooter);