(() => {
  if (!("scrollRestoration" in history)) return;

  const key = `scroll-position:${location.pathname}${location.search}`;

  const probe = `${key}:probe`;
  try {
    sessionStorage.setItem(probe, "");
    sessionStorage.removeItem(probe);
  } catch {
    return;
  }

  history.scrollRestoration = "manual";

  addEventListener("pagehide", () => {
    try {
      sessionStorage.setItem(key, `${scrollX},${scrollY}`);
    } catch {
      // Keep native navigation working when storage is unavailable.
    }
  });

  addEventListener("pageshow", () => {
    if (location.hash) return;

    try {
      const saved = sessionStorage.getItem(key);
      if (!saved) return;

      const [x, y] = saved.split(",").map(Number);
      if (Number.isFinite(x) && Number.isFinite(y)) {
        requestAnimationFrame(() => scrollTo({ left: x, top: y, behavior: "instant" }));
      }
    } catch {
      // Keep the page usable if stored state is invalid or unavailable.
    }
  });
})();
