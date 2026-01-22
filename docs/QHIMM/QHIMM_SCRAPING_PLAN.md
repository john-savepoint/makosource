# QHIMM Forum Comprehensive Scraping & Knowledge Base Plan

**Created:** 2025-12-28 13:35:00 JST (Sunday)
**Session-ID:** 5e062ad5-f6c1-44e8-bbd7-332d37b1a441
**Status:** APPROVED - Ready for Implementation

---

## Executive Summary

Scrape and organize 20+ years of FF7 modding knowledge from QHIMM forums (251,925 posts across 15,332 topics) into a searchable, vector-indexed knowledge base with AI-powered retrieval.

---

## Forum Analysis Results

### Scope Assessment

| Metric | Value |
|--------|-------|
| Total Posts | 251,925 |
| Total Topics | 15,332 |
| Total Boards | 104 |
| Registered Members | 38,113 |
| Years of Content | 15+ (2009-2025) |
| Most Viewed Topic | 7+ million views (New Threat Mod) |

### Priority FF7 Boards to Scrape

| Board | # | Topics | Posts | Priority |
|-------|---|--------|-------|----------|
| FF7 Tools | 48 | 157 | 11,234 | **CRITICAL** |
| FF7 Graphics | 61 | 266 | 16,188 | **CRITICAL** |
| FF7 Gameplay | 68 | 93 | 17,390 | **CRITICAL** |
| 7th Heaven | 37 | 1,295 | 8,125 | **CRITICAL** |
| FFNx Driver | 54 | 1 | 138 | **CRITICAL** |
| FF7 General | 96 | 166 | 7,489 | HIGH |
| FF7 Troubleshooting | 97 | 191 | 662 | HIGH |
| FF7 Audio | 65 | 84 | 2,183 | MEDIUM |
| FF7 Other Mods | 69 | 55 | 4,269 | MEDIUM |
| FAQs/Tutorials | 9 | ~50 | ~500 | HIGH |

**Estimated Total FF7 Content:** ~67,000 posts across ~2,300 topics

---

## Technical Architecture

### Phase 1: Ingestion Layer

```
┌─────────────────────────────────────────────────────────────┐
│                    SCRAPING PIPELINE                        │
├─────────────────────────────────────────────────────────────┤
│  SMF Forum Crawler (Python + BeautifulSoup/Scrapy)          │
│  ├── Board Index Parser                                      │
│  ├── Topic List Paginator                                    │
│  ├── Post Content Extractor                                  │
│  └── Rate Limiter (1-2 sec delays)                          │
├─────────────────────────────────────────────────────────────┤
│  Content Processor                                           │
│  ├── HTML → Markdown Conversion                             │
│  ├── Code Block Detection                                    │
│  ├── Image/Attachment Cataloging                            │
│  └── Quote/Reply Threading                                   │
└─────────────────────────────────────────────────────────────┘
```

### Phase 2: Storage Layer

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA STORAGE                             │
├─────────────────────────────────────────────────────────────┤
│  PostgreSQL + pgvector                                       │
│  ├── posts (id, topic_id, author, date, content, embedding) │
│  ├── topics (id, board_id, title, tags, view_count)         │
│  ├── boards (id, name, category)                            │
│  ├── users (id, name, post_count, expertise_tags)           │
│  └── attachments (id, post_id, filename, type)              │
├─────────────────────────────────────────────────────────────┤
│  File Storage                                                │
│  ├── Raw HTML Archives                                       │
│  ├── Converted Markdown                                      │
│  ├── Combined Topic Documents                                │
│  └── Downloaded Attachments/Images                          │
└─────────────────────────────────────────────────────────────┘
```

### Phase 3: Knowledge Graph

```
┌─────────────────────────────────────────────────────────────┐
│                    NEO4J KNOWLEDGE GRAPH                    │
├─────────────────────────────────────────────────────────────┤
│  Entities:                                                   │
│  ├── Tool (WallMarket, Makou Reactor, etc.)                 │
│  ├── FileFormat (kernel.bin, scene.bin, LGP, etc.)          │
│  ├── GameModule (Field, Battle, Menu, WorldMap)             │
│  ├── Technique (hex editing, texture replacement, etc.)     │
│  ├── User (expertise contributor)                           │
│  └── Topic (discussion thread)                              │
├─────────────────────────────────────────────────────────────┤
│  Relationships:                                              │
│  ├── DISCUSSES (Topic → FileFormat)                         │
│  ├── MODIFIES (Tool → FileFormat)                           │
│  ├── REFERENCES (Post → Post)                               │
│  ├── AUTHORED_BY (Post → User)                              │
│  └── PART_OF (FileFormat → GameModule)                      │
└─────────────────────────────────────────────────────────────┘
```

### Phase 4: RAG/Query Layer

```
┌─────────────────────────────────────────────────────────────┐
│                    RETRIEVAL SYSTEM                         │
├─────────────────────────────────────────────────────────────┤
│  Vector Search (pgvector)                                    │
│  ├── Semantic similarity for natural language queries       │
│  ├── Hybrid search (keyword + semantic)                     │
│  └── Context window assembly                                 │
├─────────────────────────────────────────────────────────────┤
│  Graph Traversal (Neo4j)                                     │
│  ├── "What tools modify kernel.bin?"                        │
│  ├── "Who are the experts on field scripts?"                │
│  └── "What topics discuss X technique?"                     │
├─────────────────────────────────────────────────────────────┤
│  LLM Integration                                             │
│  ├── Question answering with citations                       │
│  ├── Summary generation                                      │
│  └── Tutorial synthesis                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Plan

### Stage 1: Foundation (Week 1-2)

**Objective:** Build scraping infrastructure and test with small subset

1. **SMF Forum Scraper**
   - Extend existing `scraper.py` for SMF forum structure
   - Handle pagination (topics paginate as `topic=XXXX.0`, `.50`, `.100`, etc.)
   - Extract: post content, author, date, quotes, code blocks
   - Handle session management (PHPSESSID)

2. **Database Schema**
   - PostgreSQL setup with pgvector extension
   - Create tables: boards, topics, posts, users, attachments
   - Add embedding column for vector search

3. **Initial Test Scrape**
   - Scrape one small board (FF7 Audio - 84 topics, 2,183 posts)
   - Validate content extraction quality
   - Test rate limiting and error handling

### Stage 2: Full Ingestion (Week 2-3)

**Objective:** Scrape all priority FF7 boards

1. **Board-by-Board Scraping**
   - Start with CRITICAL boards (Tools, Graphics, Gameplay, 7th Heaven, FFNx)
   - Progress to HIGH/MEDIUM priority boards
   - Estimated: ~67,000 posts to scrape

2. **Content Processing**
   - HTML → Markdown conversion
   - Code block syntax detection (hext, LUA, field script)
   - Quote/reply threading preservation
   - Image/attachment URL cataloging

3. **Topic Collation**
   - Combine multi-page topics into single documents
   - Add metadata headers (author, date, board, view count)
   - Generate per-topic markdown files

### Stage 3: Semantic Indexing (Week 3-4)

**Objective:** Enable AI-powered search

1. **Embedding Generation**
   - Generate embeddings for all posts (OpenAI ada-002 or local)
   - Chunk long posts appropriately (512-1024 tokens)
   - Store in pgvector

2. **Knowledge Graph Population**
   - Extract entities: tools, file formats, techniques
   - Use LLM to identify relationships
   - Build Neo4j graph

3. **RAG Pipeline**
   - Implement hybrid search (keyword + semantic)
   - Context assembly for LLM queries
   - Citation tracking to source posts

### Stage 4: Knowledge Products (Week 4-5)

**Objective:** Generate educational content

1. **Consolidated Documentation**
   - Merge related topics into comprehensive guides
   - Example: All WallMarket threads → "WallMarket Complete Guide"
   - Cross-reference with existing game engine docs

2. **Query Interface**
   - CLI tool for knowledge base queries
   - Integration with Claude Code sessions
   - MCP server for real-time lookups

3. **Quality Validation**
   - Compare against existing documentation
   - Identify gaps and contradictions
   - Flag outdated information

---

## Tech Stack Selection

### Recommended Stack

| Component | Tool | Rationale |
|-----------|------|-----------|
| **Scraping** | Scrapy + BeautifulSoup | Robust, handles pagination, rate limiting |
| **Database** | PostgreSQL + pgvector | Already familiar, vector search built-in |
| **Embeddings** | OpenAI ada-002 or sentence-transformers | High quality, cost effective |
| **Knowledge Graph** | Neo4j | Industry standard, good Cypher queries |
| **Entity Extraction** | LLM (Claude/GPT) | Context-aware extraction |
| **Query Interface** | FastAPI + Streamlit | Quick prototyping, good for exploration |
| **Observability** | Langfuse | Track LLM usage and quality |

### Alternative Lightweight Stack

If you want to minimize complexity:

| Component | Tool | Rationale |
|-----------|------|-----------|
| **Scraping** | Python requests + BeautifulSoup | Simple, effective |
| **Storage** | SQLite + markdown files | Local, no server needed |
| **Search** | Full-text search + grep | Fast iteration |
| **Embeddings** | sentence-transformers (local) | No API costs |

---

## Critical Files to Modify/Create

```
/home/johnzealanddoyle/projects/ff7OG_japanese/
├── docs/QHIMM/
│   ├── scraper/
│   │   ├── smf_scraper.py          # SMF forum scraper
│   │   ├── content_processor.py     # HTML→Markdown conversion
│   │   ├── topic_collator.py        # Multi-page topic merging
│   │   └── config.yaml              # Board definitions, rate limits
│   ├── raw/                          # Raw HTML archives
│   ├── markdown/                     # Converted per-post markdown
│   ├── topics/                       # Collated topic documents
│   ├── combined/                     # Category-level merged docs
│   └── database/
│       ├── schema.sql               # PostgreSQL schema
│       └── embeddings/              # Vector storage
```

---

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Rate limiting/blocking | 2-second delays, polite user-agent, respect robots.txt |
| Session expiration | Handle PHPSESSID, implement retry logic |
| Content changes | Store raw HTML for re-processing |
| Large scale (67k posts) | Incremental scraping, checkpoint resume |
| Copyright concerns | Educational use, attribution to authors |
| Stale information | Date-stamp all content, prioritize recent posts |

---

## User Preferences (Confirmed)

| Decision | Choice | Notes |
|----------|--------|-------|
| **Hosting** | Free-tier cloud + local hybrid | Supabase free tier (500MB), Neo4j Aura free tier, local fallback |
| **Embeddings** | OpenAI API (ada-002) | ~$2-5 total cost for 67k posts |
| **Starting Point** | Prototype first | FF7 Audio board (84 topics, 2,183 posts) |
| **Integration** | All interfaces | MCP server + CLI + Web UI |
| **Cost Priority** | Minimize costs | Use free tiers where possible |

---

## Revised Tech Stack (Cost-Optimized)

| Component | Tool | Cost |
|-----------|------|------|
| **Database** | Supabase (free tier) | $0/mo (500MB, includes pgvector) |
| **Knowledge Graph** | Neo4j Aura (free tier) | $0/mo (50k nodes, 175k relationships) |
| **Embeddings** | OpenAI ada-002 | ~$2-5 one-time |
| **Backend API** | Vercel/Render (free tier) | $0/mo |
| **Frontend** | Vercel (free tier) | $0/mo |
| **MCP Server** | Local Node.js | $0 |

**Total Estimated Cost:** $2-5 one-time for embeddings

---

## Implementation Roadmap (Approved)

### Phase 1: Prototype (This Session → Week 1)

1. **Create SMF Forum Scraper**
   - Extend existing `scraper.py` patterns
   - Handle SMF URL structure (`?board=XX.0`, `?topic=XXXXX.0`)
   - Pagination support (`.0`, `.50`, `.100` suffixes)
   - Rate limiting (2-second delays)
   - Session/cookie handling

2. **Test Scrape: FF7 Audio Board**
   - Board 65: 84 topics, 2,183 posts
   - Validate HTML → Markdown conversion
   - Test quote/code block extraction
   - Verify threading preservation

3. **Local Storage First**
   - SQLite for quick iteration
   - Markdown files per topic
   - Can migrate to Supabase later

### Phase 2: Full Ingestion (Week 1-2)

4. **Scrape All Priority FF7 Boards**
   - Tools (48), Graphics (61), Gameplay (68)
   - 7th Heaven (37), FFNx (54)
   - General (96), Troubleshooting (97)
   - Estimated: ~67k posts

5. **Topic Collation**
   - Multi-page topics → single documents
   - Metadata headers (author, date, views)
   - Cross-reference links

### Phase 3: Semantic Layer (Week 2-3)

6. **Supabase Setup**
   - Migrate SQLite → Supabase pgvector
   - Generate OpenAI embeddings
   - Hybrid search implementation

7. **Neo4j Knowledge Graph**
   - Entity extraction (tools, file formats, techniques)
   - Relationship mapping
   - Query interface

### Phase 4: Interfaces (Week 3-4)

8. **MCP Server**
   - Query QHIMM knowledge from Claude Code
   - Semantic search + citation

9. **CLI Tool**
   - `qhimm-search "kernel.bin structure"`
   - Results with source links

10. **Web Interface**
    - Streamlit for rapid prototyping
    - Browse by board/topic/search

---

## Estimated Effort

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| Foundation | 1-2 weeks | Working scraper, test data |
| Full Ingestion | 1-2 weeks | All FF7 content scraped |
| Semantic Index | 1 week | Vector search working |
| Knowledge Products | 1 week | Query interface, merged docs |

**Total:** 4-6 weeks for complete system

---

*This plan incorporates your existing scraper.py patterns and the tech stack recommendations from the architecture overview you provided.*
