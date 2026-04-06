# Facebook Data Analysis: Learnings

## Mistakes We Made

### 1. Trusting exploration agent summaries without verifying counts
The first exploration agent reported "2,500+ messages, 10+ years" for the core group chat. Actual data: **69,480 messages, ~7 years** (since May 2019). The agent counted message *files* (7), not messages. Always verify counts with direct queries.

### 2. Treating the full 17-year span as a flat pool
Initial profile described barefoot running as "Tier 1 identity-defining." Evidence was entirely from 2013-2018. Last group comment: 2016. No running content in 2024-2026. The trait was dormant, not active. **A person in 2026 is not the same person as in 2015.**

### 3. Overstating patterns from single occurrences
Claimed "uses @grok to fact-check" as a habitual behavior. Actual count: 3 uses total across all data (2 in comments, 1 in messenger). That's trying something out, not a pattern.

### 4. Not distinguishing page likes from active engagement
Liking a page is a one-time click. It does not prove ongoing interest. A page liked in 2022 may be muted or unfollowed by 2025. Page likes are weak signals — event attendance and comments are strong signals.

### 5. Projecting from public posts to private behavior
FB posting frequency dropped after 2020. We initially interpreted this as personality change. It could equally be platform migration (to WhatsApp, Signal, X). Reduced FB activity ≠ reduced activity.

### 6. Referencing external sources in self-contained reports
Reports referenced `user_profile.md` from a different project. Reports built from a dataset should be self-contained — only cite what the data shows.

### 7. Writing agent instructions for things the agent would never do
"Don't reference barefoot running as current" — an agent that hasn't seen the FB data would never mention barefoot running in the first place. Negative rules only make sense if the agent has access to the underlying data.

## What Worked

### 1. Temporal confidence framework
Tagging every trait/interest with trajectory (structural, stable, rising, declining, dormant, phasic) and first-seen/last-seen dates. This caught the barefoot running error and surfaced the consciousness turn as genuinely new.

### 2. Checking the actual most recent data points
Reading the last 200 lines of comments.json and the first events in event_responses.json (sorted most recent first) gave the ground truth for "who is this person NOW." The most recent comments (Nov 2025 – Mar 2026) told a different story than the bulk of posts (2009-2018).

### 3. Verifying specific claims with targeted queries
When challenged on the group chat duration, a direct Python query (`min/max timestamp_ms`) gave a definitive answer in seconds. Every quantitative claim should be verified this way before publishing.

### 4. Separating self-reflection report from agent-actionable report
Different audiences need different things. Self-reflection benefits from historical arc, Polish quotes, the full trajectory. An agent needs only: current traits, current interests, communication rules. Dormant interests and historical contrasts are noise for an agent.

### 5. Using quotes as evidence
Original Polish quotes make personality claims verifiable. "Analytical skeptic" is vague. *"IMHO autorka na podstawie doświadczeń swoich i najbliższych snuje sobie rozważania i bezprawnie rozszerza je na wszystkich z naszego rocznika"* is evidence.

## Data Structure Learnings (Facebook Export)

### File organization
```
facebook-{username}/
  personal_information/profile_information/profile_information.json
  your_facebook_activity/
    posts/your_posts__check_ins__photos_and_videos_1.json  (48K lines)
    comments_and_reactions/comments.json                    (49K lines)
    pages/pages_you've_liked.json                           (with timestamps)
    events/your_event_responses.json                        (with timestamps)
    groups/your_comments_in_groups.json
    messages/inbox/{conversation_folder}/message_{n}.json
  connections/friends/your_friends.json
  logged_information/your_search_history.json
```

### Key gotchas
- **UTF-8 double-encoding.** Polish characters in JSON are double-encoded: `\u00c5\u0082` instead of `ł`. Needs manual decoding for readable quotes.
- **Posts file is NOT purely chronological.** Starts ascending (~2009), but later sections appear to reverse or mix in photo albums and status changes. Don't assume line offset = time period.
- **Comments file IS chronological** (ascending by timestamp). Last lines = most recent.
- **Events are sorted most recent first.** First entries = current.
- **Pages liked have timestamps** — critical for temporal analysis.
- **Messages are split across files** when conversation is large (e.g., 7 files for 69K messages). Each file has its own `participants` and `messages` array.
- **Timestamps:** Posts/comments use Unix seconds. Messages use Unix milliseconds (`timestamp_ms`). Pages use Unix seconds.

### What each data source is good for

| Source | Good for | Not good for |
|--------|----------|--------------|
| **Comments** | Communication style, argument patterns, personality traits, opinions | Interests (comments are reactive, not proactive) |
| **Posts** | Self-expression, link sharing habits, humor style, what they choose to broadcast | Deep opinions (posts are performative) |
| **Pages liked** | Interest mapping with timestamps | Depth of engagement (a like ≠ active interest) |
| **Events** | Confirmed real-world actions, temporal precision | Frequency (many events go unregistered on FB) |
| **Group comments** | Community participation, domain expertise, how they engage in tribes | Breadth (only groups they comment in, not lurk) |
| **Messages** | Real communication style, relationship depth, topics of genuine concern | Privacy (should sample patterns, not mine content) |
| **Friends list** | Network size and selectivity | Relationship quality (friended ≠ close) |
| **Search history** | Real-time concerns and curiosity | Available only if logged |

### Signal strength hierarchy
1. **Event attendance** — they physically showed up (strongest)
2. **Comments in communities** — they engaged enough to write (strong)
3. **Message content** — what they actually discuss privately (strong, but privacy-sensitive)
4. **Posts with original text** — what they chose to say publicly (moderate-strong)
5. **Shared links/posts** — what they amplified (moderate)
6. **Pages liked** — one-time click (weak per-page, strong in aggregate patterns)
7. **Friend connections** — accepted a request (weakest)

## Data Structure Learnings (LinkedIn Export)

### File organization
```
Basic_LinkedInDataExport_{date}/
  Profile.csv              (demographics, headline, summary)
  Positions.csv            (career history with dates + descriptions)
  Education.csv            (schools, degrees)
  Skills.csv               (listed skills)
  Certifications.csv       (certs with completion dates — learning trajectory)
  Learning.csv             (LinkedIn Learning courses viewed — breadth signal)
  Connections.csv          (1,306 rows: name, company, position, connected date)
  Company Follows.csv      (interest trajectory with timestamps)
  Events.csv               (professional events)
  messages.csv             (all DMs — largest file, 1.3MB)
  Ad_Targeting.csv         (how LinkedIn categorizes the person)
  Endorsement_Given_Info.csv   (who they endorsed for what)
  Endorsement_Received_Info.csv (what skills others value in them)
  Recommendations_Given.csv / Recommendations_Received.csv
  Invitations.csv          (connection requests with messages)
  Jobs/
    Job Applications.csv, Saved Jobs.csv, Job Seeker Preferences.csv
```

### Key gotchas
- **CSV format, not JSON.** Use Python csv module or pandas. Messages are multiline — row count ≠ message count.
- **No UTF-8 encoding issues.** Clean Unicode, unlike Facebook's double-encoding.
- **Timestamps are human-readable** (e.g., "2026-03-26 14:41:53 UTC"), not Unix epoch.
- **Learning.csv "Viewed" ≠ "Completed."** 193 courses all marked "Viewed" with none completed. Treat as interest signal, not achievement.
- **Ad_Targeting.csv is one row** with massive concatenated fields. Parse carefully.
- **Basic export has no post/article content.** Only the "Complete" export includes published content.
- **Messages are thin compared to Facebook.** 2,863 LN messages vs 85K FB messages. LN messages are more transactional.

### What each data source is good for

| Source | Good for | Not good for |
|--------|----------|--------------|
| **Positions.csv** | Career arc, employer loyalty, role progression | Day-to-day work (descriptions are sparse) |
| **Certifications.csv** | Learning trajectory with precise dates | Actual skill depth (cert ≠ expertise) |
| **Learning.csv** | Interest breadth — reveals hidden curiosities (drawing, 3D, game dev) | Depth (viewed ≠ studied) |
| **Company Follows** | Interest trajectory over time (timestamps show phases) | Active engagement (follow ≠ read) |
| **Endorsements Given** | Who they value professionally, skill recognition patterns | Reciprocity gaming (many endorse back) |
| **Saved Jobs** | Career aspiration direction | Current intent (may be years old) |
| **Ad_Targeting** | How LinkedIn's algorithm categorizes the person | Accuracy (algorithmic inference, not self-report) |
| **messages.csv** | Professional communication style, key relationships | Depth (thin compared to FB messenger) |
| **Connections.csv** | Network size, employer clusters, connection timing | Relationship quality (connected ≠ close) |

### Certification dates predict career moves
Certifications often precede a job change by 6-18 months. When building a career trajectory, map cert dates against position start dates to identify deliberate pivots vs. opportunistic moves.

### Cross-platform analysis notes
- **LinkedIn reveals the professional persona. Facebook reveals the personal persona.** These can appear contradictory (e.g., 17-year employer loyalty on LN vs. counter-cultural restlessness on FB). Both are real — they're different facets.
- **Company Follows on LN** have timestamps and show interest phases clearly (e.g., gaming stocks cluster June 2020, biotech cluster Nov 2021, AI companies Dec 2023).
- **Certifications + Company Follows together** show career pivot timing: process mining certs (2021) → process mining companies followed (2021) → KYP.ai role (2022).
- **Overlap in names** between FB friends and LN connections confirms which relationships span both personal and professional life.

## Analysis Flow

### Phase 1: Orientation
1. Map the export structure. List all top-level folders and file sizes.
2. Read `profile_information.json` for demographics, dates, quotes, bio.
3. Count lines in key files (posts, comments) to gauge volume.
4. Check the timestamp range: earliest and latest entries in posts and comments.

### Phase 2: Recent-First Reading
5. Read the **last 200-300 lines** of `comments.json` — this is the most recent activity and defines "who they are now."
6. Read the **first entries** of `event_responses.json` (most recent first) — what they actually attended recently.
7. Read **pages liked**, sorted by timestamp descending — what interests are current.
8. Identify the **top conversations by message count** — who they actually talk to.

### Phase 3: Historical Sampling
9. Read **early posts** (first 200 lines) for baseline personality and early interests.
10. Sample posts from **middle periods** (offset to ~40-60% of file) for evolution.
11. Read **group comments** for community participation and domain engagement.
12. Read a **sample of the largest message thread** for private communication style.

### Phase 4: Verification Queries
13. For any quantitative claim, run a **direct Python/SQL query** against the JSON data. Don't trust summaries.
    - Message counts: iterate message files, count `messages` array lengths
    - Date ranges: `min/max timestamp_ms`
    - Frequency of a term: grep or Python count
14. For any "this person does X" claim, find the **count of occurrences** and the **last occurrence date**.

### Phase 5: Temporal Classification
15. For each identified trait or interest, record:
    - First seen (date)
    - Last seen (date)
    - Number of data points
    - Source types (comments? posts? pages? events?)
16. Classify as: **structural** (spans full timeline), **stable** (multiple periods + confirmed recent), **rising** (new/intensifying), **declining** (thins recently), **dormant** (no recent signal), **phasic** (appeared and disappeared).

### Phase 6: Profile Assembly
17. Write personality traits — only those tagged **structural** (confirmed across multiple periods including recent).
18. Write current interests — only those tagged **stable** or **rising** with 2024+ evidence.
19. Write communication style — draw from comments (public) and messages (private), note register differences.
20. Include original-language quotes as evidence for key claims.
21. State the evidence basis: quote count, date range, source type.

### Phase 7: Output Separation
22. **Self-reflection report**: Full historical arc, quotes, trajectory labels, evolution timeline. For the subject to read.
23. **Agent-actionable report**: Only current state. No historical contrasts. No "don't mention X" for things the agent wouldn't know. Positive rules only (what IS true, not what WAS true).

### Phase 8: Fact-Check Pass
24. Grep reports for any quantitative claims ("10+ years", "2,500 messages", "habitually uses X"). Verify each against raw data.
25. Grep for external references (other files, projects, assumptions from outside the dataset). Remove or replace with data-derived statements.
26. For each "this person IS [trait]" — confirm the most recent evidence is within 18 months. If older, downgrade to historical.
