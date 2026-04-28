/**
 * Higgsfield Power Tools — Multi-select, keyboard shortcuts, prompt unlimiter
 *
 * Created: 2026-02-24 16:38 JST
 * Modified: 2026-03-17 22:40 JST
 * Session: d1f76181-4684-4828-834c-65b55aadf8cd
 *
 * Features:
 *   1. Shift+click: select all visible images between last click and current
 *   2. Delete key: click the Delete button (works in grid and picture viewer)
 *   3. Enter key: confirm the "Yes, delete forever" dialog
 *   4. Unlimited prompt: bypasses 15,000 char limit
 *      - inject.js (MAIN world, document_start) suppresses the validation
 *      - Exposes window.hfSetPrompt(text) for programmatic use
 *   5. Ctrl+Shift+D: bulk delete all visible failed/NSFW generations
 *      - Finds delete buttons in card footers inside #soul-feed-scroll
 *      - Clicks each → confirms "Yes, delete forever" → waits → repeats
 *      - Also callable from console: window.hfBulkDelete()
 *
 * DOM structure (as of 2026-02-24):
 *   Card: div[@container group ...][data-asset-id]
 *     └── div.z-10.absolute (checkbox overlay, visible on hover)
 *         └── div.cursor-pointer (click wrapper)
 *             └── button[role="checkbox"] (aria-checked="true"/"false")
 *
 *   Delete confirmation dialog (Radix):
 *     div[role="dialog"].dialog.dialog-md
 *       └── form.dialog-actions
 *           ├── button[type="reset"]  "No, keep them"
 *           └── button[type="submit"] "Yes, delete forever"
 *
 *   Bottom action bar (when images selected):
 *     div[data-ignore-marquee].fixed! containing: "N selected", Download, etc.
 *     Delete: .menu-item.menu-item-danger (Radix context menu)
 *
 *   Prompt editor (Lexical):
 *     div#hf\:tour-image-prompt[data-lexical-editor][contenteditable]
 *     Limit enforced in form submit handler, not the editor itself.
 */

(function () {
  "use strict";

  let lastClickedAssetId = null;

  // ─── Image card helpers ───────────────────────────────────────────

  function getVisibleCards() {
    return Array.from(document.querySelectorAll("div[data-asset-id]"));
  }

  function sortCardsByPosition(cards) {
    return cards.sort((a, b) => {
      const ra = a.getBoundingClientRect();
      const rb = b.getBoundingClientRect();
      const rowDiff = ra.top - rb.top;
      if (Math.abs(rowDiff) > 20) return rowDiff;
      return ra.left - rb.left;
    });
  }

  function getCheckbox(card) {
    return card.querySelector('button[role="checkbox"]');
  }

  function getCheckboxWrapper(card) {
    const cb = getCheckbox(card);
    if (!cb) return null;
    return cb.closest("div.cursor-pointer") || cb.parentElement;
  }

  function isChecked(card) {
    const cb = getCheckbox(card);
    return cb && cb.getAttribute("aria-checked") === "true";
  }

  function simulateClick(element) {
    element.dispatchEvent(
      new MouseEvent("click", {
        bubbles: true,
        cancelable: true,
        view: window,
      })
    );
  }

  function findCard(element) {
    return element.closest("div[data-asset-id]");
  }

  // ─── Delete confirmation detection ────────────────────────────────

  function findDeleteConfirmButton() {
    const btn = document.querySelector(
      'div[role="dialog"][data-state="open"] form.dialog-actions button[type="submit"]'
    );
    if (btn && btn.offsetParent !== null) return btn;

    const buttons = document.querySelectorAll('div[role="dialog"] button');
    for (const b of buttons) {
      if (
        b.textContent.trim().toLowerCase().includes("delete forever") &&
        b.offsetParent !== null
      ) {
        return b;
      }
    }
    return null;
  }

  function isDeleteDialogOpen() {
    return findDeleteConfirmButton() !== null;
  }

  // ─── Delete button detection ──────────────────────────────────────

  function findDeleteButton() {
    const menuItem = document.querySelector(".menu-item.menu-item-danger");
    if (menuItem && menuItem.offsetParent !== null) return menuItem;

    const allEls = document.querySelectorAll(
      '[role="menuitem"], [role="option"], .menu-item, button'
    );
    for (const el of allEls) {
      if (el.textContent.trim() === "Delete" && el.offsetParent !== null) {
        return el;
      }
    }

    const toolbar = document.querySelector('div[data-ignore-marquee="true"]');
    if (toolbar) {
      for (const btn of toolbar.querySelectorAll("button")) {
        if (btn.textContent.trim() === "" && btn.querySelector("svg")) {
          for (const p of btn.querySelectorAll("svg path")) {
            const d = p.getAttribute("d") || "";
            if (d.includes("20.32") || d.includes("6.5H21")) return btn;
          }
        }
      }
    }

    return null;
  }

  function hasSelectedImages() {
    const toolbar = document.querySelector('div[data-ignore-marquee="true"]');
    if (toolbar && toolbar.offsetParent !== null) return true;
    return getVisibleCards().some((c) => isChecked(c));
  }

  function isPictureViewerOpen() {
    for (const d of document.querySelectorAll('div[role="dialog"]')) {
      if (
        (d.textContent.includes("Asset showcase") ||
          d.textContent.includes("Overview")) &&
        (d.offsetParent !== null || d.style.display !== "none")
      ) {
        return true;
      }
    }
    return false;
  }

  // ─── Shift+click handler ──────────────────────────────────────────

  function handleClick(event) {
    const card = findCard(event.target);
    if (!card) return;

    const checkbox = getCheckbox(card);
    if (!checkbox) return;

    const wrapper = getCheckboxWrapper(card);
    if (!wrapper) return;
    if (!wrapper.contains(event.target) && event.target !== checkbox) return;

    const currentAssetId = card.getAttribute("data-asset-id");

    if (event.shiftKey && lastClickedAssetId) {
      event.preventDefault();
      event.stopPropagation();
      event.stopImmediatePropagation();

      const cards = sortCardsByPosition(getVisibleCards());
      const anchorIdx = cards.findIndex(
        (c) => c.getAttribute("data-asset-id") === lastClickedAssetId
      );
      const targetIdx = cards.findIndex(
        (c) => c.getAttribute("data-asset-id") === currentAssetId
      );

      if (anchorIdx === -1 || targetIdx === -1) {
        lastClickedAssetId = currentAssetId;
        return;
      }

      const start = Math.min(anchorIdx, targetIdx);
      const end = Math.max(anchorIdx, targetIdx);

      for (let i = start; i <= end; i++) {
        if (!isChecked(cards[i])) {
          simulateClick(getCheckboxWrapper(cards[i]));
        }
      }

      lastClickedAssetId = currentAssetId;
    } else if (!event.shiftKey) {
      lastClickedAssetId = currentAssetId;
    }
  }

  // ─── Keyboard handler ─────────────────────────────────────────────

  function handleKeyDown(event) {
    const tag = event.target.tagName;
    if (tag === "INPUT" || tag === "TEXTAREA" || event.target.isContentEditable)
      return;

    if (event.key === "Delete" || event.key === "Backspace") {
      if (isDeleteDialogOpen()) {
        event.preventDefault();
        const btn = findDeleteConfirmButton();
        if (btn) { simulateClick(btn); log("Confirmed delete via keyboard"); }
        return;
      }
      if (hasSelectedImages() || isPictureViewerOpen()) {
        const btn = findDeleteButton();
        if (btn) { event.preventDefault(); simulateClick(btn); log("Triggered delete via keyboard"); }
      }
    }

    if (event.key === "Enter" && isDeleteDialogOpen()) {
      event.preventDefault();
      const btn = findDeleteConfirmButton();
      if (btn) { simulateClick(btn); log("Confirmed delete via Enter"); }
    }
  }

  // ─── Logging ──────────────────────────────────────────────────────

  let _toastContainer = null;

  function showToast(msg) {
    if (!_toastContainer) {
      _toastContainer = document.createElement("div");
      _toastContainer.style.cssText =
        "position:fixed;top:12px;right:12px;z-index:99999;display:flex;flex-direction:column;gap:6px;pointer-events:none;";
      document.documentElement.appendChild(_toastContainer);
    }
    const toast = document.createElement("div");
    toast.textContent = "[HF] " + msg;
    toast.style.cssText =
      "background:#1a1a2e;color:#f920d1;border:1px solid #f920d1;padding:8px 14px;" +
      "border-radius:8px;font-size:12px;font-family:monospace;max-width:400px;" +
      "box-shadow:0 4px 12px rgba(0,0,0,0.5);opacity:1;transition:opacity 0.3s;pointer-events:none;";
    _toastContainer.appendChild(toast);
    setTimeout(function () {
      toast.style.opacity = "0";
      setTimeout(function () { toast.remove(); }, 300);
    }, 4000);
  }

  function log(msg) {
    console.log(
      "%c[HF Power Tools]%c " + msg,
      "color: #f920d1; font-weight: bold",
      "color: inherit"
    );
    showToast(msg);
  }

  // ─── Prompt unlimiter ───────────────────────────────────────────
  // Inject the bypass script into the page's MAIN world via a <script> tag.
  // This is necessary because content scripts run in an isolated world and
  // can't access the page's React fiber tree or Zustand stores.

  function injectMainWorldScript() {
    const script = document.createElement("script");
    script.src = chrome.runtime.getURL("inject.js");
    (document.head || document.documentElement).appendChild(script);
    script.onload = function () {
      script.remove();
      log("inject.js loaded into page context");
    };
  }

  injectMainWorldScript();

  window.hfSetPrompt = function (text) {
    const editor =
      document.getElementById("hf:tour-image-prompt") ||
      document.querySelector('[data-lexical-editor="true"]');
    if (!editor) { log("Prompt editor not found"); return 0; }
    editor.focus();
    document.execCommand("selectAll");
    document.execCommand("delete");
    document.execCommand("insertText", false, text);
    const len = editor.textContent.length;
    log("Prompt set: " + len.toLocaleString() + " chars");
    return len;
  };

  // ─── Bulk delete ─────────────────────────────────────────────────
  //
  // Finds all individual card delete buttons (the trash/delete button in each
  // card's footer overlay), clicks each one, confirms the "Yes, delete forever"
  // modal, waits for it to close, then moves to the next card.
  //
  // Trigger: Ctrl+Shift+D
  //
  // The delete buttons live inside each card's footer section:
  //   section > footer > ... > button.button.button-md.button-primary
  // with a semi-transparent white background (bg-[#FFFFFF1F]).

  function sleep(ms) {
    return new Promise(function (resolve) { setTimeout(resolve, ms); });
  }

  function waitForDeleteDialog(timeoutMs) {
    return new Promise(function (resolve) {
      var elapsed = 0;
      var interval = 100;
      var check = setInterval(function () {
        elapsed += interval;
        if (findDeleteConfirmButton()) {
          clearInterval(check);
          resolve(true);
        } else if (elapsed >= timeoutMs) {
          clearInterval(check);
          resolve(false);
        }
      }, interval);
    });
  }

  function waitForDialogClose(timeoutMs) {
    return new Promise(function (resolve) {
      var elapsed = 0;
      var interval = 100;
      var check = setInterval(function () {
        elapsed += interval;
        if (!isDeleteDialogOpen()) {
          clearInterval(check);
          resolve(true);
        } else if (elapsed >= timeoutMs) {
          clearInterval(check);
          resolve(false);
        }
      }, interval);
    });
  }

  function findCardDeleteButtons() {
    // Strategy 1: The exact selector pattern from the card footer
    // These are the delete buttons inside each generation card's overlay/footer
    var buttons = [];

    // Look for buttons with the specific Tailwind classes the user identified
    var candidates = document.querySelectorAll(
      'button.button.button-md.button-primary'
    );
    for (var i = 0; i < candidates.length; i++) {
      var btn = candidates[i];
      // Must be inside a section > footer structure (card footer, not main page)
      var footer = btn.closest("footer");
      if (!footer) continue;
      var section = footer.closest("section");
      if (!section) continue;

      // Must be inside #soul-feed-scroll (the feed area, not nav/header)
      if (!btn.closest("#soul-feed-scroll")) continue;

      // Check it looks like a delete button:
      // - has a trash icon (svg), or
      // - has short/no text content (icon-only button), or
      // - has bg-[#FFFFFF1F] class
      var text = btn.textContent.trim();
      var isIconButton = text === "" || btn.querySelector("svg");
      var hasDeleteClass = btn.className.indexOf("FFFFFF1F") !== -1;
      var looksLikeDelete = btn.querySelector('svg path[d*="M6"], svg path[d*="delete"]');

      if (isIconButton || hasDeleteClass || looksLikeDelete) {
        buttons.push(btn);
      }
    }

    // Strategy 2: broader search — any button in a card footer that triggers deletion
    if (buttons.length === 0) {
      var feedScroll = document.getElementById("soul-feed-scroll");
      if (feedScroll) {
        var allFooterBtns = feedScroll.querySelectorAll("section footer button");
        for (var j = 0; j < allFooterBtns.length; j++) {
          var b = allFooterBtns[j];
          // Skip "Recreate" and other labeled buttons
          var btnText = b.textContent.trim().toLowerCase();
          if (btnText === "recreate" || btnText === "download" || btnText.length > 20) continue;
          // Icon-only buttons or buttons with delete-like styling
          if (b.querySelector("svg") && btnText === "") {
            buttons.push(b);
          }
        }
      }
    }

    return buttons;
  }

  var _bulkDeleteRunning = false;

  async function bulkDeleteAll() {
    if (_bulkDeleteRunning) {
      log("Bulk delete already running");
      return;
    }
    _bulkDeleteRunning = true;

    var deleteButtons = findCardDeleteButtons();
    if (deleteButtons.length === 0) {
      log("No delete buttons found on visible cards");
      _bulkDeleteRunning = false;
      return;
    }

    log("Bulk delete: found " + deleteButtons.length + " cards to delete");

    var deleted = 0;
    // Process one at a time since each deletion removes the card from DOM
    // and we need to re-query after each deletion
    while (true) {
      // Re-query each iteration since DOM changes after each delete
      var btns = findCardDeleteButtons();
      if (btns.length === 0) break;

      var btn = btns[0];

      // Scroll the button into view
      btn.scrollIntoView({ block: "center", behavior: "smooth" });
      await sleep(300);

      // Click the delete button on the card
      simulateClick(btn);

      // Wait for the confirmation dialog to appear
      var dialogAppeared = await waitForDeleteDialog(3000);
      if (!dialogAppeared) {
        log("Delete dialog didn't appear, skipping...");
        // The button might not have been a delete button — remove it from consideration
        btn.setAttribute("data-hf-skip", "true");
        await sleep(200);
        continue;
      }

      await sleep(200);

      // Click "Yes, delete forever"
      var confirmBtn = findDeleteConfirmButton();
      if (confirmBtn) {
        simulateClick(confirmBtn);
        deleted++;
        log("Deleted " + deleted + " / " + (deleted + btns.length - 1) + "...");
      } else {
        log("Confirm button not found, stopping");
        break;
      }

      // Wait for dialog to close before proceeding
      var closed = await waitForDialogClose(5000);
      if (!closed) {
        log("Dialog didn't close, stopping");
        break;
      }

      // Small delay for DOM to settle after deletion
      await sleep(500);
    }

    log("Bulk delete complete: " + deleted + " cards deleted");
    _bulkDeleteRunning = false;
  }

  // Expose globally so it can be called from console too
  window.hfBulkDelete = bulkDeleteAll;

  // ─── Init ─────────────────────────────────────────────────────────

  document.addEventListener("click", handleClick, true);
  document.addEventListener("keydown", handleKeyDown, true);
  document.addEventListener("keydown", function (event) {
    // Ctrl+Shift+D — bulk delete all visible card delete buttons
    if (event.ctrlKey && event.shiftKey && event.key === "D") {
      event.preventDefault();
      bulkDeleteAll();
    }
  }, true);

  log("Loaded — shift+click, Delete/Enter, Ctrl+Shift+D bulk delete, unlimited prompt");
})();
