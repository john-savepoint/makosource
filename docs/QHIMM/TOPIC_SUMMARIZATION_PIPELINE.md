# QHIMM Topic Summarization Pipeline

**Created:** 2025-12-30 22:58 JST
**Session-ID:** 5e062ad5-f6c1-44e8-bbd7-332d37b1a441

---

## Overview

Transform 2,500+ forum topics (~5 million words) into a curated knowledge base of topic summaries (~500-1000 words each).

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    RAW FORUM DATA                           │
│  2,545 topics │ 61,000+ posts │ ~5M words                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 TOPIC CLASSIFIER                            │
│  Categorize by type: Tool, Tutorial, Discussion, Support    │
│  Estimate complexity: Simple (<20 posts) vs Complex (>100)  │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  TOOL TOPICS    │ │ TUTORIAL/FAQ    │ │ SUPPORT/DISCUSS │
│  Summarizer     │ │ Summarizer      │ │ Summarizer      │
└─────────────────┘ └─────────────────┘ └─────────────────┘
              │               │               │
              └───────────────┼───────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 STRUCTURED SUMMARIES                        │
│  - Key information extracted                                │
│  - Expert contributors identified                           │
│  - Important links/releases cataloged                       │
│  - Outdated info flagged                                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 DUAL STORAGE                                │
│  SQLite: topic_summaries table                              │
│  Markdown: /topics/{board}/{topic_id}_summary.md            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 VECTOR EMBEDDINGS                           │
│  Embed both: raw posts + summaries                          │
│  Tag embeddings with source type for filtering              │
└─────────────────────────────────────────────────────────────┘
```

---

## Summary Schema

### Database Table: `topic_summaries`

```sql
CREATE TABLE topic_summaries (
    topic_id TEXT PRIMARY KEY,
    board_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    category TEXT,              -- 'tool', 'tutorial', 'discussion', 'support', 'release'

    -- Core summary
    summary_text TEXT,          -- 500-1500 word summary
    key_points TEXT,            -- JSON array of bullet points

    -- Metadata extracted
    tool_name TEXT,             -- If about a specific tool
    tool_version TEXT,          -- Latest version mentioned
    download_urls TEXT,         -- JSON array of download links

    -- Contributors
    experts TEXT,               -- JSON array of {name, post_count, expertise}
    original_author TEXT,       -- Thread starter

    -- Temporal
    first_post_date TEXT,
    last_post_date TEXT,
    is_outdated INTEGER,        -- Flagged if superseded or abandoned
    superseded_by TEXT,         -- topic_id of newer version

    -- Stats
    post_count INTEGER,
    unique_contributors INTEGER,
    useful_post_count INTEGER,  -- Posts with actual content vs "thanks"

    -- Processing metadata
    summarized_at TEXT,
    model_used TEXT,
    tokens_used INTEGER
);
```

### Markdown Output Format

```markdown
# [Tool Name] - [Version]

**Topic:** [Original Title]
**Board:** [Board Name]
**Author:** [Original Author]
**Active:** [First Post Date] - [Last Post Date]
**Posts:** [X] ([Y] substantive)

## Summary

[2-3 paragraph summary of what this topic covers]

## Key Points

- Point 1
- Point 2
- Point 3

## Downloads & Links

- [Version X.X](url) - Latest stable
- [GitHub](url)
- [Documentation](url)

## Known Issues & Solutions

| Issue | Solution | Post # |
|-------|----------|--------|
| ... | ... | #123 |

## Expert Contributors

- **Username1** (X posts) - Primary maintainer
- **Username2** (Y posts) - Major contributor

## Related Topics

- [Related Topic 1](link)
- [Related Topic 2](link)

## Status

[Active/Abandoned/Superseded by X]

---
*Summary generated: YYYY-MM-DD*
*Source: [Original Thread](url)*
```

---

## Summarization Prompts by Category

### Tool Release Topics

```
You are summarizing a forum thread about an FF7 modding tool.

Extract:
1. Tool name and current version
2. What the tool does (1-2 sentences)
3. Key features (bullet points)
4. System requirements/compatibility
5. Download links (latest stable)
6. Common issues and solutions
7. Who maintains it
8. Current status (active/abandoned/superseded)

Focus on FACTS, not opinions. Identify which posts contain actual information vs noise.
```

### Tutorial/FAQ Topics

```
You are summarizing a tutorial or FAQ thread about FF7 modding.

Extract:
1. What skill/task this teaches
2. Prerequisites (tools needed, knowledge required)
3. Step-by-step summary of the process
4. Common mistakes and how to avoid them
5. Links to required files/tools
6. Who wrote the authoritative posts

Consolidate information from multiple posts into a coherent guide.
```

### Support/Troubleshooting Topics

```
You are summarizing a troubleshooting thread about FF7 modding.

Extract:
1. The problem described
2. Root cause (if identified)
3. Working solution(s)
4. What DIDN'T work
5. System/version specifics where relevant

Skip posts that are just "me too" or "thanks". Focus on diagnostic and solution posts.
```

---

## Processing Strategy

### Phase 1: Classification (No LLM needed)

```python
def classify_topic(topic):
    title_lower = topic['title'].lower()

    # Tool releases
    if any(x in title_lower for x in ['[rel]', '[release]', 'editor', 'viewer', 'converter', 'tool']):
        return 'tool'

    # Tutorials
    if any(x in title_lower for x in ['tutorial', 'guide', 'how to', 'faq']):
        return 'tutorial'

    # Support
    if any(x in title_lower for x in ['help', 'error', 'crash', 'problem', 'issue', "doesn't work"]):
        return 'support'

    # Default to discussion
    return 'discussion'

def estimate_complexity(post_count):
    if post_count < 20:
        return 'simple'      # Single LLM call
    elif post_count < 100:
        return 'medium'      # Chunked summarization
    else:
        return 'complex'     # Map-reduce summarization
```

### Phase 2: Content Preparation

```python
def prepare_for_summary(topic_id, posts):
    """Filter noise, identify key posts."""

    noise_patterns = [
        r'^thanks',
        r'^bump',
        r'^me too',
        r'^\+1',
        r'^great work',
        r'^awesome',
    ]

    useful_posts = []
    for post in posts:
        text = post['content_text'].strip().lower()

        # Skip very short posts
        if len(text) < 50:
            continue

        # Skip pure noise
        if any(re.match(p, text) for p in noise_patterns):
            continue

        useful_posts.append(post)

    return useful_posts
```

### Phase 3: Summarization

**Simple topics (<20 posts):** Single LLM call with all posts

**Medium topics (20-100 posts):**
1. Filter to useful posts
2. Single LLM call if <30 useful posts
3. Otherwise chunk into 20-post segments, summarize each, then combine

**Complex topics (>100 posts):**
1. Filter to useful posts
2. Map: Summarize each chunk of 20 posts
3. Reduce: Combine chunk summaries into final summary

---

## Cost Estimation

| Model | Input Cost | Output Cost | Est. Total |
|-------|------------|-------------|------------|
| GPT-4o-mini | $0.15/1M | $0.60/1M | ~$15-25 |
| Claude Haiku | $0.25/1M | $1.25/1M | ~$25-40 |
| GPT-4o | $2.50/1M | $10/1M | ~$150-250 |

**Recommendation:** GPT-4o-mini or Claude Haiku for bulk summarization. Use GPT-4o/Claude Sonnet for complex topics only.

Estimated tokens:
- Input: ~10M tokens (5M words × 1.3 tokens/word, with filtering)
- Output: ~2M tokens (2,500 summaries × 800 tokens each)

---

## Implementation Files

```
/docs/QHIMM/
├── summarizer/
│   ├── classify.py          # Topic classification
│   ├── prepare.py           # Content filtering
│   ├── summarize.py         # LLM summarization
│   ├── prompts/
│   │   ├── tool.txt
│   │   ├── tutorial.txt
│   │   └── support.txt
│   └── config.yaml          # API keys, model selection
├── summaries/               # Generated markdown summaries
│   ├── board_37/
│   ├── board_48/
│   └── ...
└── database/
    └── qhimm.db            # Now includes topic_summaries table
```

---

## Parallel Processing

Run multiple summarization agents concurrently:

```python
async def summarize_all_topics(max_concurrent=10):
    topics = get_unsummarized_topics()

    semaphore = asyncio.Semaphore(max_concurrent)

    async def process_one(topic):
        async with semaphore:
            return await summarize_topic(topic)

    results = await asyncio.gather(*[process_one(t) for t in topics])
    return results
```

With 10 concurrent agents and ~5 seconds per topic, 2,500 topics = ~20 minutes.

---

## Next Steps

1. [ ] Finish scraping (39 topics remaining)
2. [ ] Add `topic_summaries` table to database
3. [ ] Implement classifier
4. [ ] Implement content filter
5. [ ] Create summarization prompts
6. [ ] Test on 10-20 topics across categories
7. [ ] Run bulk summarization
8. [ ] Generate embeddings for summaries
9. [ ] Build search interface

---

## Quality Control

After summarization, verify:

1. **Coverage:** Every topic has a summary
2. **Accuracy:** Spot-check 50 random summaries against source
3. **Completeness:** Tool topics have download links, tutorials have steps
4. **Freshness:** Outdated topics are flagged

---

*This pipeline will transform 5M words of forum noise into ~2.5M words of curated, searchable knowledge.*
