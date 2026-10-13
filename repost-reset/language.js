(() => {
  function applyLanguage(language) {
    const selected = language === "zh-Hans" ? "zh-Hans" : "en";
    document.documentElement.lang = selected;
    document.querySelectorAll("[data-lang]").forEach(node => { node.hidden = node.dataset.lang !== selected; });
    document.querySelectorAll("[data-set-language]").forEach(button => { button.setAttribute("aria-pressed", String(button.dataset.setLanguage === selected)); });
    // Persist a preference only; never store account information here.
    try { localStorage.setItem("repost-reset.docs.language", selected); } catch (_) {}
  }
  let saved;
  try { saved = localStorage.getItem("repost-reset.docs.language"); } catch (_) {}
  const browserLanguages = navigator.languages || [navigator.language || "en"];
  const preferred = browserLanguages.find(language => /^(zh|en)(-|$)/i.test(language)) || "en";
  applyLanguage(saved === "en" || saved === "zh-Hans" ? saved : /^zh/i.test(preferred) ? "zh-Hans" : "en");
  document.querySelectorAll("[data-set-language]").forEach(button => { button.addEventListener("click", () => applyLanguage(button.dataset.setLanguage)); });
})();
