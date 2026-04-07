---
name: social-profile-analyzer
description: Use when the user wants to build a person profile, personality analysis, digital twin, or communication guide from a social media data export. Works with ANY platform — Facebook, LinkedIn, Twitter/X, Instagram, Reddit, or any other export with timestamped personal data. Use this skill whenever the user says things like "analyze my Facebook export," "create a profile from my data," "who am I based on my social media," "build a digital twin from my messages," "personality report from LinkedIn," "generate agent instructions from my export," "process my data takeout," "analyze my GDPR export," "what does my data say about me," or "analyze my data download." Also trigger when the user provides a path to a social media data export folder, even if they don't explicitly ask for a "profile" or "analysis."
---

# Social Profile Analyzer

Build a person profile from social media data exports. Platform-agnostic — works with any export that contains timestamped personal data.

## Intended Use

This skill is a **self-discovery tool**. It helps people understand their own digital footprint — how they communicate, what they care about, and how they've evolved over time. Outputs like personality reports, digital twins, and memory timelines are designed for personal insight and AI personalization.

The user must be the data subject, or have their explicit consent. If analyzing someone else's data, confirm consent before proceeding. Digital twins used in conversations with others should be disclosed as AI.

## Step 1: Ask the User

Before any analysis, use AskUserQuestion:

**Question 1:** "What is the path to your data export folder(s)? You can provide multiple paths if combining sources. Is this your own data, or do you have the data subject's consent?"
- Free text input

**Question 2:** "Which outputs do you want?" (multi-select, default: all)
- Agent communication instructions — rules for an AI talking TO this person
- Digital twin — instructions for an AI to BE this person (uses message/chat data)
- Who-is self-reflection — personality, motivations, evolution, self-reflection prompts
- Memories timeline — dated events, places, people, milestones

If the user selects digital twin, message data will be included automatically. For other outputs, include messages by default — they enrich communication style analysis. If the user explicitly asks to exclude messages, respect that and note that digital twin output won't be available.

## Ground Rule: Verify Every Count

Never trust agent summaries, file counts, or row counts as proxies for actual data volume. A folder with 7 message files may contain 69,000 messages. A CSV with 2,863 rows may have multiline fields. Always run a direct Python query to count the actual entries before stating any number. This rule applies throughout every step below.

## Step 2: Orientation

1. List all files and folders in the export. Identify the platform from folder/file naming patterns.
2. **Map to data categories.** Every platform export maps to some subset of these universal categories:

| Category | What to look for | Examples |
|----------|-----------------|----------|
| **Profile** | Demographics, bio, quotes, headline | profile.json, Profile.csv |
| **Public content** | Posts, comments, articles with timestamps | posts.json, comments.json |
| **Interest signals** | Likes, follows, groups, pages with timestamps | pages_liked.json, Company Follows.csv |
| **Events** | Attended/registered events with dates | event_responses.json, Events.csv |
| **Network** | Connections, friends, followers with dates | friends.json, Connections.csv |
| **Messages** | Private conversations (if user opted in) | messages/inbox/, messages.csv |
| **Professional** | Career history, skills, certifications, education | Positions.csv, Certifications.csv |
| **Learning** | Courses, content consumed | Learning.csv, watch history |
| **Search/browsing** | Search queries, browsing history | search_history.json |
| **Algorithmic view** | How the platform categorizes this person | Ad_Targeting.csv |

3. Count volume per category. Note which categories are present vs missing.
4. Find timestamp range: earliest and latest entries across all data.

### Multi-Platform Merging

When the user provides exports from multiple platforms:

1. **Orient each platform separately.** Complete the category mapping above for each export before merging anything.
2. **Build a unified timeline.** Normalize all timestamps to the same format, then merge entries chronologically. Tag each entry with its source platform.
3. **Cross-reference contacts.** When the same person appears on multiple platforms (e.g., a LinkedIn connection who is also a Facebook friend), merge their signals. Overlapping evidence strengthens confidence in a trait.
4. **Expect contradictions.** Different platforms reveal different personas — a steady professional on LinkedIn and a restless experimenter on Facebook are both real facets of the same person. Note the contrast rather than resolving it.
5. **Don't double-count.** If the same event or action appears on both platforms (e.g., a job change reflected in both LinkedIn positions and a Facebook post), count it once but note the cross-platform confirmation.

## Step 3: Recent-First Reading

Start with the most recent data. This defines "who they are NOW."

1. Find the most recent **public content** (comments, posts) — read the last 200-300 entries (or all entries if fewer than 300 exist; for exports exceeding 100K entries, sample across the last 3-6 months rather than a fixed count)
2. Find the most recent **events** — what they attended recently
3. Find the most recent **interest signals** — sort by timestamp descending
4. If messages included: identify **top conversations by message count**

**Why recent-first:** The bulk of a multi-year export is historical. Starting from the beginning builds a portrait of who they WERE, not who they ARE.

## Step 4: Historical Sampling

Sample across the timeline to detect evolution:

1. **Early content** (first 200 entries of public content) for baseline personality
2. **Middle period** (~40-60% through) for transition
3. **Community content** (groups, forums) for domain engagement
4. If messages included: sample the **largest conversation** for private voice

## Step 5: Verification Queries

Every quantitative claim must be verified against raw data.

- Message counts: iterate files, count actual entries. CSV row count ≠ message count if messages are multiline.
- Date ranges: compute min/max timestamps
- Pattern claims: count occurrences. **N=1 is not a pattern — state the count.**
- "Viewed" or "started" ≠ "completed" or "achieved." State the actual status.

## Step 6: Temporal Classification

For every identified trait or interest, record:
- First seen (date), last seen (date)
- Number of data points
- Source types and platforms

Then classify:

| Label | Rule |
|-------|------|
| **Structural** | Visible across full timeline including recent data |
| **Stable** | Present in multiple periods AND confirmed in last 18 months |
| **Rising** | New or increasing, concentrated in recent period |
| **Declining** | Evidence thins recently |
| **Dormant** | Last evidence >2 years ago |
| **Phasic** | Appeared and disappeared in a defined window |

**Cross-platform confirmation strengthens confidence.** A trait visible on both Facebook AND LinkedIn is more reliable than one visible on only one platform.

**Cross-platform contradiction is informative.** Different platforms reveal different personas (e.g., steady professional on LinkedIn, restless experimenter on Facebook). Note the contrast — both may be real facets.

**Temporal clustering reveals phases.** When multiple follows/likes/actions cluster in a short time window (e.g., 5 stock-related follows in one week), that's a phase — tag it as phasic with the date window, not as a stable interest.

## Step 7: Profile Assembly

### Signal Strength Hierarchy
Weight evidence by signal type (platform-agnostic):

1. **Real-world action** — event attendance, job applications, certifications (strongest)
2. **Original content in communities** — comments, group posts
3. **Private messages** — actual conversations (strong, privacy-sensitive)
4. **Public posts with original text** — what they chose to broadcast
5. **Shared/amplified content** — what they endorsed
6. **Likes/follows** — one-time click (weak individually, strong in aggregate)
7. **Connections/friends** — accepted a request (weakest)

### Evidence Rules
- Every personality claim needs: quote or data point + date + source
- Use original-language quotes where they reveal personality
- State evidence count explicitly, not "consistent pattern"
- Traits tagged **structural** only if confirmed across multiple periods INCLUDING recent

### Anti-Overstatement Rules
- **N=1 is not a pattern.** State the count.
- **A like/follow ≠ active interest.** Event attendance >> page like.
- **Absence of recent evidence = dormant.** Not "still active."
- **Reduced platform activity ≠ reduced real-world activity.** Could be platform migration.
- **Don't project across time.** A runner in 2015 is not necessarily a runner in 2026.

## Step 8: Output Generation

All outputs must be **self-contained** — based only on the input data. No references to external files.

### Output Format

Save each output as a separate markdown file. Ask the user where to save them, or default to the export's parent directory.

| Output | Filename | Target length |
|--------|----------|---------------|
| Agent instructions | `agent-instructions.md` | 500-1000 words — terse rules only |
| Digital twin | `digital-twin.md` | 1000-2000 words — detailed voice patterns |
| Who-is self-reflection | `who-is.md` | 2000-4000 words — full report with evidence |
| Memories timeline | `memories-timeline.md` | Varies — one entry per significant event |

These are targets, not hard limits. A data-rich export may justify a longer who-is report; a sparse export may produce shorter outputs. The goal is enough detail to be useful without padding.

### Agent Communication Instructions
Pure rules. No backstory, no evidence, no trajectory tags.
- Only positive rules: what IS true, how the person communicates NOW
- Never "don't mention X" for things the agent wouldn't know without seeing this data
- Format: "Do X. When he says Y, it means Z."

### Digital Twin (requires messages)
Instructions for an AI to replicate this person's voice:
- Vocabulary patterns, frequent words, dismissal vocabulary
- Argument templates (e.g., concession-then-pivot, numbered rebuttals)
- Punctuation habits (emoticons vs emoji, formatting style)
- Register rules (how voice changes by audience/platform)
- Opinion positions on recurring topics
- Humor templates with examples
- Knowledge domains and depth per domain

### Who-Is Self-Reflection
Full personality report with evolution arc:
- Personality traits with evidence (quotes, dates)
- Motivations (current + evolved)
- Communication style analysis
- Interest map with trajectory labels
- Identity evolution timeline
- Prescriptive layer: "what this pattern suggests", reflection questions

### Memories Timeline
Structured extraction of dated life events:
- Events attended
- Check-ins and places
- Life milestones (career changes, purchases, profile changes)
- Group/community formations
- Key original posts

## Step 9: Fact-Check Pass

Before delivering any output:

1. **Search your generated report text for quantitative claims** (any numbers, counts, or frequency statements). Verify each against raw data.
2. **Search for external references** in your reports. Reports must reference only the input dataset.
3. **Check recency of every "IS" claim.** If evidence >18 months old, downgrade to historical.
4. **Check every "pattern" claim has N>3.** If not, state the count explicitly.

## Data Privacy

### Message exclusion
If the user explicitly asked to exclude messages, skip all message/DM data and note that digital twin output won't be available.

### Strip script
`scripts/strip_private.py` creates a safe copy with private content removed. Never modifies the original.

```bash
# Strip message content (keep metadata: sender, timestamps)
uv run scripts/strip_private.py /path/to/export

# Remove message folders entirely
uv run scripts/strip_private.py /path/to/export --remove-messages

# Also remove search history
uv run scripts/strip_private.py /path/to/export --remove-messages --remove-search

# Preview what would be removed
uv run scripts/strip_private.py /path/to/export --dry-run --remove-messages
```

Currently handles Facebook export structure. For other platforms, identify the equivalent private data paths (e.g., LinkedIn's `messages.csv`, Twitter's `direct-messages.js`) and either adapt the script or guide the user through manually removing those paths from a copy of their export before analysis.

## Platform-Specific Notes

Platform-specific file structures, timestamp formats, and gotchas are documented in `references/analysis_learnings.md` (relative to this skill directory). Consult that file during Orientation (Step 2) when mapping the export to data categories.

For unknown platforms, map the structure manually in Step 2 by checking:
- File formats (JSON, CSV, HTML, XML?)
- Timestamp format (Unix epoch seconds? milliseconds? human-readable?)
- Character encoding (UTF-8 clean? double-encoded?)
- File ordering (chronological ascending? descending? mixed?)
- Whether large data is split across multiple files

## Common Mistakes

Reinforces rules from Steps 5, 7, and 8. Quick reference for the fact-check pass.

| Mistake | Fix |
|---------|-----|
| Treating full timeline as flat pool | Recent-first reading (Step 3) + temporal classification (Step 6) |
| Trusting agent summaries for counts | Direct Python queries — always verify (Step 5) |
| Referencing external files in reports | Reports must be self-contained from input data only |
| "Don't mention X" in agent rules | Agent wouldn't know X — write only positive rules |
| Same person on two platforms = same persona | Note cross-platform contrasts as informative, not contradictory |
