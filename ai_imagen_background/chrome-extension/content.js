/**
 * Higgsfield Multi-Select — Shift-click range selection + keyboard shortcuts
 *
 * Created: 2026-02-24 16:38 JST
 * Modified: 2026-02-24 20:20 JST
 * Session: d1f76181-4684-4828-834c-65b55aadf8cd
 *
 * Features:
 *   1. Shift+click: select all visible images between last click and current
 *   2. Delete key: click the Delete button (works in grid and picture viewer)
 *   3. Enter key: confirm the "Yes, delete forever" dialog
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
 *     Delete is an ICON-ONLY button (trash SVG, no text) — identified by
 *     its SVG path starting with "M4.75 6.5L5.72041 20.32"
 *
 *   Picture viewer:
 *     div[role="dialog"].fixed.z-101 with "Asset showcase"
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

  /**
   * Find the visible "Yes, delete forever" confirmation button.
   * The Radix dialog has: form.dialog-actions > button[type="submit"]
   */
  function findDeleteConfirmButton() {
    const btn = document.querySelector(
      'div[role="dialog"][data-state="open"] form.dialog-actions button[type="submit"]'
    );
    if (btn && btn.offsetParent !== null) return btn;

    // Fallback: find by button text content
    const buttons = document.querySelectorAll(
      'div[role="dialog"] button'
    );
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

  /**
   * Check if a delete confirmation dialog is currently open.
   */
  function isDeleteDialogOpen() {
    return findDeleteConfirmButton() !== null;
  }

  // ─── Delete button detection ──────────────────────────────────────

  /**
   * Find the Delete action in the UI. Higgsfield uses multiple patterns:
   *   1. Radix context menu: div.menu-item.menu-item-danger (right-click menu)
   *   2. Text-based button: button with text "Delete"
   *   3. Icon-only toolbar button: trash SVG in bottom action bar
   */
  function findDeleteButton() {
    // Method 1: Radix context menu item with danger class (the actual delete)
    const menuItem = document.querySelector(
      ".menu-item.menu-item-danger"
    );
    if (menuItem && menuItem.offsetParent !== null) return menuItem;

    // Method 2: any visible element with "Delete" text in a menu/dialog
    const allEls = document.querySelectorAll(
      '[role="menuitem"], [role="option"], .menu-item, button'
    );
    for (const el of allEls) {
      const text = el.textContent.trim();
      if (text === "Delete" && el.offsetParent !== null) {
        return el;
      }
    }

    // Method 3: trash icon button in the selection toolbar
    const toolbar = document.querySelector(
      'div[data-ignore-marquee="true"]'
    );
    if (toolbar) {
      const toolbarBtns = toolbar.querySelectorAll("button");
      for (const btn of toolbarBtns) {
        if (btn.textContent.trim() === "" && btn.querySelector("svg")) {
          const paths = btn.querySelectorAll("svg path");
          for (const p of paths) {
            const d = p.getAttribute("d") || "";
            if (d.includes("20.32") || d.includes("6.5H21")) {
              return btn;
            }
          }
        }
      }
    }

    // Method 4: broader search for trash icon in any visible button
    const buttons = document.querySelectorAll("button");
    for (const btn of buttons) {
      if (btn.offsetParent === null) continue;
      if (btn.textContent.trim() !== "") continue;
      const paths = btn.querySelectorAll("svg path");
      for (const p of paths) {
        const d = p.getAttribute("d") || "";
        if (d.includes("5.72041") && d.includes("20.32")) {
          return btn;
        }
      }
    }

    return null;
  }

  /**
   * Check if any images are currently selected.
   * Detects by: checkbox aria-checked state OR presence of the selection toolbar.
   */
  function hasSelectedImages() {
    // Check toolbar presence (most reliable — the toolbar shows "N selected")
    const toolbar = document.querySelector(
      'div[data-ignore-marquee="true"]'
    );
    if (toolbar && toolbar.offsetParent !== null) return true;

    // Fallback: check checkbox states
    const cards = getVisibleCards();
    return cards.some((c) => isChecked(c));
  }

  /**
   * Check if the picture viewer dialog is open.
   */
  function isPictureViewerOpen() {
    const dialogs = document.querySelectorAll('div[role="dialog"]');
    for (const d of dialogs) {
      if (
        d.textContent.includes("Asset showcase") ||
        d.textContent.includes("Overview")
      ) {
        if (d.offsetParent !== null || d.style.display !== "none") {
          return true;
        }
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
    // Ignore if user is typing in an input/textarea
    const tag = event.target.tagName;
    if (tag === "INPUT" || tag === "TEXTAREA" || event.target.isContentEditable) {
      return;
    }

    if (event.key === "Delete" || event.key === "Backspace") {
      // If delete confirmation dialog is open, confirm it
      if (isDeleteDialogOpen()) {
        event.preventDefault();
        const confirmBtn = findDeleteConfirmButton();
        if (confirmBtn) {
          simulateClick(confirmBtn);
          log("Confirmed delete via keyboard");
        }
        return;
      }

      // If images are selected or picture viewer is open, click Delete
      if (hasSelectedImages() || isPictureViewerOpen()) {
        const deleteBtn = findDeleteButton();
        if (deleteBtn) {
          event.preventDefault();
          simulateClick(deleteBtn);
          log("Triggered delete via keyboard");
        }
      }
    }

    if (event.key === "Enter") {
      // If delete confirmation dialog is open, confirm it
      if (isDeleteDialogOpen()) {
        event.preventDefault();
        const confirmBtn = findDeleteConfirmButton();
        if (confirmBtn) {
          simulateClick(confirmBtn);
          log("Confirmed delete via Enter");
        }
      }
    }
  }

  // ─── Logging ──────────────────────────────────────────────────────

  function log(msg) {
    console.log(
      "%c[HF Multi-Select]%c " + msg,
      "color: #f920d1; font-weight: bold",
      "color: inherit"
    );
  }

  // ─── Init ─────────────────────────────────────────────────────────

  document.addEventListener("click", handleClick, true);
  document.addEventListener("keydown", handleKeyDown, true);

  log("Loaded — shift+click to range-select, Delete/Enter for quick delete");
})();
