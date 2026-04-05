#!/usr/bin/env python3
"""
Article Processor for Higgsfield AI Image Generation
======================================================
Created: 2026-04-06
Session: 04.1-01

Context:
    Parses article markdown files from Astro content collections and generates
    prompts for hero images, section illustrations, and video content using
    the STYLE-GUIDE.md templates.

Usage:
    from article_processor import parse_article, generate_prompts, extract_sections

    article = parse_article("/path/to/article.md")
    prompts = generate_prompts(article, "/path/to/STYLE-GUIDE.md")
"""

import re
from pathlib import Path
from typing import Optional

try:
    import frontmatter
except ImportError:
    print("ERROR: python-frontmatter not installed. Run: pip3 install python-frontmatter")
    raise


# Tone mapping based on article tags
TAG_MOOD_MAP = {
    "critical": "confrontational, evidence-based",
    "ironic": "dark humor, satirical",
    "satirical": "witty, pointed satire",
    "dark humor": "darkly comic, provocative",
    "serious": "serious, analytical",
    "analytical": "analytical, data-driven",
}

DEFAULT_MOOD = "confrontational, serious, evidence-based"


def parse_article(article_path: str) -> dict:
    """
    Extract frontmatter and content from a markdown article.

    Args:
        article_path: Path to the article markdown file

    Returns:
        dict with keys: title, slug, description, tags, content, sections
    """
    path = Path(article_path)
    if not path.exists():
        raise FileNotFoundError(f"Article not found: {article_path}")

    with open(path, "r", encoding="utf-8") as f:
        post = frontmatter.load(f)

    metadata = post.metadata

    return {
        "title": metadata.get("title", ""),
        "slug": metadata.get("slug", path.stem),
        "description": metadata.get("description", ""),
        "tags": metadata.get("tags", []),
        "content": post.content,
        "sections": extract_sections(post.content),
        "file_path": str(path),
    }


def extract_sections(content: str) -> list:
    """
    Extract section headings (h2) from article content.

    Args:
        content: Raw markdown content

    Returns:
        List of section heading strings
    """
    sections = []
    for match in re.finditer(r"^## (.+)$", content, re.MULTILINE):
        sections.append(match.group(1).strip())
    return sections


def extract_satirical_element(content: str) -> str:
    """
    Extract a key provocative phrase or data point from article content
    for the satirical element in prompts.

    Looks for:
    - Quoted statistics with sources
    - Provocative statements
    - Key comparisons

    Args:
        content: Raw markdown content

    Returns:
        String containing a satirical element for prompt enrichment
    """
    # Priority 1: Statistics with units (percentages, costs, numbers)
    stat_pattern = r'(\d+(?:\.\d+)?(?:\s*(?:percent|%|billion|million|trillion|GW|GWh|hectares?|years?|times?))(?:\s+(?:more|less|of|the|than))?)'
    stat_match = re.search(stat_pattern, content, re.IGNORECASE)
    if stat_match:
        # Get context around the stat
        start = max(0, stat_match.start() - 50)
        end = min(len(content), stat_match.end() + 50)
        context = content[start:end].strip()
        # Clean up the context
        context = re.sub(r'\s+', ' ', context)
        if len(context) > 100:
            context = context[:100] + "..."
        return f"Key statistic: {context}"

    # Priority 2: Comparisons (X vs Y, more than, less than)
    compare_pattern = r'(approximately|roughly|about|over|under|more than|less than)?\s*\d+(?:\.\d+)?\s*(?:times?|percent|%).*?(?:than|compared to)'
    compare_match = re.search(compare_pattern, content, re.IGNORECASE)
    if compare_match:
        return f"Key comparison: {compare_match.group(0).strip()}"

    # Priority 3: Provocative phrases
    provocative_keywords = [
        "masterclass", "irony", "ironically", "not supported by", "poisoned by",
        "fighting", "forced to", "can't replace", "doesn't work when",
        "net negative", "environmental cost", "atrocious"
    ]
    for keyword in provocative_keywords:
        if keyword.lower() in content.lower():
            # Find sentence containing the keyword
            sentence_pattern = rf'[^.!?]*{re.escape(keyword)}[^.!?]*[.!?]'
            match = re.search(sentence_pattern, content, re.IGNORECASE)
            if match:
                sentence = match.group(0).strip()
                if len(sentence) > 150:
                    sentence = sentence[:150] + "..."
                return f"Key phrase: \"{sentence}\""

    # Fallback: First sentence of first paragraph after title
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    for para in paragraphs:
        if para.startswith("#"):
            continue
        first_sentence = re.match(r'^([^.!?]+[.!?])', para)
        if first_sentence:
            sentence = first_sentence.group(1).strip()
            if len(sentence) > 100:
                sentence = sentence[:100] + "..."
            return f"Article context: {sentence}"

    return ""


def determine_mood(tags: list) -> str:
    """
    Determine the visual mood from article tags.

    Args:
        tags: List of tag strings from article frontmatter

    Returns:
        Mood string for prompt generation
    """
    for tag in tags:
        tag_lower = tag.lower()
        if tag_lower in TAG_MOOD_MAP:
            return TAG_MOOD_MAP[tag_lower]

    # Check for partial matches
    for tag in tags:
        tag_lower = tag.lower()
        for key, mood in TAG_MOOD_MAP.items():
            if key in tag_lower or tag_lower in key:
                return mood

    return DEFAULT_MOOD


def suggest_key_element(section_title: str) -> str:
    """
    Suggest a key visual element based on section title.

    This is a simple heuristic that maps common section topics
    to visual metaphors suitable for illustration.

    Args:
        section_title: The section heading text

    Returns:
        Suggested key visual element description
    """
    title_lower = section_title.lower()

    # Energy/power related
    if any(word in title_lower for word in ["nuclear", "power", "energy", "electricity", "grid"]):
        return "power infrastructure, energy flow visualization"

    # Environmental
    if any(word in title_lower for word in ["environment", "climate", "carbon", "emission", "waste"]):
        return "environmental impact visualization, carbon flow"

    # Economic/financial
    if any(word in title_lower for word in ["cost", "price", "economic", "money", "invest", "billion"]):
        return "financial data visualization, cost comparison charts"

    # Policy/political
    if any(word in title_lower for word in ["policy", "government", "political", "ban", "regulation"]):
        return "policy document imagery, governmental symbols"

    # Technology
    if any(word in title_lower for word in ["technology", "solar", "wind", "battery", "storage"]):
        return "technical diagrams, infrastructure cross-sections"

    # Comparison/analysis
    if any(word in title_lower for word in ["comparison", "versus", "analysis", "problem", "issue"]):
        return "comparative visualization, side-by-side data"

    # Future/path forward
    if any(word in title_lower for word in ["future", "path", "forward", "solution", "alternative"]):
        return "forward-looking visualization, pathway imagery"

    # Default
    return "editorial illustration element relevant to topic"


# Prompt templates matching STYLE-GUIDE.md

HERO_TEMPLATE = """A dramatic editorial illustration for a political commentary article about {topic}.
Dark background (#0a0a0a), high contrast lighting, bold composition.
Style: investigative journalism magazine cover art, data-driven visual metaphor.
Mood: {mood}.
Color palette: predominantly dark with punchy red (#ff3b3b) and blue (#4da6ff) accents.
No text, no watermarks, no borders.
Aspect ratio: 16:9, 1600x900px.

Article context: {context}
{satirical_element}"""

SECTION_TEMPLATE = """An editorial spot illustration for a section about "{section_title}" in an article about "{article_topic}".
Dark background, high contrast, editorial magazine style.
Focused composition highlighting {key_element}.
Color palette: dark with selective use of red (#ff3b3b) or blue (#4da6ff) accent.
No text, no watermarks.
Aspect ratio: 3:2, 1200x800px."""

VIDEO_TEMPLATE = """A dramatic editorial animation for a political commentary article about {topic}.
Dark background (#0a0a0a), high contrast lighting, subtle motion.
Style: investigative journalism magazine cover art coming to life.
Motion: slow pan, zoom, or data visualization animation.
Duration: 3-5 seconds.
No text, no watermarks, no borders.
Aspect ratio: 16:9.

Article context: {context}
{satirical_element}"""


def generate_prompts(article: dict, style_guide_path: str = None) -> dict:
    """
    Generate prompts for hero image, section illustrations, and video.

    Args:
        article: Dict from parse_article()
        style_guide_path: Optional path to STYLE-GUIDE.md (for future template loading)

    Returns:
        dict with keys:
            - hero: string prompt for hero image
            - sections: list of prompts, one per section heading
            - video: string prompt for video generation
    """
    topic = article.get("title", "")
    context = article.get("description", "")
    content = article.get("content", "")
    sections = article.get("sections", [])
    tags = article.get("tags", [])

    # Determine mood from tags
    mood = determine_mood(tags)

    # Extract satirical element from content
    satirical_element = extract_satirical_element(content)

    # Generate hero prompt
    hero_prompt = HERO_TEMPLATE.format(
        topic=topic,
        mood=mood,
        context=context,
        satirical_element=satirical_element
    )

    # Generate section prompts
    section_prompts = []
    for section_title in sections:
        key_element = suggest_key_element(section_title)
        section_prompt = SECTION_TEMPLATE.format(
            section_title=section_title,
            article_topic=topic,
            key_element=key_element
        )
        section_prompts.append({
            "title": section_title,
            "prompt": section_prompt
        })

    # Generate video prompt
    video_prompt = VIDEO_TEMPLATE.format(
        topic=topic,
        mood=mood,
        context=context,
        satirical_element=satirical_element
    )

    return {
        "hero": hero_prompt.strip(),
        "sections": section_prompts,
        "video": video_prompt.strip(),
        "metadata": {
            "article_slug": article.get("slug", ""),
            "article_title": topic,
            "mood": mood,
            "section_count": len(sections),
        }
    }


def generate_prompts_from_file(article_path: str, style_guide_path: str = None) -> dict:
    """
    Convenience function to parse article and generate prompts in one step.

    Args:
        article_path: Path to article markdown file
        style_guide_path: Optional path to STYLE-GUIDE.md

    Returns:
        dict from generate_prompts()
    """
    article = parse_article(article_path)
    return generate_prompts(article, style_guide_path)


def main():
    """CLI entry point for testing."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Process article and generate prompts for Higgsfield AI"
    )
    parser.add_argument("article", help="Path to article markdown file")
    parser.add_argument("--style-guide", help="Path to STYLE-GUIDE.md", default=None)
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    try:
        result = generate_prompts_from_file(args.article, args.style_guide)

        if args.json:
            import json
            print(json.dumps(result, indent=2))
        else:
            print("=" * 60)
            print(f"ARTICLE: {result['metadata']['article_title']}")
            print(f"SLUG: {result['metadata']['article_slug']}")
            print(f"MOOD: {result['metadata']['mood']}")
            print(f"SECTIONS: {result['metadata']['section_count']}")
            print("=" * 60)
            print("\n--- HERO PROMPT ---")
            print(result["hero"])
            print("\n--- SECTION PROMPTS ---")
            for i, section in enumerate(result["sections"], 1):
                print(f"\n[{i}] {section['title']}:")
                print(section["prompt"])
            print("\n--- VIDEO PROMPT ---")
            print(result["video"])

    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        return 1
    except Exception as e:
        print(f"ERROR: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())