# FFNx Crowdsourced Translation System - Viability Assessment

**Document Version:** 1.0
**Created:** 2026-01-16 12:14 JST (Friday)
**Session ID:** 1025061b-d84f-4164-9c29-e4e1f682ab19
**Author:** Claude Code (Sonnet 4.5)
**Purpose:** Comprehensive assessment of the crowdsourced translation specification's viability for integration with a web-based analytics and community platform

---

## TABLE OF CONTENTS

1. [Executive Summary](#executive-summary)
2. [Context Review](#context-review)
3. [Specification Analysis](#specification-analysis)
4. [Extended Vision Assessment](#extended-vision-assessment)
5. [Technical Feasibility by Feature](#technical-feasibility-by-feature)
6. [Architecture Gaps](#architecture-gaps)
7. [Implementation Recommendations](#implementation-recommendations)
8. [Risk Analysis](#risk-analysis)
9. [Conclusions](#conclusions)

---

## Executive Summary

### The Question

The user asked about the viability of the FFNx Crowdsourced Translation System specification for integrating FF7 into a website platform with:
- **Analytics tracking** (where players are in the game)
- **Collaborative translation editing** (updating field dialogue)
- **In-game messaging** (leaving messages for each other in the game world)
- **Dual display** (analytics visible both in-game and on website)

### The Verdict

**The specification is technically sound for its stated scope (translation submission and voting) but incomplete for the extended vision.**

**Viability Tiers:**
- **Tier 1 (High Viability):** Translation submission, web voting, moderator approval, .iro export
- **Tier 2 (Medium Viability):** Session-based analytics, player progression tracking, translation comparison views
- **Tier 3 (Lower Viability):** Real-time translation hot-swap, in-game messaging system, persistent world markers

### Key Finding

The specification excels at what it targets (crowdsourced translation workflow) but does not address the real-time bidirectional game↔server communication required for analytics and messaging features. These would require significant additional architecture.

---

## Context Review

### Documents Analyzed

1. **SESSION_CONTEXT_19-28_NAMING_SCREEN.md** (1,207 lines)
   - FFNx Japanese naming screen implementation (Sessions 19-28)
   - Memory address mapping, HEXT patches, character encoding
   - Demonstrates FFNx's hook infrastructure capabilities

2. **SceneSessionContextDirectory.md** (496 lines)
   - Sessions 1-16 context: Japanese text rendering, font system
   - PR #737 integration, multi-language architecture
   - Shows existing FFNx modification patterns

3. **naming_screen_tables.txt** (362 lines)
   - Character encoding tables for naming screen
   - Hiragana/Katakana/Eisuu table layouts
   - Encoding validation patterns

4. **FFNX_DEVELOPER_GUIDE.md** (2,310 lines)
   - FFNx architecture overview
   - PR #737 (Japanese text support) deep dive
   - Hook system, rendering pipeline, build system
   - Critical for understanding integration points

5. **FFNX_CROWDSOURCED_TRANSLATION_SPEC.md** (1,729 lines)
   - The specification under review
   - Client-side (FFNx) implementation details
   - Server-side API, database schema, deployment
   - User workflows and security measures

### Existing FFNx Work (Relevant Context)

The user has completed extensive FFNx modifications:
- **Sessions 1-28:** Japanese text rendering system
- **PR #737 integration:** Multi-page font textures (FA-FE encoding)
- **HEXT patching experience:** Memory address manipulation
- **Character width tables:** 1,536 values for proper rendering
- **Hook infrastructure:** Function interception, memory reading

This existing work provides a solid foundation for the translation system but doesn't yet include bidirectional server communication or real-time state synchronization.

---

## Specification Analysis

### What the Spec Covers Well

#### 1. Client-Side Translation Capture (Strong)

**Hotkey Detection:**
```cpp
// Ctrl+T (keyboard) or L3+R3 (controller)
void CheckTranslationHotkeys() {
    if (IsKeyPressed(VK_CONTROL) && IsKeyJustPressed('T')) {
        TriggerTranslationSubmission();
    }
}
```

**Context Capture:**
```cpp
struct DialogueContext {
    char field_id[16];         // "md1_1" (current field map)
    uint16_t string_id;        // 0x42 (dialogue index)
    uint8_t window_id;         // 0-3 (which text box)
    char character_name[32];   // "Cloud" (speaker)
    char* text_pointer;        // Actual displayed text
    uint32_t scene_timestamp;  // Game frame counter
};
```

**Memory Addresses (US 1.02 - Approximate):**
| Data | Address | Type | Notes |
|------|---------|------|-------|
| `field_id` | `0x9A82D0` | `char[16]` | Current map name |
| `dialogue_index` | `0xDBFD38` | `uint16_t` | Script string index |
| `active_window` | `0xDC08D8` | `uint8_t` | 0-3 for text boxes |
| `current_text_buffer` | `0xE04318` | `char[256]` | Currently displayed text |

**Assessment:** This approach is solid and aligns with the user's existing FFNx work. The memory addresses need verification via debugger, but the methodology is sound.

#### 2. Encoding Validation (Strong)

```cpp
bool ValidateTranslation(const char* text, int language) {
    // Check length
    if (len > 255) return false;

    // For CJK languages, validate character support
    if (language == LANG_JA || language == LANG_ZH_TW) {
        const char* ptr = text;
        while (*ptr) {
            uint32_t codepoint = UTF8ToCodepoint(ptr, &ptr);
            if (!CharacterSupported(codepoint, language)) {
                return false; // Character not in font texture
            }
        }
    }

    // Estimate encoded size (FA-FE takes 2 bytes per extended char)
    size_t encoded_size = EstimateEncodedSize(text, language);
    if (encoded_size > 255) return false;

    return true;
}
```

**Assessment:** Critical feature that leverages the user's existing character mapping work (Sessions 1-16, naming screen character tables). This prevents invalid submissions.

#### 3. HTTP Submission (Standard)

```cpp
// Uses libcurl for HTTPS POST
bool SubmitTranslation(DialogueContext ctx, int language, const char* text) {
    json payload = {
        {"string_id", StringFormat("%s:%04X", ctx.field_id, ctx.string_id)},
        {"language", GetLanguageCode(language)},
        {"translation", text},
        {"timestamp", GetISO8601Timestamp()},
        {"username", GetUsername()},
        {"game_version", "steam_2013"},
        {"ffnx_version", FFNX_VERSION}
    };

    CURL* curl = curl_easy_init();
    curl_easy_setopt(curl, CURLOPT_URL, TRANSLATION_API_ENDPOINT);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, payload.dump().c_str());
    // ... SSL verification, timeout, response handling
}
```

**Assessment:** Straightforward implementation using standard libraries. No concerns here.

#### 4. Server-Side Architecture (Solid)

**Database Schema:**
```sql
CREATE TABLE translations (
    id SERIAL PRIMARY KEY,
    string_id VARCHAR(32) NOT NULL,        -- "md1_1:0x42"
    language VARCHAR(8) NOT NULL,          -- "ja", "zh-tw", etc.
    translation TEXT NOT NULL,
    username VARCHAR(64),
    status VARCHAR(16) DEFAULT 'pending',  -- pending, approved, rejected
    created_at TIMESTAMP DEFAULT NOW(),
    votes_up INTEGER DEFAULT 0,
    votes_down INTEGER DEFAULT 0,
    approved_by VARCHAR(64),
    approved_at TIMESTAMP
);

CREATE TABLE votes (
    id SERIAL PRIMARY KEY,
    translation_id INTEGER REFERENCES translations(id),
    username VARCHAR(64) NOT NULL,
    vote_type VARCHAR(8) NOT NULL,        -- "upvote", "downvote"
    comment TEXT,
    UNIQUE (translation_id, username)
);

CREATE TABLE contexts (
    id SERIAL PRIMARY KEY,
    string_id VARCHAR(32) UNIQUE NOT NULL,
    field_map VARCHAR(16),
    scene_description TEXT,
    screenshot_url TEXT,
    previous_line TEXT,
    next_line TEXT,
    speaker VARCHAR(32)
);
```

**Assessment:** Well-designed schema. The `contexts` table is particularly valuable for providing translators with scene context.

**REST API (FastAPI):**
- `POST /api/submit` - Submit new translation
- `GET /api/translations/{string_id}` - Get all translations for a string
- `POST /api/vote` - Vote on translation
- `POST /api/approve/{translation_id}` - Moderator approval
- `GET /api/review/pending` - Moderation queue

**Assessment:** Clean RESTful design. Rate limiting and authentication are properly considered.

#### 5. Security Measures (Comprehensive)

**Client-Side Rate Limiting:**
- 50 submissions per day
- 1 submission per 10 seconds

**Server-Side Protection:**
- Redis-based rate limiting (100 requests/hour per IP)
- Profanity filter
- XSS/SQL injection prevention (parameterized queries)
- Vote manipulation detection (IP tracking, username correlation)
- JWT authentication for moderators

**Assessment:** Appropriate for the scale. The dual rate limiting (client + server) prevents both accidental spam and malicious abuse.

#### 6. Deployment Strategy (Realistic)

**Infrastructure:**
- Docker Compose (API, Database, Redis, Web UI, Nginx)
- PostgreSQL 14+ for data
- FastAPI (Python) or Express (Node.js) for backend
- React/Svelte for frontend

**Cost Estimate:** ~$45/month (2 vCPU, 4GB RAM server + PostgreSQL managed instance)

**Assessment:** Accurate cost estimate. The Docker setup is production-ready and scalable.

### What the Spec Does NOT Cover

#### 1. Real-Time Game State Synchronization

**Missing:** How to push approved translations BACK into the running game.

The spec is **read-only** on the client side. It captures context and sends data to the server, but there's no mechanism for:
- Loading updated translations from the server while the game is running
- Hot-swapping translation tables in FFNx memory
- Notifying the game when new translations are approved

**Impact:** Players must download .iro packages via 7th Heaven and restart the game to see updated translations. No live updates.

#### 2. Continuous Analytics Collection

**Missing:** Persistent telemetry for tracking player location and progression.

The spec captures context only when Ctrl+T is pressed. For the user's vision of "tracking where players are in the game," you'd need:
- **Polling mechanism:** Periodic (every N seconds) reporting of field_id, position, party status
- **Event-based tracking:** Trigger on scene transitions, battle starts, dialogue completion
- **Privacy controls:** Opt-in/opt-out, anonymization
- **Server infrastructure:** High-frequency telemetry endpoint (separate from translation API)

**Impact:** Cannot build "heat maps" of player locations or "current players on this scene" features without additional architecture.

#### 3. In-Game Messaging System

**Missing:** Rendering user-generated content in the game world.

The spec focuses on dialogue box text. For "leaving messages for each other" (Dark Souls bloodstain-style), you need:
- **Custom rendering layer:** New draw calls separate from dialogue boxes
- **World coordinate tracking:** X/Y/Z position, not just field_id
- **Message persistence:** Database of messages per location
- **Moderation at scale:** Real-time review (different from translation approval workflow)
- **UI for message creation:** Keyboard input system (can reuse naming screen work)

**Impact:** This is a separate project with different technical requirements.

#### 4. Bidirectional Communication

**Missing:** WebSocket or polling for server→client updates.

The spec uses one-way HTTP POST (client→server). For features like:
- "See live analytics on screen while playing"
- "Receive notifications of approved translations"
- "Download new translations without restarting"

You need:
- **WebSocket connection:** Persistent socket for push notifications
- **Polling loop:** FFNx periodically checks server for updates
- **State synchronization:** Handle conflicts (local vs. remote translation versions)

**Impact:** Cannot implement real-time features without adding this infrastructure.

---

## Extended Vision Assessment

The user's vision extends beyond the spec in four key areas:

### Feature 1: Analytics Tracking (Where Players Are)

**User's Goal:** Track player location, scene progression, time spent in each area. Display analytics both in-game and on website.

#### What's Needed (Not in Spec)

**Client-Side (FFNx):**
```cpp
// New module: src/ff7/analytics_telemetry.cpp

struct TelemetryData {
    char field_id[16];
    uint32_t timestamp;
    uint32_t playtime_seconds;
    uint16_t party_members[3];
    uint8_t current_level;
    bool in_battle;
    // ... other metadata
};

void SendTelemetryUpdate() {
    if (!analytics_enabled) return;

    TelemetryData data = CaptureCurrentState();

    // Non-blocking HTTP POST
    std::thread([data]() {
        SendToAnalyticsEndpoint(data);
    }).detach();
}

// Call every 30 seconds or on scene transition
void ff7_frame_hook() {
    static uint32_t last_telemetry = 0;
    uint32_t now = GetFrameCount();

    if (now - last_telemetry > 30 * 60) { // 30 seconds at 60fps
        SendTelemetryUpdate();
        last_telemetry = now;
    }
}
```

**Server-Side (New Endpoint):**
```python
@app.post("/api/analytics/track")
async def track_player_location(data: TelemetryData):
    # Store in time-series database (InfluxDB or TimescaleDB)
    await db.execute("""
        INSERT INTO player_telemetry
        (field_id, timestamp, playtime, party, level, in_battle)
        VALUES ($1, $2, $3, $4, $5, $6)
    """, data.field_id, data.timestamp, ...)

    # Aggregate for "players currently on this scene"
    await redis.zincrby("active_players", 1, data.field_id)
    await redis.expire(f"player:{username}:heartbeat", 60)

    return {"status": "ok"}

@app.get("/api/analytics/scene/{field_id}")
async def get_scene_analytics(field_id: str):
    # Return stats for website dashboard
    active_players = await redis.zscore("active_players", field_id)
    avg_time = await db.query("SELECT AVG(playtime) FROM telemetry WHERE field_id = $1", field_id)

    return {
        "active_players": active_players,
        "average_time_spent": avg_time,
        "total_visits": ...,
        "heat_map": ...
    }
```

**In-Game Display (FFNx):**
```cpp
// Render analytics overlay using ImGui (already in FFNx)
void RenderAnalyticsOverlay() {
    if (!show_analytics_overlay) return;

    // Fetch from server (cached)
    auto stats = GetSceneAnalytics(current_field_id);

    ImGui::Begin("Scene Analytics");
    ImGui::Text("Players currently here: %d", stats.active_players);
    ImGui::Text("Average time: %d minutes", stats.avg_time / 60);
    ImGui::Text("Total visits: %d", stats.total_visits);
    ImGui::End();
}
```

**Challenges:**
1. **Privacy:** Always-on tracking requires opt-in consent, anonymization
2. **Performance:** Non-blocking HTTP requests to avoid game stuttering
3. **Battery/Network:** Mobile users may not want constant telemetry
4. **Server cost:** High-frequency data ingestion (thousands of players × 30 sec intervals)

**Viability:** **Medium** - Technically feasible but requires significant additional infrastructure not in the spec.

### Feature 2: Collaborative Translation Editing

**User's Goal:** Update field dialogue translations in real-time, visible to all players without restarting.

#### What's Needed (Not in Spec)

**Hot-Reload Translation Tables:**

The spec exports approved translations as .iro packages. To enable live updates:

```cpp
// New module: src/ff7/translation_hotswap.cpp

struct TranslationCache {
    std::unordered_map<std::string, std::string> translations; // string_id -> text
    uint32_t last_sync_timestamp;
};

static TranslationCache cache;

void PollForUpdates() {
    // Check server for new translations
    auto response = FetchJSON("/api/translations/updates?since=" + cache.last_sync_timestamp);

    if (response.has_updates) {
        for (auto& update : response.translations) {
            cache.translations[update.string_id] = update.text;
        }
        cache.last_sync_timestamp = response.timestamp;

        ffnx_info("Loaded %d updated translations\n", response.translations.size());
    }
}

// Hook into dialogue rendering
void RenderDialogue(uint16_t string_id) {
    char string_key[32];
    sprintf(string_key, "%s:%04X", current_field_id, string_id);

    // Check cache first
    if (cache.translations.count(string_key)) {
        std::string& updated_text = cache.translations[string_key];
        RenderText(updated_text.c_str()); // Use cached translation
        return;
    }

    // Fall back to original game text
    RenderOriginalText(string_id);
}
```

**Server-Side:**
```python
@app.get("/api/translations/updates")
async def get_translation_updates(since: int):
    # Return all approved translations since timestamp
    updates = await db.query("""
        SELECT string_id, translation, approved_at
        FROM translations
        WHERE status = 'approved' AND approved_at > $1
        ORDER BY approved_at ASC
    """, since)

    return {
        "has_updates": len(updates) > 0,
        "translations": updates,
        "timestamp": int(time.time())
    }
```

**Challenges:**
1. **Memory management:** Storing all translations in RAM (FFNx already has ~1536 character widths loaded)
2. **Concurrency:** Thread-safe updates while game is rendering
3. **Version conflicts:** What if local .iro and server have different versions?
4. **Testing:** Ensuring hot-swapped text doesn't break dialogue boxes (length, encoding)

**Viability:** **Medium** - Technically possible (FFNx already dynamically loads textures) but requires careful memory management and testing. Not in spec at all.

### Feature 3: In-Game Messaging System

**User's Goal:** Leave messages for other players in the game world (like Dark Souls bloodstains).

#### What's Needed (Not in Spec)

**Message Rendering System:**

This is fundamentally different from dialogue boxes:

```cpp
// New module: src/ff7/world_messages.cpp

struct WorldMessage {
    uint32_t message_id;
    char field_id[16];
    float x, y, z;              // 3D world coordinates
    char text[128];
    char author[32];
    uint32_t upvotes;
    uint32_t timestamp;
};

// Fetch messages for current location
std::vector<WorldMessage> GetMessagesForLocation() {
    auto response = FetchJSON("/api/messages?field_id=" + current_field_id);
    return ParseMessages(response);
}

// Render markers in 3D space
void RenderWorldMessages() {
    auto messages = GetMessagesForLocation();

    for (auto& msg : messages) {
        // Convert world coords to screen coords
        Vector2 screen_pos = WorldToScreen(msg.x, msg.y, msg.z);

        // Draw icon at position
        DrawSprite("message_icon.png", screen_pos.x, screen_pos.y);

        // If player is close, show text
        float distance = DistanceToPlayer(msg.x, msg.y, msg.z);
        if (distance < 5.0f) {
            DrawText(msg.text, screen_pos.x, screen_pos.y + 20);
            DrawText(msg.author, screen_pos.x, screen_pos.y + 40);
        }
    }
}

// Create new message
void CreateWorldMessage() {
    // Get player position
    Vector3 pos = GetPlayerPosition();

    // Show input dialog (reuse naming screen keyboard)
    char message_text[128];
    if (ShowMessageInputDialog(message_text, sizeof(message_text))) {
        // Submit to server
        PostJSON("/api/messages", {
            {"field_id", current_field_id},
            {"x", pos.x}, {"y", pos.y}, {"z", pos.z},
            {"text", message_text},
            {"author", username}
        });
    }
}
```

**Server-Side:**
```python
@app.post("/api/messages")
async def create_message(data: MessageCreate):
    # Validate
    if len(data.text) > 128:
        raise HTTPException(400, "Message too long")

    if not is_valid_location(data.field_id, data.x, data.y, data.z):
        raise HTTPException(400, "Invalid location")

    # Store
    message_id = await db.execute("""
        INSERT INTO world_messages (field_id, x, y, z, text, author)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING id
    """, data.field_id, data.x, data.y, data.z, data.text, data.author)

    return {"message_id": message_id}

@app.get("/api/messages")
async def get_messages(field_id: str, limit: int = 50):
    messages = await db.query("""
        SELECT id, x, y, z, text, author, upvotes, created_at
        FROM world_messages
        WHERE field_id = $1
        ORDER BY created_at DESC
        LIMIT $2
    """, field_id, limit)

    return messages
```

**Challenges:**
1. **3D rendering:** FFNx uses BGFX renderer; adding custom sprites requires understanding the rendering pipeline
2. **World coordinates:** FF7 uses complex coordinate systems (field vs. world map vs. battle)
3. **Position tracking:** Finding player X/Y/Z coordinates (different memory addresses per scene type)
4. **Moderation:** Real-time review needed (unlike translations which can wait for approval)
5. **Spam prevention:** Much easier to spam short messages than write translations
6. **Performance:** Rendering 50+ messages per scene without FPS drop

**Viability:** **Low** - This is a separate project requiring:
- Deep understanding of FF7's 3D engine
- Custom rendering layer in FFNx
- Real-time moderation system
- Significantly more complex than the translation spec

### Feature 4: Dual Display (In-Game + Website)

**User's Goal:** Show analytics both on the website dashboard and as an in-game overlay.

#### What's Needed (Partially in Spec)

**Website Dashboard:** ✅ The spec covers this well with React/Svelte frontend.

**In-Game Overlay:** ❌ Not in spec.

**Implementation (FFNx already has ImGui):**

```cpp
// FFNx already includes ImGui for DevTools
// Can extend for analytics display

void RenderStatsOverlay() {
    if (!show_stats) return;

    ImGui::SetNextWindowPos(ImVec2(10, 10));
    ImGui::Begin("FF7 Community Stats", &show_stats,
                 ImGuiWindowFlags_NoResize | ImGuiWindowFlags_AlwaysAutoResize);

    // Fetch from server (cached, updated every 60 seconds)
    auto stats = GetCommunityStats();

    ImGui::Text("Players online: %d", stats.online_players);
    ImGui::Text("Players on this scene: %d", stats.scene_players);
    ImGui::Separator();
    ImGui::Text("Translation progress: %.1f%%", stats.translation_coverage);
    ImGui::Text("Pending submissions: %d", stats.pending_translations);

    if (ImGui::Button("Submit Translation (Ctrl+T)")) {
        TriggerTranslationSubmission();
    }

    ImGui::End();
}
```

**Challenges:**
1. **UI design:** Making it look consistent with FF7's aesthetic (not default ImGui style)
2. **Performance:** HTTP requests for stats must be async and cached
3. **Toggle hotkey:** Needs to not conflict with game controls

**Viability:** **High** - FFNx already has ImGui integrated (from FFNX_DEVELOPER_GUIDE.md Section 11.1). This is straightforward.

---

## Technical Feasibility by Feature

### Summary Table

| Feature | Spec Coverage | Additional Work | Viability | Estimated Effort |
|---------|---------------|-----------------|-----------|------------------|
| **Translation Submission** | ✅ Comprehensive | Minimal (debugger to find addresses) | **High** | 5-10 hours |
| **Web Voting Dashboard** | ✅ Complete | None | **High** | 20-30 hours |
| **Moderator Approval** | ✅ Complete | None | **High** | 10-15 hours |
| **`.iro` Export** | ✅ Outlined | Implementation | **High** | 15-20 hours |
| **Session Analytics** | ⚠️ Partial | Telemetry system | **Medium** | 30-40 hours |
| **Live Translation Updates** | ❌ Not covered | Hot-reload system | **Medium** | 40-50 hours |
| **In-Game Stats Overlay** | ❌ Not covered | ImGui extension | **High** | 10-15 hours |
| **World Messaging System** | ❌ Not covered | Complete subsystem | **Low** | 80-100 hours |

### Detailed Feasibility Analysis

#### High Viability Features (Use Spec As-Is)

**1. Translation Submission Workflow**
- **Spec quality:** 9/10
- **Gaps:** Memory addresses need verification
- **Alignment with user's work:** Perfect - leverages naming screen experience
- **Recommendation:** Implement exactly as specified

**2. Web Dashboard & Voting**
- **Spec quality:** 8/10
- **Gaps:** UI/UX mockups not included
- **Technology:** Standard React/FastAPI stack
- **Recommendation:** Follow spec, use existing web frameworks

**3. Moderator Queue**
- **Spec quality:** 9/10
- **Gaps:** Bulk operations could be more detailed
- **Security:** Well-considered (JWT, rate limiting)
- **Recommendation:** Implement as specified

#### Medium Viability Features (Significant Extension Needed)

**4. Player Analytics & Tracking**
- **Spec coverage:** Captures context on Ctrl+T only
- **Gap:** No continuous telemetry
- **New architecture needed:**
  - Polling loop in FFNx (every 30-60 seconds)
  - Time-series database (InfluxDB/TimescaleDB)
  - Aggregation endpoints for website
- **Privacy concerns:** Opt-in required, GDPR compliance
- **Recommendation:** Start with minimal telemetry (scene transitions only), expand later

**5. Hot-Reload Translation System**
- **Spec coverage:** Static .iro export only
- **Gap:** No mechanism for live updates
- **New architecture needed:**
  - Translation cache in FFNx memory
  - Polling endpoint for updates
  - Version conflict resolution
  - Thread-safe rendering hooks
- **Testing burden:** High (must not break existing dialogue)
- **Recommendation:** Implement as Phase 2 feature after core translation submission is stable

#### Low Viability Features (Separate Project)

**6. World Messaging System**
- **Spec coverage:** None
- **Complexity:** High (3D rendering, position tracking, real-time moderation)
- **Prerequisites:**
  - Deep FF7 engine knowledge
  - BGFX rendering expertise
  - Understanding of field/world/battle coordinate systems
- **Effort:** ~100 hours minimum
- **Recommendation:** Defer to Phase 3 or separate project. Consider prototype first to assess feasibility.

---

## Architecture Gaps

### Gap 1: Bidirectional Communication

**Current (Spec):** Client → Server (HTTP POST only)

**Needed:** Client ↔ Server (WebSocket or polling)

**Use cases:**
- Push notifications of approved translations
- Live stats updates
- Message notifications

**Solution Options:**

**Option A: WebSocket**
```cpp
// FFNx client
WebSocketClient ws("wss://ff7translations.yoursite.com/ws");

ws.on_message([](const std::string& msg) {
    auto data = json::parse(msg);

    if (data["type"] == "translation_approved") {
        // Reload translation cache
        ReloadTranslations();
    } else if (data["type"] == "stats_update") {
        // Update analytics overlay
        UpdateStatsDisplay(data["stats"]);
    }
});
```

**Pros:** Real-time, low latency
**Cons:** Persistent connection overhead, requires WebSocket library in FFNx

**Option B: Polling**
```cpp
void PollServerUpdates() {
    static uint32_t last_poll = 0;
    uint32_t now = GetFrameCount();

    if (now - last_poll > 60 * 60) { // Every 60 seconds
        std::thread([]() {
            auto updates = FetchJSON("/api/updates?since=" + last_check);
            ProcessUpdates(updates);
        }).detach();

        last_poll = now;
    }
}
```

**Pros:** Simpler, no persistent connection
**Cons:** Higher latency, more HTTP requests

**Recommendation:** Start with polling (simpler), upgrade to WebSocket if real-time is critical.

### Gap 2: Translation Versioning & Conflicts

**Scenario:** Player has .iro package v1.0 installed. Server approves new translation. What happens?

**Current (Spec):** Player must manually download new .iro and restart.

**Needed:** Conflict resolution strategy.

**Solution:**
```cpp
struct TranslationVersion {
    std::string source;  // "iro", "server", "local"
    uint32_t priority;   // Higher = takes precedence
    uint32_t timestamp;
};

std::string GetTranslation(const std::string& string_id) {
    std::vector<TranslationCandidate> candidates;

    // Check all sources
    if (auto iro_text = GetFromIRO(string_id))
        candidates.push_back({iro_text, "iro", 1, iro_timestamp});

    if (auto server_text = GetFromCache(string_id))
        candidates.push_back({server_text, "server", 2, server_timestamp});

    if (auto local_text = GetFromLocalOverride(string_id))
        candidates.push_back({local_text, "local", 3, local_timestamp});

    // Return highest priority
    std::sort(candidates.begin(), candidates.end(),
              [](auto& a, auto& b) { return a.priority > b.priority; });

    return candidates.empty() ? GetOriginalText(string_id) : candidates[0].text;
}
```

**Recommendation:** Server translations override .iro when both exist. Document this behavior clearly.

### Gap 3: Screenshot Context Capture

**Spec mentions:** Screenshot URLs in `contexts` table.

**Not specified:** How screenshots are captured and uploaded.

**Solution:**
```cpp
void TriggerTranslationSubmission() {
    // Capture screenshot (FFNx can do this - see FFNX_DEVELOPER_GUIDE.md)
    std::vector<uint8_t> screenshot = CaptureFramebuffer();

    // Upload to image host (Imgur, Cloudinary)
    std::string screenshot_url = UploadScreenshot(screenshot);

    // Include in context
    DialogueContext ctx = CaptureCurrentDialogue();
    ctx.screenshot_url = screenshot_url;

    OpenTranslationSubmissionDialog(ctx);
}
```

**Recommendation:** Add this to spec. Use external image host (Cloudinary free tier: 25GB storage, 25GB bandwidth/month).

### Gap 4: Testing Strategy

**Spec includes:** Security testing (rate limiting, profanity filter).

**Missing:**
- Integration testing (FFNx ↔ Server)
- Load testing (1000 concurrent users)
- Translation quality testing (encoding validation)

**Recommendation:**
```python
# tests/integration/test_submission_flow.py

def test_full_submission_workflow():
    # 1. Mock FFNx client submits translation
    response = client.post("/api/submit", json={
        "string_id": "md1_1:0x42",
        "language": "ja",
        "translation": "テスト翻訳",
        "username": "test_user"
    })
    assert response.status_code == 201

    # 2. Verify stored in database
    translation = db.query(Translation).filter_by(string_id="md1_1:0x42").first()
    assert translation.status == "pending"

    # 3. Moderator approves
    response = client.post(f"/api/approve/{translation.id}",
                          headers={"Authorization": f"Bearer {moderator_token}"})
    assert response.status_code == 200

    # 4. Verify status changed
    translation = db.query(Translation).get(translation.id)
    assert translation.status == "approved"

    # 5. Verify appears in export
    export = generate_iro_package()
    assert "テスト翻訳" in export["data/kernel/KERNEL.BIN"]
```

---

## Implementation Recommendations

### Phased Approach

#### Phase 1: Core Translation System (MVP) - 60-80 hours

**Goal:** Prove the concept end-to-end.

**Deliverables:**
1. FFNx translation submission (Ctrl+T hotkey)
2. Basic API (submit endpoint only)
3. Simple web page showing submissions
4. No voting, no moderation, no analytics

**Success criteria:** User can submit translation in-game, see it on website.

**Estimated timeline:** 2-3 weeks (part-time)

#### Phase 2: Voting & Moderation - 40-60 hours

**Additions:**
1. Complete voting system
2. Moderator dashboard with approval queue
3. User authentication (GitHub OAuth)
4. Rate limiting and security
5. .iro export pipeline

**Success criteria:** Community can vote, moderators can approve, translations get packaged into .iro files.

**Estimated timeline:** 2-3 weeks (part-time)

#### Phase 3: Lightweight Analytics - 30-40 hours

**Additions:**
1. Simple telemetry hook (field_id transitions only)
2. Aggregated stats endpoint (players per scene, time spent)
3. ImGui overlay showing stats

**Success criteria:** Players can see "X players currently here" and "average time: Y minutes" for each scene.

**Estimated timeline:** 1-2 weeks (part-time)

#### Phase 4: Hot-Reload Translations - 40-50 hours

**Additions:**
1. Translation cache in FFNx
2. Polling endpoint for updates
3. Thread-safe hot-swap during gameplay

**Success criteria:** Approved translations appear in-game without restart.

**Estimated timeline:** 2-3 weeks (part-time)

#### Phase 5 (Optional): World Messaging - 80-100 hours

**Additions:**
1. 3D position tracking
2. Custom rendering layer
3. Message creation UI
4. Real-time moderation

**Success criteria:** Players can leave messages visible to others in 3D space.

**Estimated timeline:** 4-6 weeks (part-time)

### Technology Stack Recommendations

**Based on user's existing work (from context documents):**

**FFNx Modifications (C++):**
- Keep using the existing PR #737 infrastructure
- Reuse naming screen keyboard input system for message composition
- Use ImGui (already integrated) for overlays
- Add libcurl dependency for HTTP (standard, widely supported)

**Server Backend:**
```python
# FastAPI (Python) - Recommended
# Pros: Fast to develop, excellent async support, auto-generated docs
# Cons: Smaller ecosystem than Node.js

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
# ... (as in spec)
```

**Alternative:**
```javascript
// Express (Node.js/TypeScript)
// Pros: Larger ecosystem, easier to find developers
// Cons: Slightly more boilerplate for async operations

import express from 'express';
import { PrismaClient } from '@prisma/client';
// ... (TypeScript provides type safety)
```

**Database:**
- **Development:** SQLite (zero setup)
- **Production:** PostgreSQL 14+ (mature, well-documented, free tier on Render/Railway)

**Frontend:**
```typescript
// Svelte + Vite (Recommended based on user's ff7-landscaper project)
// User already uses Svelte in ff7-landscaper, ff7-ultima

<script lang="ts">
  import { onMount } from 'svelte';

  let translations: Translation[] = [];

  onMount(async () => {
    const res = await fetch('/api/translations/pending');
    translations = await res.json();
  });
</script>

{#each translations as t}
  <TranslationCard translation={t} />
{/each}
```

**Deployment:**
- **Docker Compose** (as in spec) - good for self-hosting
- **Fly.io/Render** - cheap managed hosting ($5-10/month for starter tier)

### Code Organization

```
ff7-translation-platform/
├── ffnx/                          # FFNx modifications
│   ├── src/
│   │   ├── ff7/
│   │   │   ├── translation_submission.cpp
│   │   │   ├── translation_cache.cpp      # Phase 4
│   │   │   ├── analytics_telemetry.cpp    # Phase 3
│   │   │   └── world_messages.cpp         # Phase 5
│   │   └── common/
│   │       └── http_client.cpp
│   └── docs/
│       └── INTEGRATION.md
│
├── server/                        # Backend API
│   ├── api/
│   │   ├── routes/
│   │   │   ├── translations.py
│   │   │   ├── votes.py
│   │   │   ├── moderation.py
│   │   │   └── analytics.py          # Phase 3
│   │   ├── models/
│   │   │   ├── translation.py
│   │   │   ├── vote.py
│   │   │   └── user.py
│   │   └── main.py
│   ├── alembic/                   # Database migrations
│   ├── tests/
│   │   ├── test_submission.py
│   │   └── test_voting.py
│   └── requirements.txt
│
├── web/                           # Frontend
│   ├── src/
│   │   ├── routes/
│   │   │   ├── +page.svelte       # Dashboard
│   │   │   ├── review/+page.svelte
│   │   │   └── moderation/+page.svelte
│   │   ├── components/
│   │   │   ├── TranslationCard.svelte
│   │   │   └── VoteButton.svelte
│   │   └── lib/
│   │       └── api.ts
│   ├── package.json
│   └── vite.config.ts
│
├── docker-compose.yml
├── README.md
└── docs/
    ├── API.md
    ├── DEPLOYMENT.md
    └── CONTRIBUTING.md
```

---

## Risk Analysis

### Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Memory addresses change between game versions** | High | High | Version detection, multiple address tables |
| **Hot-reload causes game crashes** | Medium | High | Extensive testing, fallback to .iro export |
| **WebSocket connection instability** | Medium | Medium | Implement reconnection logic, fallback to polling |
| **Database performance under load** | Low | Medium | Use PostgreSQL (handles 1000s of writes/sec), add indexes |
| **FFNx conflicts with other mods** | Medium | Low | Test with popular mods, document compatibility |

### Security Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Spam submissions** | High | Medium | Client + server rate limiting (implemented in spec) |
| **Profanity/offensive content** | High | High | Profanity filter + moderator approval (implemented) |
| **Vote manipulation** | Medium | Medium | IP tracking, username correlation (implemented) |
| **SQL injection** | Low | Critical | Parameterized queries (spec uses SQLAlchemy ORM) |
| **XSS in web dashboard** | Low | High | Input sanitization, CSP headers |
| **DoS attack** | Medium | High | Cloudflare CDN (free tier includes DDoS protection) |

### Project Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Scope creep** | High | High | **Stick to phased approach**, resist adding features |
| **User adoption low** | Medium | Medium | Start with JP community (most motivated for translations) |
| **Moderator burnout** | Medium | High | Build reputation system, distribute workload |
| **Server costs exceed budget** | Low | Medium | Start with cheap hosting, scale only if needed |
| **Competing solution emerges** | Low | Low | Open-source the project, focus on quality |

---

## Conclusions

### What the Spec Does Well

1. **Solid foundation for translation workflow** - The core submission → voting → approval → export pipeline is well-designed.
2. **Realistic security measures** - Rate limiting, profanity filtering, vote manipulation detection are appropriate.
3. **Practical deployment strategy** - Docker Compose setup and cost estimates are accurate.
4. **Good use of existing FFNx infrastructure** - Leverages the user's Sessions 1-28 work (naming screen, character encoding).

### What's Missing for the Extended Vision

1. **Bidirectional communication** - No WebSocket/polling for server→client updates.
2. **Continuous analytics** - Only captures context on Ctrl+T, not periodic telemetry.
3. **Hot-reload mechanism** - No way to update translations without restart.
4. **World messaging system** - Completely separate project not addressed by spec.

### Recommended Path Forward

**Start with the spec as-written (Phases 1-2):**
- Implement core translation submission and voting system
- Deploy basic web dashboard and moderator queue
- Get real users submitting translations

**Then evaluate before extending:**
- If users love it → Add analytics (Phase 3)
- If hot-reload is critical → Implement caching system (Phase 4)
- If messaging is demanded → Prototype separately (Phase 5)

### Final Assessment

**For the spec as-written:** **8/10 viability** - Excellent design for its stated scope. Minor gaps in testing strategy and screenshot handling.

**For the extended vision:** **5/10 viability** - Translation + voting is solid. Analytics requires medium effort. Messaging system is a major separate project.

**Bottom line:** The spec is production-ready for crowdsourced translation workflow. The analytics and messaging features require significant additional architecture not covered in the spec. Build the core first, then evaluate if the extended features are worth the 80-100 additional hours of development.

---

## Appendix: Quick Reference

### Memory Addresses Needed (US 1.02)

These are approximate - must verify with debugger:

```cpp
// From FFNX_CROWDSOURCED_TRANSLATION_SPEC.md Section 3.1
char* const FIELD_ID = (char*)0x9A82D0;                // Current map ("md1_1")
uint16_t* const DIALOGUE_INDEX = (uint16_t*)0xDBFD38;  // String index
uint8_t* const ACTIVE_WINDOW = (uint8_t*)0xDC08D8;     // Text box 0-3
char* const TEXT_BUFFER = (char*)0xE04318;             // Displayed text

// Additional (for analytics)
uint32_t* const FRAME_COUNTER = (uint32_t*)0xDC0788;   // Game frame count
uint8_t* const PARTY_MEMBERS = (uint8_t*)0xDBFD98;     // Party array
```

### API Endpoints Summary

```
POST   /api/submit              # Submit translation
GET    /api/translations/{id}   # Get translations for string
POST   /api/vote                # Vote on translation
POST   /api/approve/{id}        # Moderator approval
GET    /api/review/pending      # Moderation queue

# Phase 3 additions:
POST   /api/analytics/track     # Telemetry data
GET    /api/analytics/scene/{id} # Scene stats

# Phase 4 additions:
GET    /api/translations/updates # Poll for new translations

# Phase 5 additions:
POST   /api/messages             # Create world message
GET    /api/messages             # Get messages for location
```

### Estimated Total Effort

| Phase | Deliverables | Hours | Timeline (Part-Time) |
|-------|--------------|-------|----------------------|
| Phase 1 | MVP (submission only) | 60-80 | 2-3 weeks |
| Phase 2 | Voting & moderation | 40-60 | 2-3 weeks |
| Phase 3 | Basic analytics | 30-40 | 1-2 weeks |
| Phase 4 | Hot-reload | 40-50 | 2-3 weeks |
| Phase 5 | World messages | 80-100 | 4-6 weeks |
| **Total** | **All features** | **250-330 hours** | **11-17 weeks** |

**For comparison:**
- Core spec (Phases 1-2): 100-140 hours
- Extended vision (all phases): 250-330 hours
- **Extended features add ~150 hours (2x the core)**

---

**Document Complete**

*For technical implementation details, see:*
- `FFNX_CROWDSOURCED_TRANSLATION_SPEC.md` (the specification reviewed)
- `FFNX_DEVELOPER_GUIDE.md` (FFNx architecture and PR #737 integration)
- `SESSION_CONTEXT_19-28_NAMING_SCREEN.md` (user's existing FFNx work)
