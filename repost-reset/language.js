(() => {
  const names = { en: "English", "zh-Hans": "简体中文", "zh-Hant": "繁體中文", ja: "日本語", es: "Español", de: "Deutsch", fr: "Français" };
  const storageKey = "repost-reset.docs.language";
  const supports = language => Object.hasOwn(names, language);
  function browserLanguage(value) {
    const code = (value || "").toLowerCase();
    if (/^zh(?:-|$)/.test(code)) return /^zh-(?:hant|tw|hk|mo)(?:-|$)/.test(code) ? "zh-Hant" : "zh-Hans";
    const language = code.split("-")[0];
    return supports(language) ? language : null;
  }
  const select = document.getElementById("language-select");
  const label = document.getElementById("current-language");
  const descriptions = { en: "TokCleaner help, privacy and terms of use.", "zh-Hans": "TokCleaner 使用帮助、隐私政策和使用条款。", "zh-Hant": "TokCleaner 使用說明、隱私政策與使用條款。", ja: "TokCleaner のヘルプ、プライバシー、利用規約。", es: "Ayuda, privacidad y condiciones de TokCleaner.", de: "Hilfe, Datenschutz und Nutzungsbedingungen für TokCleaner.", fr: "Aide, confidentialité et conditions de TokCleaner." };
  const accessibility = { en: ["Language", "Documentation"], "zh-Hans": ["语言", "文档导航"], "zh-Hant": ["語言", "文件導覽"], ja: ["言語", "ドキュメント"], es: ["Idioma", "Documentación"], de: ["Sprache", "Dokumentation"], fr: ["Langue", "Documentation"] };
  function applyLanguage(language, persist = false) {
    const selected = supports(language) ? language : "en";
    document.documentElement.lang = selected;
    document.querySelectorAll("[data-lang]").forEach(node => { node.hidden = node.dataset.lang !== selected; });
    select.value = selected;
    select.setAttribute("aria-label", accessibility[selected][0]);
    document.querySelector("nav").setAttribute("aria-label", accessibility[selected][1]);
    label.textContent = names[selected];
    const heading = document.querySelector(`#main [data-lang="${selected}"] h1`);
    document.title = heading.textContent === "TokCleaner" ? "TokCleaner" : "TokCleaner · " + heading.textContent;
    document.querySelector('meta[name="description"]').content = descriptions[selected];
    // Keep navigation shareable even when browser storage is disabled.
    document.querySelectorAll('a[href$=".html"], a[data-document-link]').forEach(link => {
      const url = new URL(link.getAttribute("href"), location.href);
      if (url.origin !== location.origin) return;
      link.dataset.documentLink = "true";
      url.searchParams.set("lang", selected);
      link.setAttribute("href", url.pathname + url.search + url.hash);
    });
    if (persist) {
      try { localStorage.setItem(storageKey, selected); } catch (_) {}
      const url = new URL(location.href);
      url.searchParams.set("lang", selected);
      try { history.replaceState(null, "", url.pathname + url.search + url.hash); } catch (_) {}
    }
  }
  const requested = new URLSearchParams(location.search).get("lang");
  let saved;
  try { saved = localStorage.getItem(storageKey); } catch (_) {}
  const preferred = (navigator.languages || [navigator.language]).map(browserLanguage).find(Boolean);
  applyLanguage(supports(requested) ? requested : supports(saved) ? saved : preferred || "en");
  select.addEventListener("change", () => applyLanguage(select.value, true));
})();
