# FF7 Documentation System Architecture - Comprehensive Session Summary

**Date**: 2026-01-16 12:15 JST (Friday)
**Session ID**: 1c5b37d9-4924-4634-a8c4-2efbfcf46480
**Previous Session**: Continued from 2026-01-13 (FF7 String Decoder + IDA MCP setup)
**Duration**: ~4 hours
**Author**: Claude Sonnet 4.5

---

## Executive Summary

This session focused on designing a comprehensive documentation system for Final Fantasy VII reverse engineering. The system combines **two separate knowledge domains**: technical code analysis from IDA Pro and FFNx source code, plus community knowledge from forums, wikis, and external content. The architecture uses a hybrid database approach (Neo4j for code relationships + Supabase for documentation/search) with local Qwen embeddings for semantic search, generating a public MkDocs documentation website.

**Key Deliverable**: Complete architecture diagram and 50+ page technical specification document created at `/home/johnzealanddoyle/projects/tools/ff7-function-docs/FF7_DOCUMENTATION_SYSTEM_ARCHITECTURE.md`

---

## Session Context

### Starting Point
- **Previous session** (2026-01-13): Successfully set up IDA Pro MCP integration, created FF7 string decoder with correct byte+0x20 encoding, added 767 menu string comments to English ff7_en.exe database
- **User's goal**: Build a scalable documentation system for FF7 reverse engineering that combines technical analysis with community knowledge
- **Key question**: How to make this documentation accessible to both humans and AI agents via semantic search

---

## Part 1: Vector Database Fundamentals (Understanding Embeddings)

### User Question: "What is an embedding and how do we get things into it?"

**Explanation Provided**:

An **embedding** is a list of numbers (vector) that represents the *meaning* of text mathematically. Similar concepts have similar numbers.

**Example**:
```python
# Embedding for "add health points"
[0.023, -0.891, 0.445, 0.234, ..., 0.712]  # 1536 numbers

# Embedding for "increase HP"
[0.019, -0.887, 0.441, 0.229, ..., 0.708]  # Very similar!

# Embedding for "render graphics"
[-0.523, 0.234, -0.112, 0.891, ..., -0.334]  # Completely different
```

**How Embeddings Enable Semantic Search**:
1. Convert all documentation to embeddings (one-time process)
2. Store embeddings in database (PostgreSQL with pgvector extension)
3. When user searches "increase player HP", convert query to embedding
4. Find documents with similar embeddings (vector similarity search)
5. Return ranked results by similarity score

**Cost Comparison**:
- **OpenAI**: text-embedding-3-small at $0.00002 per 1k tokens (~$0.01 for 5,000 functions)
- **Local (Qwen)**: Zero API costs, runs on user's RTX 3070 GPU

### User's Decision: Qwen Embeddings (Local)

User revealed existing setup:
- `/home/johnzealanddoyle/projects/tools/qwen-semantic-search/`
- **Model**: Qwen3-Embedding-0.6B (1024-dimensional vectors)
- **Reranker**: BGE-Reranker-v2-m3 for two-stage search
- **Performance**: ~477ms search time with reranker, ~281ms without
- **Hardware**: RTX 3070 Laptop GPU (8GB VRAM)

**Advantages of User's Local Setup**:
- ✅ No API costs
- ✅ No data sent externally
- ✅ Already configured and tested
- ✅ Two-stage search (embedding + reranker) for high accuracy

---

## Part 2: Database Architecture Design

### Initial Question: Supabase vs Neon?

**User's Research**: Shared comparison article about Supabase vs Neon

**Recommendation: Supabase**

| Feature | Supabase | Neon | Winner |
|---------|----------|------|--------|
| **pgvector support** | ✅ Built-in | ✅ Supported | Tie |
| **Local development** | ✅ Full Docker stack | ❌ Cloud-only | **Supabase** |
| **Authentication** | ✅ Built-in GoTrue | ❌ Bring your own | **Supabase** |
| **Real-time updates** | ✅ WebSockets | ❌ Build yourself | **Supabase** |
| **Storage** | ✅ S3-compatible | ❌ Database only | **Supabase** |
| **Auto-generated API** | ✅ PostgREST | ❌ Build your own | **Supabase** |
| **Branching** | ❌ No | ✅ Yes (git-like) | Neon |
| **Scale-to-zero** | ❌ Always on | ✅ Yes | Neon |
| **Cost** | $25/mo Pro | $5/mo min usage | Neon (cheaper) |

**Why Supabase Won**:
1. **Wiki features needed**: User wants community contributions, requires auth
2. **Local development**: `supabase start` runs entire stack in Docker
3. **Real-time collaboration**: Multiple agents can see changes live
4. **Dashboard for moderation**: Non-technical users can review contributions
5. **Storage for assets**: Screenshots, diagrams alongside docs
6. **User's needs favor features over cost**: Always-on documentation server

**Local Development Workflow**:
```bash
# One-time setup
supabase init
supabase start  # Runs PostgreSQL + pgvector + Auth + API in Docker

# Database: postgresql://postgres:postgres@localhost:54322/postgres
# API: http://localhost:54321
# Dashboard: http://localhost:54323

# Work locally, then deploy to cloud when ready
supabase link --project-ref your-project
supabase db push
```

---

## Part 3: Why Graph Databases for Code Analysis?

### User's Insight: "Would Neo4j be better for representing code?"

**Answer: Absolutely YES**

**Problem with Relational Databases (PostgreSQL)**:

Finding "all functions that call addHealthPoints AND read currentHP":
```sql
-- Requires 4 joins, explodes in complexity
SELECT f1.name
FROM functions f1
JOIN function_calls fc ON f1.id = fc.caller_id
JOIN functions f2 ON fc.callee_id = f2.id
JOIN variable_reads vr ON f1.id = vr.function_id
JOIN variables v ON vr.variable_id = v.id
WHERE f2.name = 'addHealthPoints'
  AND v.name = 'currentHP';
```

**Solution with Graph Database (Neo4j)**:

Same query is trivial:
```cypher
MATCH (f:Function)-[:CALLS]->(target:Function {name: 'addHealthPoints'})
MATCH (f)-[:READS]->(v:Variable {name: 'currentHP'})
RETURN f.name
```

**Graph Advantages for Code**:
- **O(1) traversals**: Following relationships is instant (no joins)
- **Natural representation**: Code IS a graph (functions call functions, read variables)
- **Deep analysis**: "What breaks if I change this?" queries are simple
- **Pattern matching**: Find polymorphism, unused code, architectural issues

### Hybrid Architecture Decision

**Use BOTH databases for different purposes**:

```text
Neo4j Graph Database
├─ Function relationships (CALLS edges)
├─ Variable access patterns (READS/WRITES edges)
├─ Control flow graphs
├─ Class inheritance (INHERITS edges)
└─ Purpose: "What calls this?", "Impact analysis", "Data flow"

Supabase (PostgreSQL + pgvector)
├─ Full markdown documentation
├─ Semantic search (Qwen embeddings)
├─ Version history (entity_versions table)
├─ User contributions/approvals
└─ Purpose: Documentation storage, search, collaboration

Bidirectional Sync
└─ Metadata (names, addresses) synced between both
```

**Why Not Just One Database?**:
- Neo4j has no vector search (can't do semantic search)
- PostgreSQL relationship queries become complex beyond 3-4 levels deep
- Each database optimized for its purpose

**Graph Schema Example**:

```cypher
// Nodes
(:Function {ida_address, current_name, size, confidence})
(:Variable {ida_address, current_name, data_type, scope})
(:Struct {name, size, fields})

// Relationships
(Function)-[:CALLS {call_address}]->(Function)
(Function)-[:READS {read_address}]->(Variable)
(Function)-[:WRITES {write_address}]->(Variable)
(Struct)-[:HAS_FIELD {offset}]->(Variable)
```

**Powerful Graph Queries**:

1. **Find unused functions**:
```cypher
MATCH (f:Function)
WHERE NOT (f)<-[:CALLS]-()
RETURN f.current_name, f.ida_address
```

2. **Trace data flow**:
```cypher
MATCH path = (v:Variable {current_name: 'currentHP'})<-[:READS|WRITES*1..5]-(f:Function)
RETURN path
```

3. **Impact analysis**:
```cypher
MATCH path = (start:Function {name: 'addHealthPoints'})<-[:CALLS*1..10]-(caller:Function)
RETURN caller.current_name, length(path) as depth
```

4. **Discover potential classes** (functions operating on same variables):
```cypher
MATCH (f:Function)-[:READS|WRITES]->(v:Variable)
WITH v, collect(f) as functions
WHERE size(functions) > 3
RETURN v.current_name, [f IN functions | f.current_name]
```

---

## Part 4: Documentation Website Integration (MkDocs)

### User Question: "How would MkDocs change our architecture?"

**Recommendation: Database → MkDocs (Auto-Generated)**

```text
┌──────────────────────────────────────┐
│  Supabase Database (Source of Truth) │
│  - entities table with markdown_content
│  - entity_embeddings for search      │
└────────────┬─────────────────────────┘
             ↓
┌────────────────────────────────────────┐
│  generate_mkdocs.py (hourly via GitHub Actions)
│  - Queries database for all entities  │
│  - Generates .md files in docs/       │
│  - Builds mkdocs.yml navigation       │
└────────────┬───────────────────────────┘
             ↓
┌────────────────────────────────────────┐
│  MkDocs Static Site (GitHub Pages)    │
│  - Function documentation pages       │
│  - Relationship graphs from Neo4j     │
│  - Community discussion links         │
│  - Semantic search widget             │
└────────────────────────────────────────┘
```

**Why Database as Source of Truth**:
- ✅ Single source - no sync issues
- ✅ Updates to DB instantly reflected on website (hourly rebuild)
- ✅ Version history built-in (entity_versions table)
- ✅ Search and display use same data
- ✅ Can export to markdown files for git backup

**MkDocs Generation Script** (conceptual):

```python
def generate_mkdocs_site():
    # 1. Query all entities from Supabase
    result = supabase.table('entities').select('*').execute()

    # 2. Generate markdown files
    for entity in result.data:
        filename = f"docs/functions/{entity['ida_address']:08X}_{entity['current_name']}.md"

        # Add frontmatter
        content = f"""---
title: {entity['current_name']}
ida_address: 0x{entity['ida_address']:X}
last_updated: {entity['updated_at']}
---

{entity['markdown_content']}

## Relationships

### Calls
{get_neo4j_calls(entity['ida_address'])}

### Called By
{get_neo4j_callers(entity['ida_address'])}
"""

        write_file(filename, content)

    # 3. Generate mkdocs.yml
    generate_navigation(result.data)

    # 4. Build site
    subprocess.run(['mkdocs', 'build'])
```

**GitHub Actions Auto-Deploy**:

```yaml
name: Deploy Documentation
on:
  schedule:
    - cron: '0 * * * *'  # Rebuild every hour
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Generate docs from database
        env:
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_KEY: ${{ secrets.SUPABASE_KEY }}
        run: python generate_mkdocs_site.py --build

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
```

---

## Part 5: Dual Vector Database Concept

### User's Vision: Two Separate Knowledge Domains

**Critical Distinction**: Code analysis knowledge vs Community knowledge

**Vector Database 1: Code Documentation**

**Content**:
- Function documentation from IDA Pro analysis
- FFNx source code references
- Technical implementation details
- Disassembly explanations

**Example Entries**:
- "addHealthPoints - Adds health points to player character. Validates max HP limit and updates UI health bar."
- "patch_scene_block_divisor - Patches FF7's hardcoded scene.bin block divisor for multi-language support (German/French/Spanish use 11 scenes per block instead of 12)"

**Vector Database 2: Community Knowledge**

**Content**:
- Qhimm.com forum posts
- FF7 modding community discussions
- Reddit threads about FF7 mechanics
- Blog posts analyzing FF7 systems
- YouTube reverse engineering videos
- Wiki articles

**Example Entries**:
- "Qhimm forum: How HP damage formula works - explains ATK vs DEF calculation"
- "Blog post: Understanding FF7's battle system - detailed mechanics breakdown"
- "Reddit discussion: Why German version has different scene.bin structure"

**Why Two Separate Databases?**

1. **Different update frequencies**:
   - Code: Updated when agents analyze new functions
   - Community: Scraped periodically from external sources

2. **Different search contexts**:
   - Code search: "Find function that does X"
   - Community search: "Why does X work this way?"

3. **Different confidence levels**:
   - Code: High confidence (from disassembly)
   - Community: Varies (forum speculation vs confirmed knowledge)

4. **Combined power**:
   - Agent analyzes IDA function → searches BOTH databases
   - Technical analysis + community context = comprehensive documentation

**Combined Workflow Example**:

```python
def document_unknown_function(ida_address):
    # 1. Analyze in IDA
    disasm = mcp__ida_pro__get_disassembly(ida_address)

    # 2. Search CODE database
    code_matches = search_code_db("function that loads textures")
    # Returns: Similar functions already documented

    # 3. Search COMMUNITY database
    community_matches = search_community_db("FF7 texture loading LZSS")
    # Returns: Forum post explaining LZSS decompression format

    # 4. Generate documentation combining both
    markdown = f"""
# textureLoader (0x{ida_address:X})

## Technical Analysis
{analyze_disassembly(disasm)}

## Community Context
Related discussion: {community_matches[0]['url']}
"{community_matches[0]['excerpt']}"

## See Also
Similar functions: {[m['name'] for m in code_matches]}
"""

    store_in_database(markdown)
```

**Supabase Schema for Dual Databases**:

```sql
-- Code documentation
CREATE TABLE entities (
    id BIGSERIAL PRIMARY KEY,
    ida_address BIGINT,
    current_name VARCHAR(255),
    description TEXT,
    markdown_content TEXT
);

CREATE TABLE entity_embeddings (
    id BIGSERIAL PRIMARY KEY,
    entity_id INTEGER REFERENCES entities(id),
    embedding vector(1024)  -- Qwen embeddings
);

-- Community knowledge
CREATE TABLE community_posts (
    id BIGSERIAL PRIMARY KEY,
    source_type VARCHAR(50),  -- 'forum', 'blog', 'reddit', 'youtube'
    source_url TEXT,
    title TEXT,
    content TEXT,
    author VARCHAR(255),
    posted_at TIMESTAMP,
    scraped_at TIMESTAMP
);

CREATE TABLE community_embeddings (
    id BIGSERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES community_posts(id),
    embedding vector(1024)  -- Qwen embeddings
);

CREATE TABLE community_topics (
    id BIGSERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES community_posts(id),
    topic VARCHAR(255),
    relevance_score FLOAT
);
```

---

## Part 6: IDA Pro Multi-User Synchronization

### User Question: "How can multiple users sync IDA Pro databases?"

**Challenge**: IDA Pro `.idb` files are single-user, but we need collaborative analysis.

**Solution: Export/Import Scripts + Central Database**

**Approach 1: Manual Export/Import (Simplest)**

```python
# export_to_ida.py - Run in IDA Pro
# Downloads all names/comments from Supabase and applies to local IDA

import idc
from supabase import create_client

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Get all entities
result = supabase.table('entities').select('*').execute()

for entity in result.data:
    addr = entity['ida_address']
    name = entity['current_name']
    desc = entity['description']

    # Apply to IDA database
    idc.set_name(addr, name)
    if entity['entity_type'] == 'function':
        idc.set_func_cmt(addr, desc, 0)

print(f"✓ Imported {len(result.data)} entities")
```

```python
# import_from_ida.py - Run in IDA Pro
# Uploads your IDA names/comments to Supabase

import idc
import idautils
from supabase import create_client

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

for func_ea in idautils.Functions():
    name = idc.get_func_name(func_ea)

    # Skip auto-generated names
    if name.startswith('sub_'):
        continue

    comment = idc.get_func_cmt(func_ea, 0) or ''

    # Upload to database
    supabase.table('entities').insert({
        'ida_address': func_ea,
        'entity_type': 'function',
        'current_name': name,
        'original_name': f'sub_{func_ea:X}',
        'description': comment
    }).execute()

    print(f"✓ Uploaded {name}")
```

**User Workflow**:

1. **New user setup**:
   - Load ff7_en.exe in IDA Pro
   - Run `export_to_ida.py`
   - All community-documented names/comments applied instantly

2. **Contributing changes**:
   - User renames functions in IDA
   - Run `import_from_ida.py`
   - Changes uploaded to central database
   - Other users run `export_to_ida.py` to get updates

**Conflict Resolution Strategies**:

**Strategy 1: Last Write Wins**
```python
# Most recent change is kept
supabase.table('entities').update({
    'current_name': new_name,
    'updated_at': 'NOW()'
}).eq('id', entity_id).execute()
```

**Strategy 2: Contribution Approval**
```python
# Changes require moderator approval
supabase.table('contributions').insert({
    'entity_id': entity_id,
    'contributor_name': username,
    'old_value': old_name,
    'new_value': new_name,
    'status': 'pending'
}).execute()
```

**Strategy 3: Confidence-Based**
```python
# Higher confidence wins
if new_confidence > current_confidence:
    update_entity(new_name)
else:
    add_alternative_name(new_name)
```

**Approach 2: IDA Python Plugin (Advanced)**

```python
# ida_supabase_sync.py - IDA plugin with hotkeys

class SupabaseSync(idaapi.plugin_t):
    def init(self):
        # Register hotkeys
        idaapi.add_hotkey("Ctrl-Shift-U", self.upload_changes)
        idaapi.add_hotkey("Ctrl-Shift-D", self.download_changes)
        return idaapi.PLUGIN_KEEP

    def upload_changes(self):
        # Upload local IDA changes to Supabase
        # (same logic as import_from_ida.py)
        pass

    def download_changes(self):
        # Download Supabase changes to local IDA
        # (same logic as export_to_ida.py)
        pass
```

**Shared IDA Database File (Alternative)**:

- Host master `.i64` file on Google Drive/GitHub LFS
- Users download before analysis, upload after
- Requires manual merge if conflicts
- Simpler but less scalable

---

## Part 7: Complete System Architecture

### The 5-Layer Architecture

**Created**: `/home/johnzealanddoyle/projects/tools/ff7-function-docs/FF7_DOCUMENTATION_SYSTEM_ARCHITECTURE.md`

**Mermaid Diagram with Color-Coding**:

```mermaid
flowchart LR
    %% Color scheme:
    %% Blue (#2196f3) - Code analysis
    %% Purple (#9c27b0) - Community knowledge
    %% Pink (#e91e63) - Databases
    %% Green (#4caf50) - Agents
    %% Orange (#ff9800) - Output
    %% Teal (#009688) - Embeddings

    subgraph Layer1["LAYER 1: Analysis Sources"]
        IDA[IDA Pro]
        FFNx[FFNx Source Code]
    end

    subgraph Layer2["LAYER 2: Knowledge Ingestion"]
        Forums[Forums & Wikis]
        External[External Content]
    end

    subgraph Layer3["LAYER 3: Data Storage"]
        Neo4j[Neo4j Graph DB]
        SupabaseCode[Supabase - Code Docs]
        SupabaseCommunity[Supabase - Community]
        Qwen[Qwen Embeddings]
    end

    subgraph Layer4["LAYER 4: Agent Processing"]
        MCPAgent[MCP Analysis Agent]
        ContextAgent[Context Discovery Agent]
        SyncAgent[Sync Agent]
    end

    subgraph Layer5["LAYER 5: Documentation Output"]
        MkDocs[MkDocs Website]
        PublicAPI[Public API]
    end
```

**Layer 1: Analysis Sources** (Blue)
- IDA Pro: Local FF7 disassembly analysis
- FFNx Source: C++ implementation with documented hooks

**Layer 2: Knowledge Ingestion** (Purple)
- Forums & Wikis: Qhimm.com, community discussions
- External Content: Blogs, YouTube, Reddit, mod docs

**Layer 3: Data Storage** (Pink)
- **Neo4j**: Code structure (CALLS/READS/WRITES edges)
- **Supabase Code DB**: Function documentation + Qwen embeddings
- **Supabase Community DB**: Forum posts + Qwen embeddings
- **Qwen**: Local embedding generation (RTX 3070)

**Layer 4: Agent Processing** (Green)
- **MCP Analysis Agent**: IDA → documentation pipeline
- **Context Discovery Agent**: Community knowledge search
- **Sync Agent**: Bidirectional sync between databases

**Layer 5: Documentation Output** (Orange)
- **MkDocs Website**: Auto-generated from databases
- **Public API**: REST endpoints for external access

### Agent Workflows

**Workflow 1: Documenting Unknown Function**

```text
1. MCP Analysis Agent queries IDA at 0x6C9FF0
2. Gets disassembly showing texture loading code
3. Context Discovery Agent searches community DB: "FF7 texture loading"
4. Finds forum post explaining LZSS decompression
5. MCP Agent generates documentation combining:
   - Technical analysis (disassembly)
   - Community context (forum explanation)
6. Stores in Neo4j (code structure) + Supabase (docs + embeddings)
7. MkDocs regenerates site with new function page
```

**Workflow 2: User Searches "HP damage calculation"**

```text
1. User enters query on documentation website
2. Query sent to Public API /search endpoint
3. Qwen generates embedding for query
4. Searches BOTH databases:
   - Code DB: Finds calculateBattleDamage() function (95% match)
   - Community DB: Finds Qhimm forum "Damage Formula Explained" (88% match)
5. BGE Reranker refines top 50 results to top 5
6. Returns:
   - Function documentation with disassembly
   - Link to forum discussion
   - Related community posts
```

**Workflow 3: Modder Renames Function in IDA**

```text
1. Modder renames sub_401234 → addHealthPoints in IDA
2. Runs import_from_ida.py script
3. Sync Agent:
   - Updates Neo4j node with new name
   - Updates Supabase entity record
   - Adds entry to entity_versions table
4. Hourly GitHub Action regenerates MkDocs site
5. Documentation website now shows addHealthPoints
```

### Database Schemas

**Neo4j (Graph)**:

```cypher
// Nodes
(:Function {ida_address, current_name, original_name, size, confidence})
(:Variable {ida_address, current_name, data_type, scope})
(:Struct {name, size, fields})
(:BasicBlock {ida_address, parent_function, instructions})

// Relationships
(Function)-[:CALLS {call_address, call_type}]->(Function)
(Function)-[:READS {read_address}]->(Variable)
(Function)-[:WRITES {write_address}]->(Variable)
(Struct)-[:HAS_FIELD {offset}]->(Variable)
(Class)-[:INHERITS]->(Class)
(BasicBlock)-[:JUMPS_TO {condition}]->(BasicBlock)
```

**Supabase (PostgreSQL + pgvector)**:

```sql
-- Code documentation
CREATE TABLE entities (
    id BIGSERIAL PRIMARY KEY,
    ida_address BIGINT NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    current_name VARCHAR(255) NOT NULL,
    original_name VARCHAR(255) NOT NULL,
    description TEXT,
    markdown_content TEXT,
    confidence_score FLOAT DEFAULT 0.5,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(ida_address, entity_type)
);

CREATE TABLE entity_embeddings (
    id BIGSERIAL PRIMARY KEY,
    entity_id INTEGER REFERENCES entities(id),
    embedding vector(1024),  -- Qwen embeddings
    embedding_text TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE entity_versions (
    id BIGSERIAL PRIMARY KEY,
    entity_id INTEGER REFERENCES entities(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    markdown_content TEXT,
    changed_by VARCHAR(255),
    change_reason TEXT,
    confidence_score FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE contributions (
    id BIGSERIAL PRIMARY KEY,
    entity_id INTEGER REFERENCES entities(id),
    contributor_name VARCHAR(255),
    contribution_type VARCHAR(50),
    old_value TEXT,
    new_value TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    synced_to_ida BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Community knowledge
CREATE TABLE community_posts (
    id BIGSERIAL PRIMARY KEY,
    source_type VARCHAR(50),
    source_url TEXT,
    title TEXT,
    content TEXT,
    author VARCHAR(255),
    posted_at TIMESTAMP,
    scraped_at TIMESTAMP
);

CREATE TABLE community_embeddings (
    id BIGSERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES community_posts(id),
    embedding vector(1024),
    embedding_text TEXT
);

CREATE TABLE community_topics (
    id BIGSERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES community_posts(id),
    topic VARCHAR(255),
    relevance_score FLOAT
);
```

---

## Part 8: Technology Stack & Implementation

### Final Tech Stack

| Component | Technology | Justification |
|-----------|-----------|---------------|
| **IDA Pro** | Binary analysis tool | Industry standard for reverse engineering |
| **Neo4j** | Graph database | Optimal for code relationship traversals |
| **Supabase** | PostgreSQL + pgvector | Semantic search + local development |
| **Qwen** | Local embedding model | No API costs, runs on RTX 3070 |
| **BGE Reranker** | Two-stage search | 7-12x better accuracy than embeddings alone |
| **MkDocs** | Static site generator | Beautiful documentation websites |
| **FastAPI** | Public API backend | High-performance Python REST API |
| **GitHub Actions** | CI/CD | Auto-regenerate docs hourly |

### Performance Estimates

**For 5,000 FF7 Functions**:

**Embedding Generation** (one-time):
- Time: ~71 seconds (Qwen on RTX 3070)
- Storage: ~20MB (1024-dim × 5,000 × 4 bytes)

**Search Performance**:
- With reranker: ~477ms per query
- Without reranker: ~281ms per query
- Accuracy improvement: 3.5-12.8x better score separation with reranker

**Database Sizes**:
- Neo4j: ~50MB for 5,000 functions + relationships
- Supabase: ~100MB documentation + ~20MB embeddings
- Total: ~170MB

### Deployment Options

**Local Development**:
```bash
# Supabase
supabase start  # Full Docker stack

# Neo4j
docker run -p 7474:7474 -p 7687:7687 neo4j

# Qwen
# Runs on local RTX 3070 GPU
```

**Production**:
- **Supabase**: Free tier (500MB) or Pro ($25/mo)
- **Neo4j**: Aura free tier (200k nodes) or self-hosted
- **MkDocs**: GitHub Pages (free)
- **API**: Vercel or Railway (free tier)

---

## Part 9: IDA Pro MCP Testing (German Executable)

### User Action: Opened German ff7_de.exe

**Initial Confusion**: User opened German executable in new IDA window, both windows had remote control on port 9045.

**Testing**:
```python
# Query which executable is connected
mcp__ida_pro__run_ida_command("""
import idaapi
input_file = idaapi.get_input_file_path()
print(f"Currently loaded: {input_file}")
""")
```

**Result**: MCP was still connected to **English ff7_en.exe**, not German.

**Reason**: Both IDA instances running remote control on **same port (9045)**, MCP connects to first instance only.

**Solution**: User closed English IDA window.

**Verification After Closing English**:
```python
# Re-query
mcp__ida_pro__run_ida_command(...)

# Result:
# Currently loaded: D:\Games\Stand-alone\FINAL FANTASY VII\ff7_de.exe
# Database: D:\Games\Stand-alone\FINAL FANTASY VII\ff7_de.exe.i64
```

✅ **MCP successfully switched to German executable**

**Key Learning**:
- MCP server connects to one IDA instance at a time
- Multiple IDA windows must use different ports OR close one to switch
- Can configure different ports for simultaneous access (advanced)

---

## Key Findings & Decisions

### 1. Embeddings Are Cost-Effective

- **Local Qwen**: Zero cost, 1024-dim vectors, ~70 docs/sec
- **OpenAI alternative**: ~$0.01 for 5,000 functions (also cheap)
- **User's choice**: Local Qwen (no external dependencies)

### 2. Hybrid Database Architecture Is Optimal

- **Neo4j**: Code relationships (CALLS, READS, WRITES)
- **Supabase**: Documentation, search, versioning
- **Why both**: Each optimized for its purpose
- **Sync**: Metadata shared bidirectionally

### 3. Two Vector Databases for Two Knowledge Domains

- **Code DB**: Technical analysis from IDA/FFNx
- **Community DB**: Forums, wikis, blogs, Reddit
- **Combined power**: Technical + context = comprehensive docs

### 4. MkDocs Generated from Database

- **Source of truth**: Database (not markdown files)
- **Generation**: Hourly via GitHub Actions
- **Benefits**: Single source, auto-updates, version history
- **Optional**: Export to markdown for git backup

### 5. IDA Pro Multi-User via Export/Import Scripts

- **Simple approach**: Manual export/import scripts
- **Advanced**: IDA Python plugin with hotkeys
- **Conflict resolution**: Last write wins / approval workflow
- **Alternative**: Shared .i64 file (less scalable)

### 6. Supabase Over Neon

- **Local development**: Full Docker stack
- **Built-in features**: Auth, real-time, storage, API
- **Wiki needs**: Contributions require auth/moderation
- **Cost**: $25/mo Pro (acceptable for always-on docs)

### 7. Architecture is Scalable

- **5,000 functions**: ~71 seconds to embed, ~170MB storage
- **10,000+ functions**: Use FAISS for faster search
- **Community posts**: Scrape and index periodically
- **Real-time**: Supabase provides WebSocket updates

---

## Files Created

### Main Deliverable

**`/home/johnzealanddoyle/projects/tools/ff7-function-docs/FF7_DOCUMENTATION_SYSTEM_ARCHITECTURE.md`**

Contents:
- Complete Mermaid architecture diagram with color-coding
- Detailed explanation of all 5 layers
- Database schemas (Neo4j + Supabase)
- Agent workflow examples
- Technology stack breakdown
- Scalability analysis
- Deployment options
- 50+ pages of comprehensive documentation

### Session Tracking

**`/home/johnzealanddoyle/projects/tools/.project/cc_sessions/claude-1c5b37d9.txt`**

Resume command:
```bash
claude --resume 1c5b37d9-4924-4634-a8c4-2efbfcf46480
```

---

## Next Steps (Not Implemented - Research Phase Only)

### Immediate (Phase 1)
1. Set up Supabase local development (`supabase start`)
2. Create PostgreSQL schema with pgvector extension
3. Set up Neo4j Docker container
4. Test Qwen embedding generation with sample data

### Short-term (Phase 2)
1. Build IDA → Supabase sync script (export_to_ida.py)
2. Test with 10-20 FF7 functions
3. Implement Neo4j relationship tracking
4. Create basic MkDocs generation script

### Medium-term (Phase 3)
1. Build community scraping system (forums, wikis)
2. Populate community knowledge database
3. Implement combined search (code + community)
4. Deploy MkDocs site to GitHub Pages

### Long-term (Phase 4)
1. Public API for external access
2. User contribution system with moderation
3. Real-time collaboration features
4. Mobile app for documentation access

---

## Unanswered Questions / Future Considerations

1. **Community scraping ethics**: How to scrape forums respectfully?
   - Robots.txt compliance
   - Rate limiting
   - Attribution requirements

2. **Moderation workflow**: Who approves contributions?
   - Automated approval for high-confidence changes?
   - Community voting system?
   - Trusted contributor system?

3. **Address offset handling**: English vs German vs other versions
   - Previous session found +0x401600 offset for English
   - German may have different offset
   - Need to verify and document per-version offsets

4. **FFNx version tracking**: FFNx is actively developed
   - How to track which FFNx version documentation applies to?
   - Version-specific documentation branches?

5. **Cross-platform considerations**:
   - 1998 CD vs Steam vs eStore versions
   - Different executables, different addresses
   - How to handle in documentation?

---

## Technical Insights

### ★ Insight: Why Vector Similarity Works ─────────────────────────────

Embeddings transform text into high-dimensional space where semantic similarity becomes geometric proximity. Two concepts like "add health" and "increase HP" map to nearby points because they share contextual patterns in training data. This enables approximate nearest neighbor search algorithms (like pgvector's HNSW or FAISS) to find semantically related documents in milliseconds, even across millions of entries.

The two-stage approach (embedding retrieval + reranker) exploits speed vs accuracy trade-off: embeddings quickly narrow to top 50 candidates (~0.5ms), then cross-encoder reranker (which reads query+document together) precisely ranks them (~196ms). This achieves both speed AND accuracy.

─────────────────────────────────────────────────────────────────────

### ★ Insight: Graph Databases vs Relational for Code ───────────────

Relational databases store relationships as foreign keys requiring joins. For "what calls this function?" with 3 levels of indirection, PostgreSQL needs 3 joins. At 5 levels, performance degrades exponentially.

Graph databases store relationships as first-class edges with pointers. Traversing edges is O(1) regardless of depth - following 10 CALLS edges is 10 pointer lookups, not 10 joins. This matches how code naturally works: functions point to functions they call.

Neo4j's Cypher pattern matching also enables queries impossible in SQL: "find all functions with similar call patterns" (polymorphism detection) becomes a simple graph pattern match instead of complex self-joins.

─────────────────────────────────────────────────────────────────────

### ★ Insight: Dual Knowledge Domains ──────────────────────────────

Separating code knowledge from community knowledge prevents contamination but enables synthesis. Code analysis provides "what" (this function adds HP), community knowledge provides "why" (HP calculation uses ATK-DEF formula discovered by Qhimm users).

Storing them separately allows:
1. Different confidence scoring (disassembly = high, forum post = varies)
2. Different update cadences (code = on analysis, community = periodic scrape)
3. Independent search (sometimes you want just technical, sometimes just community context)
4. Combined search (usually you want both)

The agent layer synthesizes both into comprehensive documentation that would be impossible from either source alone.

─────────────────────────────────────────────────────────────────────

---

## Session Statistics

- **Duration**: ~4 hours
- **Main topics**: 9 major areas covered
- **Files created**: 2 (architecture doc + session file)
- **Lines of markdown**: ~1,500+ in architecture document
- **Database schemas designed**: 2 (Neo4j + Supabase)
- **Architecture diagrams**: 1 comprehensive 5-layer diagram
- **Example workflows**: 3 detailed workflows
- **Code examples**: 20+ across all sections
- **Technologies evaluated**: 6 (Supabase, Neon, Neo4j, Qwen, MkDocs, FAISS)

---

## Conclusion

This session successfully designed a comprehensive, scalable architecture for FF7 reverse engineering documentation that:

1. ✅ Combines technical code analysis with community knowledge
2. ✅ Uses local Qwen embeddings (no API costs)
3. ✅ Leverages Neo4j for code relationships + Supabase for docs/search
4. ✅ Enables multi-user collaboration via IDA sync scripts
5. ✅ Auto-generates beautiful MkDocs website
6. ✅ Provides public API for external access
7. ✅ Tracks version history of all changes
8. ✅ Supports user contributions with moderation

The architecture is **fully specified and ready for implementation** when the user is ready to move from research to development phase.

All design decisions were made collaboratively with detailed explanations of trade-offs, ensuring the user understands the "why" behind each choice.

---

**End of Session Summary**

**Status**: Architecture design complete, ready for implementation
**Next session**: Implementation of Phase 1 (database setup and initial sync scripts)
