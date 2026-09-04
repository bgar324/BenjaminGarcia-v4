(() => {
  if (!("scrollRestoration" in history)) return;

  const url = `${location.pathname}${location.search}${location.hash}`;
  const latestKey = `scroll-position:url:${url}`;
  const probeKey = "scroll-position:probe";

  try {
    sessionStorage.setItem(probeKey, "");
    sessionStorage.removeItem(probeKey);
  } catch {
    return;
  }

  const stateKey = "__scrollRestorationId";
  const currentState =
    history.state && typeof history.state === "object" ? history.state : {};
  const existingEntryId =
    typeof currentState[stateKey] === "string" ? currentState[stateKey] : null;
  const entryId =
    existingEntryId ??
    `${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`;

  if (!existingEntryId) {
    history.replaceState({ ...currentState, [stateKey]: entryId }, "");
  }

  const entryKey = `scroll-position:entry:${entryId}`;
  history.scrollRestoration = "manual";

  addEventListener("pagehide", () => {
    const position = `${scrollX},${scrollY}`;

    try {
      sessionStorage.setItem(entryKey, position);
      sessionStorage.setItem(latestKey, position);
    } catch {
      history.scrollRestoration = "auto";
    }
  });

  addEventListener("pageshow", () => {

    try {
      const saved =
        sessionStorage.getItem(entryKey) ?? sessionStorage.getItem(latestKey);
      if (!saved) return;

      const [x, y] = saved.split(",").map(Number);
      if (!Number.isFinite(x) || !Number.isFinite(y)) {
        history.scrollRestoration = "auto";
        return;
      }

      requestAnimationFrame(() => {
        const root = document.documentElement;
        const previousBehavior = root.style.scrollBehavior;
        root.style.scrollBehavior = "auto";
        scrollTo(x, y);
        root.style.scrollBehavior = previousBehavior;
      });
    } catch {
      history.scrollRestoration = "auto";
    }
  });
})();
