"""
Temporary clean download_image function.
"""
import base64
import time
from pathlib import Path
from typing import Optional


def click_download_button(page):
    """
    Click the download button in the floating bottom bar.

    Uses attribute selectors to find the toolbar container (bottom-4, fixed),
    then falls back to scanning all page buttons for download text/icon.

    Args:
        page: Playwright page object

    Returns:
        True if download initiated, False otherwise
    """
    result = page.evaluate("""
        () => {
            // Primary: find bottom toolbar via partial class match
            const container = document.querySelector('[class*="bottom-4"][class*="fixed"]');
            const buttons = container ? [...container.querySelectorAll('button')] : [];
            let dlBtn = buttons[5]; // 0-indexed: 6th button

            // Fallback 1: button with download text or aria-label
            if (!dlBtn) {
                dlBtn = [...document.querySelectorAll('button')].find(b => {
                    const t = (b.textContent || '').trim().toLowerCase();
                    const a = (b.getAttribute('aria-label') || '').toLowerCase();
                    return t.includes('download') || a.includes('download');
                });
            }

            // Fallback 2: button with download SVG icon (arrow-down)
            if (!dlBtn) {
                dlBtn = [...document.querySelectorAll('button')].find(b =>
                    b.querySelector('svg') && !b.textContent.trim()
                );
            }

            // Fallback 3: last button in bottom-4 modal (likely download)
            if (!dlBtn) {
                const modal = document.querySelector('[class*="bottom-4"][class*="left-4"]');
                if (modal) {
                    const modalBtns = [...modal.querySelectorAll('button')];
                    dlBtn = modalBtns[modalBtns.length - 1];
                }
            }

            // Diagnostic: return info about what was found
            if (!dlBtn) {
                const allBtns = [...document.querySelectorAll('button')];
                const modal = document.querySelector('[class*="bottom-4"][class*="left-4"]');
                const modalBtns = modal ? [...modal.querySelectorAll('button')] : [];
                return {
                    success: false,
                    debug: {
                        containerFound: !!container,
                        buttonsInContainer: buttons.length,
                        allButtonsCount: allBtns.length,
                        modalButtons: modalBtns.map(b => b.getAttribute('aria-label') || b.textContent.trim().slice(0, 20))
                    }
                };
            }

            dlBtn.click();
            return { success: true };
        }
    """)

    if result.get("success"):
        print("  [OK] Clicked download button")
        return True

    debug = result.get("debug", {})
    print(f"  [WARN] Could not find download button: containerFound={debug.get('containerFound')}, buttonsInContainer={debug.get('buttonsInContainer')}, allButtonsCount={debug.get('allButtonsCount')}")
    if debug.get("modalButtons"):
        print(f"       Modal buttons: {debug['modalButtons']}")
    return False


def download_image(page, output_dir: str, filename: str, image_index: int = 1, timeout: int = 60000) -> Optional[str]:
    """
    Download a generated image from Higgsfield.

    Workflow:
    1. Select image in feed (#soul-feed-scroll)
    2. Intercept image network response after clicking download
    3. Fallback: extract image from page DOM via canvas

    Args:
        page: Playwright page object
        output_dir: Directory to save the image
        filename: Output filename (e.g., "candidate_001.png")
        image_index: 1-based index of the image in the feed (default 1)
        timeout: Download timeout in milliseconds

    Returns:
        Path to downloaded file, or None if download failed
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    final_path = output_path / filename

    print(f"  Downloading image {image_index} to: {final_path}")

    try:
        # Step 1: Select the image
        if not select_image(page, image_index):
            print(f"  [ERROR] Could not select image {image_index}")
            return None

        time.sleep(1.0)  # Wait for selection + modal to fully render

        # Step 2: Intercept image responses
        img_data = None
        pending_response = [None]  # Using list to allow nonlocal assignment

        def handle_response(response):
            content_type = response.headers.get("content-type", "")
            url = response.url
            if "image" in content_type or any(url.endswith(ext) for ext in (".png", ".jpg", ".jpeg", ".webp")):
                pending_response[0] = response.body()

        page.on("response", handle_response)

        # Step 3: Click download button
        if not click_download_button(page):
            page.remove_listener("response", handle_response)
            print("  [ERROR] Could not click download button")
            return None

        # Step 4: Wait for image response (5 second max)
        start_time = time.time()
        while pending_response[0] is None and (time.time() - start_time) < 5:
            time.sleep(0.3)

        page.remove_listener("response", handle_response)
        img_data = pending_response[0]

        # Step 5: If no network response, extract from page DOM via canvas
        if not img_data:
            img_data = page.evaluate("""
                () => {
                    // Find the largest (displayed) image on page
                    const imgs = [...document.querySelectorAll('img')];
                    let best = null;
                    for (const img of imgs) {
                        if (img.complete && img.naturalWidth > 100) {
                            if (!best || img.naturalWidth > best.naturalWidth) {
                                best = img;
                            }
                        }
                    }
                    if (!best) return null;

                    // Try canvas extraction (works for any img)
                    try {
                        const canvas = document.createElement('canvas');
                        canvas.width = best.naturalWidth;
                        canvas.height = best.naturalHeight;
                        const ctx = canvas.getContext('2d');
                        ctx.drawImage(best, 0, 0);
                        return canvas.toDataURL('image/png').split(',')[1];
                    } catch(e) {
                        return null;
                    }
                }
            """)
            if img_data:
                img_data = base64.b64decode(img_data)
            else:
                print("  [ERROR] Could not extract image from DOM or network")
                return None

        # Step 6: Save image
        with open(final_path, "wb") as f:
            f.write(img_data)
        print(f"  [OK] Downloaded: {final_path}")
        return str(final_path)

    except Exception as e:
        print(f"  [ERROR] Download failed: {e}")
        return None
