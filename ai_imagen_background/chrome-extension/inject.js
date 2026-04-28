/**
 * inject.js — Bypasses prompt character limit on Higgsfield AI
 *
 * Previous approach (String wrapper) crashed because typeof new String()
 * returns "object" not "string", breaking downstream code.
 *
 * New approach: Keep the store untouched. When the Generate button is
 * clicked, temporarily set prompt to the first 100 chars, let validation
 * pass, then restore the full prompt before the async API call fires.
 */
(function () {
  "use strict";

  let _toastContainer = null;
  function toast(msg) {
    if (!document.body) return;
    if (!_toastContainer) {
      _toastContainer = document.createElement("div");
      _toastContainer.style.cssText =
        "position:fixed;top:12px;right:12px;z-index:99999;display:flex;flex-direction:column;gap:6px;pointer-events:none;";
      document.body.appendChild(_toastContainer);
    }
    const t = document.createElement("div");
    t.textContent = msg;
    t.style.cssText =
      "background:#1a1a2e;color:#f920d1;border:1px solid #f920d1;padding:8px 14px;" +
      "border-radius:8px;font-size:12px;font-family:monospace;max-width:500px;word-break:break-all;" +
      "box-shadow:0 4px 12px rgba(0,0,0,0.5);opacity:1;transition:opacity 0.3s;pointer-events:none;";
    _toastContainer.appendChild(t);
    setTimeout(function () {
      t.style.opacity = "0";
      setTimeout(function () { t.remove(); }, 300);
    }, 6000);
    console.log("[HF]", msg);
  }

  // Suppress limit toasts
  new MutationObserver(function (muts) {
    for (const m of muts) for (const n of m.addedNodes) {
      if (n.nodeType === 1 && (n.textContent || "").indexOf("Prompt should be less than") !== -1) {
        n.style.display = "none";
        try { n.remove(); } catch (e) {}
      }
    }
  }).observe(document.documentElement, { childList: true, subtree: true });

  // ─── Find all store references ────────────────────────────────
  // Returns array of {hook, state} where hook.memoizedState has .prompt
  // We return the HOOK so we can replace hook.memoizedState entirely
  function findPromptHooks() {
    const results = [];
    const seen = new WeakSet();

    const els = [
      document.querySelector("[id='hf:tour-image-prompt']"),
      document.querySelector("[id='hf:image-form-submit']"),
      document.querySelector("form"),
    ].filter(Boolean);

    for (const el of els) {
      const fk = Object.keys(el).find(k => k.startsWith("__reactFiber"));
      if (!fk) continue;

      let fiber = el[fk];
      for (let d = 0; d < 80 && fiber; d++) {
        let hook = fiber.memoizedState;
        while (hook) {
          const s = hook.memoizedState;
          if (s && typeof s === "object" && !Array.isArray(s) &&
              "prompt" in s && !seen.has(s)) {
            seen.add(s);
            results.push(hook); // the hook, not the state
          }
          hook = hook.next;
        }
        fiber = fiber.return;
      }
    }
    return results;
  }

  // ─── Click interception ───────────────────────────────────────
  // Listen for ALL clicks in capture phase. When the Generate button
  // is clicked and prompt is long, temporarily swap prompt to short
  // string, then restore via microtask.

  document.addEventListener("click", function (e) {
    let el = e.target;
    while (el) {
      if (el.tagName === "BUTTON" && (el.textContent || "").indexOf("Generate") !== -1) {
        handleGenerateClick();
        return;
      }
      el = el.parentElement;
    }
  }, true);

  function handleGenerateClick() {
    const hooks = findPromptHooks();
    toast("Generate clicked — found " + hooks.length + " hooks");

    if (hooks.length === 0) return;

    const toRestore = [];

    for (const hook of hooks) {
      const state = hook.memoizedState;
      const realPrompt = state.prompt;
      if (!realPrompt || typeof realPrompt !== "string" || realPrompt.length < 14000) {
        toast("Prompt under limit (" + (realPrompt ? realPrompt.length : 0) + ") — no bypass needed");
        continue;
      }

      // The property is writable:false but configurable:true.
      // Use defineProperty to temporarily redefine it as a short string.
      const shortPrompt = realPrompt.substring(0, 100);

      try {
        Object.defineProperty(state, "prompt", {
          value: shortPrompt,
          writable: false,
          configurable: true,
          enumerable: true,
        });
        toRestore.push({ state: state, realPrompt: realPrompt });
        toast("Spoofed via defineProperty: " + realPrompt.length + " → " + shortPrompt.length);
      } catch (e) {
        toast("defineProperty failed: " + e.message);

        // Fallback: replace entire hook.memoizedState
        try {
          const fakeState = Object.assign({}, state);
          Object.defineProperty(fakeState, "prompt", {
            value: shortPrompt,
            writable: false,
            configurable: true,
            enumerable: true,
          });
          hook.memoizedState = fakeState;
          toRestore.push({ hook: hook, realState: state, state: null });
          toast("Spoofed via hook replacement");
        } catch (e2) {
          toast("All spoof methods failed: " + e2.message);
        }
      }
    }

    if (toRestore.length === 0) return;

    // Restore via microtask
    Promise.resolve().then(function () {
      for (const item of toRestore) {
        if (item.state) {
          // Restore via defineProperty on the original state
          Object.defineProperty(item.state, "prompt", {
            value: item.realPrompt,
            writable: false,
            configurable: true,
            enumerable: true,
          });
          toast("Restored: " + item.realPrompt.length + " chars for API");
        } else if (item.hook) {
          // Restore hook.memoizedState
          item.hook.memoizedState = item.realState;
          toast("Restored hook state");
        }
      }
    });
  }

  toast("inject.js loaded");
})();
