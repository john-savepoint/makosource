#!/usr/bin/env python3
"""
Higgsfield AI Video Generation Module
======================================
Created: 2026-04-06
Session: 04.1-01

Context:
    Extends generate_images.py to support video generation via Higgsfield AI.
    Videos use a different UI section and have longer generation times.

Workflow:
    1. Navigate to video section
    2. Upload reference image (hero image from article)
    3. Enter video prompt
    4. Poll for completion (videos take 30s-2min)
    5. Download video to staging area

Usage:
    from generate_videos import generate_video, VIDEO_URL

    # After hero image generation
    generate_video(page, hero_image_path, video_prompt, output_dir)

Dependencies:
    - Reuses functions from generate_images.py:
        - create_browser, navigate_safely, wait_for_logged_in, enter_prompt
"""

import time
from pathlib import Path
from typing import Optional

# Import reusable functions from generate_images
from generate_images import (
    create_browser,
    navigate_safely,
    wait_for_logged_in,
    enter_prompt,
    PROFILE_DIR,
)

# TODO: Actual video URL needs to be determined after manual Higgsfield UI exploration
# This is a placeholder based on the image generation URL pattern
VIDEO_URL = "https://higgsfield.ai/video/"

# Video-specific constants
VIDEO_POLL_INTERVAL = 2  # seconds between completion checks
VIDEO_MAX_POLLS = 60  # max polls (60 * 2s = 2 minutes max wait)
VIDEO_INITIAL_WAIT = 30  # seconds to wait before first poll (generation start time)


def upload_reference_image(page, image_path: str) -> bool:
    """
    Upload a reference image for video generation.

    TODO: Video section may have different upload UI than image section.
    This function uses the same pattern as image upload but should be
    validated after exploring the video UI.

    Args:
        page: Playwright page object
        image_path: Path to the reference image file

    Returns:
        True if upload succeeded, False otherwise
    """
    from generate_images import upload_images

    path = Path(image_path).resolve()
    if not path.exists():
        print(f"  [ERROR] Reference image not found: {path}")
        return False

    # TODO: Verify video section uses same upload mechanism
    upload_images(page, [str(path)])
    return True


def check_video_ready(page) -> bool:
    """
    Poll to check if video generation is complete.

    TODO: This function needs UI selector exploration.
    The completion indicator for videos may differ from images.
    Possible indicators:
    - Download button appearing
    - Progress bar completing
    - Video preview appearing
    - Specific completion message

    Args:
        page: Playwright page object

    Returns:
        True if video is ready for download, False otherwise
    """
    # TODO: Replace with actual selector after UI exploration
    # Placeholder: check for download button or completion indicator
    result = page.evaluate("""
        () => {
            // TODO: Find actual video completion selector
            // Possible patterns to check:
            // 1. Download button: button:has-text("Download")
            // 2. Video preview: video[src]
            // 3. Progress complete: progress[value="100"] or similar

            // Current placeholder: check for video element
            const video = document.querySelector('video');
            if (video && video.src) {
                return { ready: true, method: 'video_element' };
            }

            // Alternative: check for download button
            const buttons = [...document.querySelectorAll('button')];
            const downloadBtn = buttons.find(b =>
                b.textContent.toLowerCase().includes('download') ||
                b.getAttribute('aria-label')?.toLowerCase().includes('download')
            );
            if (downloadBtn) {
                return { ready: true, method: 'download_button' };
            }

            // Check for progress indicator
            const progress = document.querySelector('[role="progressbar"]');
            if (progress) {
                const value = progress.getAttribute('aria-valuenow') ||
                              progress.getAttribute('value');
                if (value && parseInt(value) >= 100) {
                    return { ready: true, method: 'progress_complete' };
                }
            }

            return { ready: false };
        }
    """)

    if result.get("ready"):
        print(f"  [OK] Video ready (detected via {result.get('method', 'unknown')})")
        return True
    return False


def download_video(page, output_dir: str, filename: str = "candidate_001.mp4") -> Optional[str]:
    """
    Download the generated video to the staging area.

    TODO: Video download may have different UI flow than image download.
    May need to:
    - Click a download button
    - Wait for browser download dialog
    - Handle Playwright's expect_download

    Args:
        page: Playwright page object
        output_dir: Directory to save the video
        filename: Output filename (default: candidate_001.mp4)

    Returns:
        Path to downloaded file, or None if download failed
    """
    from playwright.sync_api import expect_download

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"  Downloading video to: {output_path / filename}")

    # TODO: Verify video download mechanism after UI exploration
    # Option 1: Click download button if present
    download_clicked = page.evaluate("""
        () => {
            const buttons = [...document.querySelectorAll('button')];
            const downloadBtn = buttons.find(b =>
                b.textContent.toLowerCase().includes('download') ||
                b.getAttribute('aria-label')?.toLowerCase().includes('download')
            );
            if (downloadBtn) {
                downloadBtn.click();
                return true;
            }
            return false;
        }
    """)

    if download_clicked:
        try:
            # Wait for download to complete
            with page.expect_download(timeout=120000) as download_info:  # 2 min timeout
                pass
            download = download_info.value

            # Save to output path
            final_path = output_path / filename
            download.save_as(str(final_path))
            print(f"  [OK] Video saved: {final_path}")
            return str(final_path)

        except Exception as e:
            print(f"  [ERROR] Download failed: {e}")
            return None
    else:
        print("  [ERROR] Could not find download button")
        return None


def generate_video(
    page,
    reference_image: str,
    prompt: str,
    output_dir: str,
    video_url: Optional[str] = None
) -> Optional[str]:
    """
    Generate a video from a reference image and prompt.

    This is the main entry point for video generation. It:
    1. Navigates to the video section
    2. Uploads the reference image
    3. Enters the video prompt
    4. Triggers generation
    5. Polls for completion
    6. Downloads the result

    Args:
        page: Playwright page object (already logged in)
        reference_image: Path to the hero image to use as reference
        prompt: Video generation prompt
        output_dir: Directory to save the video
        video_url: Optional override for video URL (for testing)

    Returns:
        Path to downloaded video, or None if generation failed
    """
    url = video_url or VIDEO_URL

    print(f"\n{'='*60}")
    print("VIDEO GENERATION")
    print(f"{'='*60}")
    print(f"  Reference: {Path(reference_image).name}")
    print(f"  Output: {output_dir}")
    print(f"  URL: {url}")

    # Step 1: Navigate to video section
    print("\nStep 1: Navigating to video section...")
    try:
        navigate_safely(page, url)
        time.sleep(3)  # Wait for page hydration
    except Exception as e:
        print(f"  [ERROR] Navigation failed: {e}")
        return None

    # TODO: Verify video section loaded correctly
    # May need to check for video-specific UI elements

    # Step 2: Upload reference image
    print("\nStep 2: Uploading reference image...")
    if not upload_reference_image(page, reference_image):
        print("  [ERROR] Reference image upload failed")
        return None
    time.sleep(2)

    # Step 3: Enter prompt
    print("\nStep 3: Entering video prompt...")
    enter_prompt(page, prompt)
    time.sleep(1)

    # Step 4: Click Generate
    # TODO: Verify generate button selector for video section
    print("\nStep 4: Clicking Generate...")
    from generate_images import click_generate

    # Videos may need only 1 click (different from images)
    click_generate(page, times=1, interval=1.0)

    # Step 5: Wait for generation and poll for completion
    print(f"\nStep 5: Waiting for video generation...")
    print(f"  Initial wait: {VIDEO_INITIAL_WAIT}s")
    time.sleep(VIDEO_INITIAL_WAIT)

    print(f"  Polling for completion (max {VIDEO_MAX_POLLS * VIDEO_POLL_INTERVAL}s)...")
    for poll_num in range(VIDEO_MAX_POLLS):
        if check_video_ready(page):
            break
        if poll_num < VIDEO_MAX_POLLS - 1:
            time.sleep(VIDEO_POLL_INTERVAL)
            if poll_num % 15 == 0:  # Print status every 30 seconds
                print(f"  Waiting... ({poll_num * VIDEO_POLL_INTERVAL}s elapsed)")
    else:
        print("  [ERROR] Video generation timed out after 2 minutes")
        return None

    # Step 6: Download video
    print("\nStep 6: Downloading video...")
    result = download_video(page, output_dir)

    print(f"\n{'='*60}")
    if result:
        print("VIDEO GENERATION COMPLETE")
        print(f"{'='*60}")
        print(f"  Output: {result}")
    else:
        print("VIDEO GENERATION FAILED")
        print(f"{'='*60}")

    return result


def main():
    """CLI entry point for video generation testing."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate videos via Higgsfield AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate video from reference image
  python generate_videos.py --reference hero.png --prompt "slow pan across..."

  # Specify output directory
  python generate_videos.py --reference hero.png --prompt "..." --output ./videos/

  # Use custom video URL (for testing)
  python generate_videos.py --reference hero.png --prompt "..." --url "https://..."
        """,
    )

    parser.add_argument(
        "--reference", "-r",
        required=True,
        help="Path to reference image (hero image)"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Video generation prompt"
    )
    parser.add_argument(
        "--output", "-o",
        default="./downloads/higgsfield/video/",
        help="Output directory for generated video"
    )
    parser.add_argument(
        "--url",
        default=None,
        help="Override video URL (for testing)"
    )
    parser.add_argument(
        "--login",
        action="store_true",
        help="Run login mode first (from generate_images.py)"
    )

    args = parser.parse_args()

    # Import from generate_images for browser creation
    from generate_images import login_mode
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        if args.login:
            login_mode(playwright)
            return

        # Check for existing session
        if not PROFILE_DIR.exists():
            print("[ERROR] No saved session. Run with --login first.")
            return 1

        context = create_browser(playwright, headless=False)
        page = context.pages[0] if context.pages else context.new_page()

        # Navigate and verify login
        navigate_safely(page, VIDEO_URL)
        time.sleep(3)

        if not wait_for_logged_in(page):
            print("[ERROR] Not logged in. Run with --login first.")
            context.close()
            return 1

        # Generate video
        result = generate_video(
            page=page,
            reference_image=args.reference,
            prompt=args.prompt,
            output_dir=args.output,
            video_url=args.url
        )

        print("\nBrowser will stay open for review. Close when done.")
        try:
            page.wait_for_event("close", timeout=0)
        except Exception:
            pass

        try:
            context.close()
        except Exception:
            pass

        return 0 if result else 1


if __name__ == "__main__":
    exit(main())