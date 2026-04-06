# Social Profile Analyzer

Build personality profiles, digital twins, and communication guides from your social media data exports.

[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-blue)](https://github.com/Tomasz-T/social-profile-analyzer)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## The problem

You downloaded your Facebook/LinkedIn/Twitter data export. Now you have a pile of JSON and CSV files spanning years of your digital life. What do you do with it?

This skill reads your export, classifies every trait and interest by when it appeared and whether it's still active, and produces structured outputs you can actually use.

## What you get

| Output | What it is |
|--------|-----------|
| **Agent communication instructions** | Rules for an AI talking TO you. How you think, what you care about, how to phrase things for you. |
| **Digital twin** | Instructions for an AI to BE you. Your vocabulary, argument style, humor, opinions. Requires message data. |
| **Who-is self-reflection** | Full personality report with evidence. Traits, motivations, evolution over time, reflection prompts. |
| **Memories timeline** | Dated life events extracted from your data. Events, places, milestones, key posts. |

## Install

```bash
claude plugin marketplace add Tomasz-T/social-profile-analyzer
claude plugin install social-profile-analyzer
```

Then tell Claude something like: "Analyze my Facebook export at ~/Downloads/facebook-data" and the skill takes over.

## How it works

1. **Ask** what exports you have and which outputs you want
2. **Orient** by mapping the export structure to universal data categories
3. **Read recent data first** because who you are NOW matters more than who you were in 2012
4. **Sample historically** to detect how you've evolved
5. **Verify every count** against raw data (never trust file counts or agent summaries)
6. **Classify temporally** every trait as structural, stable, rising, declining, dormant, or phasic
7. **Assemble the profile** using a 7-tier evidence hierarchy weighted by signal strength
8. **Generate outputs** as self-contained markdown files
9. **Fact-check** every quantitative claim and recency assertion before delivering

## Platforms supported

Works with any platform that provides a data export with timestamped content:

| Platform | Export format | How to get it |
|----------|-------------|--------------|
| Facebook | JSON or HTML | Settings > Your Facebook Information > Download Your Information |
| LinkedIn | CSV | Settings > Data Privacy > Get a copy of your data |
| Twitter/X | JSON + HTML | Settings > Your Account > Download an archive of your data |
| Instagram | JSON or HTML | Settings > Your Activity > Download Your Information |
| Reddit | CSV | Settings > Privacy & Security > Request Your Data |

Other platforms with timestamped exports (TikTok, YouTube via Google Takeout, Mastodon, Bluesky) also work -- the skill maps any export structure automatically.

## Privacy

Your data never leaves your machine. Everything runs locally through Claude Code.

For extra safety, a bundled strip script lets you remove private content before analysis:

```bash
# Preview what would be removed
uv run scripts/strip_private.py /path/to/export --dry-run --remove-messages

# Strip message content but keep metadata (sender, timestamps)
uv run scripts/strip_private.py /path/to/export

# Remove message folders entirely
uv run scripts/strip_private.py /path/to/export --remove-messages
```

## What makes this different

Most "analyze my data" prompts treat years of content as a flat pool and produce vague summaries. This skill was built from real analysis failures:

- **Temporal classification** -- every trait gets a trajectory label (structural/stable/rising/declining/dormant/phasic) with first-seen and last-seen dates. A barefoot running interest from 2015 won't show up as current.
- **Anti-overstatement rules** -- N=1 is not a pattern, a page like is not an active interest, absence of recent evidence means dormant (not "still active").
- **Evidence hierarchy** -- 7 signal tiers from strongest (event attendance) to weakest (accepted a friend request). Claims are weighted accordingly.
- **Multi-platform merging** -- combine exports from different platforms. Cross-platform confirmation strengthens confidence; contradictions are noted as different facets, not errors.
- **Verification-first** -- every count is verified with a direct Python query against raw data. No trusting summaries.

## License

[MIT](LICENSE)
