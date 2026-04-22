# Token Usage Log

**Purpose:** Track daily token usage to monitor z.ai subscription value and anticipate renewal needs

## How to Check Current Usage

```bash
openclaw status
```

**Key Metrics:**
- `Tokens: X in / Y out` — Tokens used / monthly limit
- `Cost: $0.XXXX` — Actual cost incurred
- `Usage: Monthly XX% left` — Quota remaining
- `Cache: XX% hit` — Efficiency metric (higher = better)

---

## Monthly Summary

### April 2026

| Date | Daily Tokens | Tokens Used | Tokens Left | Cost | Cache Hit | Notes |
|-------|---------------|--------------|-------------|-------|------------|
| 2026-04-03 | 86k | 86k / 547k | 461k (84.3%) | $0.0000 | 12% | Model switches (GLM 4.7 → Claude 3.5 Sonnet → gemini 2.5-flash → GLM 4.7) |

**Daily Average (so far):** 86k / 1 day = 86k tokens/day

---

## Daily Log

### 2026-04-03 (Friday)

| Time | Tokens Used | Tokens Left | Cost | Notes |
|-------|--------------|-------------|-------|-------|
| 4:36 PM (end of session) | 86k / 547k | 461k (84.3%) | $0.0000 | First check on new session (Claude 3.5 Sonnet → gemini 2.5-flash → GLM 4.7) |

---

## Questions to Track

- **Daily average usage:** How many tokens do I typically use per day?
- **Peak days:** Heavy sessions (coding, analysis) vs. light days (casual chat)
- **Monthly burn rate:** Am I hitting my monthly limit?
- **Cost efficiency:** Cache hit rate, compaction rate (look for higher %)
- **Value assessment:** Am I getting good value from z.ai subscription?

---

## When to Renew

**Subscription renews:** 6 weeks from now

**Decision factors:**
- Am I consistently hitting monthly limits?
- Do I need more tokens for heavier workflows?
- Is current plan sufficient for my usage patterns?
- Should I upgrade/downgrade before renewal?

---

**Last updated:** 2026-04-03
