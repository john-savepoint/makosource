#!/usr/bin/env python3
"""
Higgsfield AI Image Generation Automation Script
=================================================
Created: 2026-02-20 14:20 JST
Modified: 2026-02-20 14:35 JST
Session: 0cb1e16b-ea88-43b5-ab5d-af3e4410a23a

Context:
    Automates image generation on https://higgsfield.ai/image/nano_banana_2
    using Playwright with a persistent Chrome profile so that Google OAuth
    login only needs to happen once (manually).

Workflow:
    1. First run: Opens Chrome, user signs in manually, session is saved.
    2. Subsequent runs: Loads saved session, uploads reference image(s),
       enters prompt, ensures "unlimited" toggle is on, clicks Generate
       four times with 1-second intervals.

Usage:
    # First run — sign in manually:
    python generate_images.py --login

    # Generation run:
    python generate_images.py --prompt "your prompt here" --image /path/to/image.png

    # Generation with multiple images:
    python generate_images.py --prompt "your prompt" --image img1.png --image img2.png

    # Override number of generate clicks (default 4):
    python generate_images.py --prompt "..." --image img.png --clicks 6

    # Override interval between clicks in seconds (default 1.0):
    python generate_images.py --prompt "..." --image img.png --interval 2.0

DOM Structure Notes (logged-in, as of 2026-02-20):
    - Unlimited toggle: <div>Unlimited <button role="switch" aria-checked="false/true">
    - Upload (+) button: first button inside form > fieldset, before the textarea
    - Prompt textarea: inside form > fieldset > div
    - Generate button: <button type="submit"> containing "Generate"
    - Aspect ratio: <select> with options Auto/1:1/3:4/4:3/etc.
    - Quality: <select> with options 1K/2K/4K
    - Image count: buttons with aria-label="Decrement"/"Increment", text "N/4"
"""

import argparse
import atexit
import signal
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# Persistent profile directory — stores cookies/session across runs
PROFILE_DIR = Path(__file__).parent / ".chrome_profile"
HIGGSFIELD_URL = "https://higgsfield.ai/image/nano_banana_2"

# Track browser context for cleanup on unexpected exit
_active_context = None


def _cleanup():
    """Ensure Chrome is closed on exit to prevent zombie processes."""
    global _active_context
    if _active_context:
        try:
            _active_context.close()
        except Exception:
            pass
        _active_context = None


atexit.register(_cleanup)
signal.signal(signal.SIGTERM, lambda *_: (_cleanup(), sys.exit(143)))
signal.signal(signal.SIGINT, lambda *_: (_cleanup(), sys.exit(130)))


def create_browser(playwright, headless=False):
    """Launch Chrome with persistent profile directory."""
    global _active_context

    # Remove stale lock files that cause ERR_NETWORK_CHANGED
    for lock_file in ["SingletonLock", "SingletonSocket", "SingletonCookie"]:
        lock_path = PROFILE_DIR / lock_file
        if lock_path.exists() or lock_path.is_symlink():
            lock_path.unlink(missing_ok=True)

    context = playwright.chromium.launch_persistent_context(
        user_data_dir=str(PROFILE_DIR),
        channel="chrome",
        headless=headless,
        viewport={"width": 1280, "height": 800},
        args=[
            "--disable-blink-features=AutomationControlled",
        ],
    )
    _active_context = context
    return context


def navigate_safely(page, url, timeout=30000):
    """Navigate with fallback strategy to handle ERR_NETWORK_CHANGED."""
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=timeout)
        page.wait_for_load_state("networkidle", timeout=15000)
    except PlaywrightTimeout:
        # networkidle timeout is acceptable — page may have long-polling
        pass
    except Exception as e:
        if "ERR_NETWORK_CHANGED" in str(e):
            print("  [RETRY] Network changed, retrying navigation...")
            time.sleep(2)
            page.goto(url, wait_until="domcontentloaded", timeout=timeout)
            time.sleep(3)
        else:
            raise


def login_mode(playwright):
    """
    Open the browser for manual login.
    User signs in via Google OAuth, then closes the browser.
    The session is persisted in PROFILE_DIR.
    """
    print("=" * 60)
    print("LOGIN MODE")
    print("=" * 60)
    print(f"Profile directory: {PROFILE_DIR}")
    print()
    print("A Chrome window will open. Please:")
    print("  1. Navigate to the login page if not redirected")
    print("  2. Sign in with your Google account")
    print("  3. Verify you're logged in (you should see your avatar)")
    print("  4. Close the browser window when done")
    print()

    context = create_browser(playwright, headless=False)
    page = context.pages[0] if context.pages else context.new_page()
    navigate_safely(page, HIGGSFIELD_URL)

    print("Browser opened. Waiting for you to sign in and close the window...")
    print("(The script will exit when you close the browser)")
    print()

    try:
        page.wait_for_event("close", timeout=0)
    except Exception:
        pass

    try:
        context.close()
    except Exception:
        pass

    print("Session saved. You can now run generation commands without --login.")


def wait_for_logged_in(page, timeout=10000):
    """Check if user is logged in by looking for the Upgrade link (logged-in indicator)."""
    try:
        # Logged-in users see "Upgrade" instead of "Login"
        upgrade_link = page.locator('a:has-text("Upgrade")').first
        upgrade_link.wait_for(state="attached", timeout=timeout)
        return True
    except PlaywrightTimeout:
        # Fallback: check if Login link is absent
        try:
            login_link = page.locator('a[href*="/auth/sign-in"]').first
            login_link.wait_for(state="attached", timeout=3000)
            return False
        except PlaywrightTimeout:
            return True


def ensure_unlimited_toggle(page):
    """
    Enable the 'Unlimited' toggle switch via JS for reliability.

    DOM structure (as of 2026-02-20):
        <div>
            "Unlimited"
            <button role="switch" aria-checked="false/true" class="bg-toggle-default">
        </div>
    """
    # Scroll the prompt area into view to ensure toggle is rendered
    page.evaluate("() => { const f = document.querySelector('form'); if (f) f.scrollIntoView(); }")
    time.sleep(1)

    result = page.evaluate("""
        () => {
            // Find the "Unlimited" text node — check for exact match and partial
            const walker = document.createTreeWalker(
                document.body, NodeFilter.SHOW_TEXT,
                { acceptNode: n => {
                    const t = n.textContent.trim().toLowerCase();
                    return t === 'unlimited' ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
                }}
            );
            const textNode = walker.nextNode();
            if (!textNode) {
                // Fallback: find by switch role near bottom of page (form area)
                const switches = [...document.querySelectorAll('button[role="switch"]')];
                for (const sw of switches) {
                    const parent = sw.parentElement;
                    if (parent?.textContent?.toLowerCase().includes('unlimited')) {
                        const checked = sw.getAttribute('aria-checked') === 'true';
                        if (checked) return { found: true, already_on: true, method: 'switch_scan' };
                        sw.click();
                        return { found: true, already_on: false, method: 'switch_scan' };
                    }
                }
                return { found: false, switches_count: switches.length };
            }

            // The switch button is a sibling or descendant of the text's parent
            let container = textNode.parentElement;
            for (let i = 0; i < 3 && container; i++) {
                const sw = container.querySelector('button[role="switch"]');
                if (sw) {
                    const checked = sw.getAttribute('aria-checked') === 'true';
                    if (checked) return { found: true, already_on: true };
                    sw.click();
                    return {
                        found: true,
                        already_on: false,
                        now_checked: sw.getAttribute('aria-checked') === 'true'
                    };
                }
                container = container.parentElement;
            }
            return { found: true, no_switch: true };
        }
    """)

    if not result.get("found"):
        print("  [WARN] 'Unlimited' text not found on page")
        return False
    if result.get("no_switch"):
        print("  [WARN] Found 'Unlimited' text but no switch button nearby")
        return False
    if result.get("already_on"):
        print("  [OK] Unlimited toggle already on")
        return True
    print("  [OK] Unlimited toggle enabled")
    return True


def upload_images(page, image_paths: list[str]):
    """
    Upload reference images via the '+' button in the prompt area.

    The '+' button is the first button inside the form's fieldset,
    positioned before the textarea. Clicking it opens a file chooser.
    If that doesn't work, falls back to hidden input[type="file"].
    """
    for img_path in image_paths:
        path = Path(img_path).resolve()
        if not path.exists():
            print(f"  [ERROR] Image not found: {path}")
            continue

        print(f"  Uploading: {path.name}")

        # Try to trigger file chooser via the '+' button (first button in the form)
        try:
            with page.expect_file_chooser(timeout=5000) as fc_info:
                page.evaluate("""
                    () => {
                        const form = document.querySelector('form');
                        if (!form) return false;
                        const btn = form.querySelector('fieldset button');
                        if (btn) { btn.click(); return true; }
                        return false;
                    }
                """)
            file_chooser = fc_info.value
            file_chooser.set_files(str(path))
            print(f"  [OK] Uploaded: {path.name}")
            time.sleep(2)
        except PlaywrightTimeout:
            print(f"  [WARN] File chooser didn't open, trying hidden input...")
            try:
                file_input = page.locator('input[type="file"]').first
                file_input.set_input_files(str(path))
                print(f"  [OK] Uploaded via file input: {path.name}")
                time.sleep(2)
            except Exception as e:
                print(f"  [ERROR] Failed to upload {path.name}: {e}")


def enter_prompt(page, prompt_text: str):
    """Type the generation prompt into the text area using JS for reliability."""
    # Find and focus the textbox, then use Playwright keyboard input
    found = page.evaluate("""
        () => {
            // Try multiple selectors for the prompt input
            const selectors = [
                'textarea[placeholder*="Describe"]',
                '[role="textbox"]',
                '[contenteditable="true"]',
                'textarea',
            ];
            for (const sel of selectors) {
                const el = document.querySelector(sel);
                if (el) {
                    el.focus();
                    el.click();
                    return { found: true, tag: el.tagName, selector: sel };
                }
            }
            return { found: false };
        }
    """)

    if not found.get("found"):
        print("  [ERROR] Could not find prompt textbox")
        return

    time.sleep(0.3)

    # Use keyboard to select all and delete, then type
    page.keyboard.press("Control+a")
    page.keyboard.press("Backspace")
    time.sleep(0.2)
    page.keyboard.type(prompt_text, delay=10)

    truncated = prompt_text[:60] + ("..." if len(prompt_text) > 60 else "")
    print(f"  [OK] Prompt entered: {truncated}")


def click_generate(page, times: int = 4, interval: float = 1.0):
    """
    Click the Generate button multiple times with a delay between clicks.

    The Generate button's accessible name is "Generate N" where N is the
    credit cost. Uses JS click as primary method since the button's text
    content is dynamically rendered and Playwright selectors can time out.
    """
    # Wait for page to be interactive after prompt entry
    time.sleep(2)

    for i in range(times):
        try:
            clicked = page.evaluate("""
                () => {
                    const btns = [...document.querySelectorAll('button')];
                    // Try "Generate" first, fall back to submit button
                    let gen = btns.find(b => b.textContent.includes('Generate'));
                    if (!gen) gen = document.querySelector('button[type="submit"]');
                    if (!gen) gen = document.querySelector('aside button');
                    if (!gen) return {
                        success: false,
                        reason: 'not_found',
                        debug: btns.slice(-10).map(b => b.textContent.trim().substring(0, 40))
                    };
                    if (gen.disabled) return { success: false, reason: 'disabled' };
                    gen.scrollIntoView({ block: 'nearest' });
                    gen.click();
                    return { success: true };
                }
            """)

            if clicked["success"]:
                print(f"  [OK] Generate clicked ({i + 1}/{times})")
            elif clicked["reason"] == "disabled":
                print(f"  [WAIT] Generate button disabled, waiting...")
                # Poll until enabled, up to 30 seconds
                for _ in range(30):
                    time.sleep(1)
                    result = page.evaluate("""
                        () => {
                            const btns = [...document.querySelectorAll('button')];
                            const gen = btns.find(b => b.textContent.includes('Generate'));
                            if (!gen || gen.disabled) return false;
                            gen.click();
                            return true;
                        }
                    """)
                    if result:
                        print(f"  [OK] Generate clicked ({i + 1}/{times})")
                        break
                else:
                    print(f"  [ERROR] Generate button stayed disabled for 30s")
                    break
            else:
                debug = clicked.get("debug", [])
                print(f"  [ERROR] Generate button not found on page")
                if debug:
                    print(f"  [DEBUG] Last 10 buttons: {debug}")
                break

            if i < times - 1:
                time.sleep(interval)

        except Exception as e:
            print(f"  [ERROR] Click {i + 1} failed: {e}")
            break


def run_generation(playwright, args):
    """Main generation workflow."""
    print("=" * 60)
    print("GENERATION MODE")
    print("=" * 60)

    if not PROFILE_DIR.exists():
        print("[ERROR] No saved session found. Run with --login first.")
        sys.exit(1)

    context = create_browser(playwright, headless=False)
    page = context.pages[0] if context.pages else context.new_page()

    print(f"Navigating to {HIGGSFIELD_URL}...")
    navigate_safely(page, HIGGSFIELD_URL)
    # Wait for SPA hydration
    time.sleep(3)

    # Verify logged in
    print("Checking login status...")
    if not wait_for_logged_in(page):
        print("[ERROR] Not logged in. Run with --login first to save your session.")
        context.close()
        sys.exit(1)
    print("  [OK] Logged in")

    # Step 1: Ensure unlimited toggle is ON
    print("\nStep 1: Checking unlimited toggle...")
    ensure_unlimited_toggle(page)

    # Step 2: Upload images
    if args.image:
        print("\nStep 2: Uploading images...")
        upload_images(page, args.image)
    else:
        print("\nStep 2: No images to upload (use --image to add)")

    # Step 3: Enter prompt
    if args.prompt:
        print("\nStep 3: Entering prompt...")
        enter_prompt(page, args.prompt)
    else:
        print("\nStep 3: No prompt specified (use --prompt to add)")

    # Step 4: Click Generate
    print(f"\nStep 4: Clicking Generate {args.clicks} times "
          f"(interval: {args.interval}s)...")
    click_generate(page, times=args.clicks, interval=args.interval)

    print("\n" + "=" * 60)
    print("GENERATION COMPLETE")
    print("=" * 60)
    print(f"Sent {args.clicks} generation requests.")
    print("The browser will stay open so you can monitor results.")
    print("Close the browser window when done.")

    try:
        page.wait_for_event("close", timeout=0)
    except Exception:
        pass

    try:
        context.close()
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(
        description="Automate image generation on Higgsfield AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # First time: login and save session
  python generate_images.py --login

  # Generate with prompt and image
  python generate_images.py --prompt "a futuristic cityscape" --image reference.png

  # Generate with multiple images, 6 clicks, 2s interval
  python generate_images.py --prompt "blend these styles" -i a.png -i b.png --clicks 6 --interval 2.0

  # Prompt only, no image upload
  python generate_images.py --prompt "a serene japanese garden at sunset"
        """,
    )

    parser.add_argument(
        "--login",
        action="store_true",
        help="Open browser for manual login (first-time setup)",
    )
    parser.add_argument(
        "--prompt", "-p",
        type=str,
        default="",
        help="The image generation prompt",
    )
    parser.add_argument(
        "--image", "-i",
        action="append",
        default=[],
        help="Path to reference image(s) to upload (can specify multiple times)",
    )
    parser.add_argument(
        "--clicks", "-c",
        type=int,
        default=4,
        help="Number of times to click Generate (default: 4)",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Seconds between Generate clicks (default: 1.0)",
    )

    args = parser.parse_args()

    with sync_playwright() as playwright:
        if args.login:
            login_mode(playwright)
        else:
            if not args.prompt and not args.image:
                parser.print_help()
                print("\n[ERROR] Provide at least --prompt or --image, or use --login")
                sys.exit(1)
            run_generation(playwright, args)


if __name__ == "__main__":
    main()
