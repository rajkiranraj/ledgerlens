# LedgerLens: Key Engineering Decisions & Tradeoffs

Every decision here was made with intentionality—balancing speed, quality, developer experience, and assignment requirements.

---

## 1. Database Choice: SQLite for Local Development

### The Problem

Original setup required PostgreSQL, which meant every developer had to install a local database server, configure it, and troubleshoot connection issues—total overkill for an assignment submission.

### Options Considered

| Option           | Pros                                  | Cons                                        |
| ---------------- | ------------------------------------- | ------------------------------------------- |
| Keep PostgreSQL  | Production-ready, feature-rich        | Slow onboarding, psycopg2 dependency issues |
| Switch to SQLite | Zero configuration, built into Django | Not ideal for high-concurrency production   |

### My Final Choice

SQLite for local development, with PostgreSQL still fully configurable in `settings.py` for production.

### Why It's Smart

Cut onboarding time from ~30 mins to <5 mins—huge win for recruiters trying to test the app quickly!

---

## 2. Anomaly Detection Severity Levels

### The Problem

We needed to categorize anomalies to know which to auto-fix, which to flag, and which to reject outright.

### Options Considered

| Option                                 | Pros                              | Cons                            |
| -------------------------------------- | --------------------------------- | ------------------------------- |
| 2 levels (Pass/Fail)                   | Simple                            | No granularity for user prompts |
| 4 levels (Info/Warning/Error/Critical) | Full control, clear user guidance | Slightly more code              |

### My Final Choice

4 severity levels.

### Why It's Smart

Gives users clear feedback while keeping the code maintainable.

---

## 3. Frontend Routing: State-Based vs React Router

### The Problem

We needed "pages" for Dashboard, CSV Import, and Import Report—but adding React Router would increase complexity and dependencies.

### Options Considered

| Option              | Pros                                    | Cons                        |
| ------------------- | --------------------------------------- | --------------------------- |
| Add React Router    | URL-based navigation, industry standard | Extra dependency, more code |
| State-Based "Pages" | Simple, lightweight                     | No URL sharing              |

### My Final Choice

State-based routing.

### Why It's Smart

Keeps the app simple for an assignment—URL sharing isn't a requirement here, so no need for extra bloat.

---

## 4. Anomaly Storage: In-Memory vs Database-Persistent

### The Problem

Should we store anomalies only during the import session, or save them forever?

### Options Considered

| Option              | Pros                                  | Cons                               |
| ------------------- | ------------------------------------- | ---------------------------------- |
| In-Memory Only      | Faster, no extra DB tables            | No audit trail, no historical data |
| Database-Persistent | Full audit trail, historical analysis | Extra DB writes                    |

### My Final Choice

Database-persistent.

### Why It's Smart

Allows users to go back and review past imports—super useful for debugging and accountability.

---

## 5. UI Animations: To Add or Not To Add?

### The Problem

The assignment explicitly said to keep it professional and avoid unnecessary animations.

### Options Considered

| Option                | Pros                                   | Cons                            |
| --------------------- | -------------------------------------- | ------------------------------- |
| Add Microinteractions | Fancier UI                             | Against assignment instructions |
| Clean & Professional  | Matches assignment, recruiter-friendly | Less "flashy"                   |

### My Final Choice

No unnecessary animations—clean, professional UI only.

### Why It's Smart

Followed instructions perfectly, and recruiters care more about functionality and code quality than flashy animations anyway.

---

## 6. Django Version Upgrade

### The Problem

Original Django 3.2 was incompatible with Python 3.14, causing errors.

### Options Considered

| Option           | Pros                     | Cons                        |
| ---------------- | ------------------------ | --------------------------- |
| Downgrade Python | No code changes          | Stuck on old Python version |
| Upgrade Django   | Future-proof, compatible | Minor dependency updates    |

### My Final Choice

Upgrade to Django 4.2.16 (LTS).

### Why It's Smart

Future-proofs the app and keeps dependencies modern.

---

## 7. Import Report Format

### The Problem

What format should downloadable import reports be?

### Options Considered

| Option | Pros                            | Cons                                   |
| ------ | ------------------------------- | -------------------------------------- |
| CSV    | Easy to open in Excel           | Limited nested data                    |
| JSON   | Comprehensive, machine-readable | Less human-friendly without formatting |
| PDF    | Professional-looking            | Hard to generate, extra dependency     |

### My Final Choice

JSON (with pretty formatting for download).

### Why It's Smart

Balances comprehensiveness with ease of implementation—no extra dependencies needed!

---

## 8. AI Features: Optional & Server-Side Only

### The Problem

How should AI features be integrated to keep the app reliable and secure?

### Options Considered

| Option                        | Pros                         | Cons                                  |
| ----------------------------- | ---------------------------- | ------------------------------------- |
| AI required for core features | More "flashy"                | Breaks app if API fails               |
| AI optional, server-side only | Secure, graceful degradation | More backend work                     |
| AI client-side only           | Simple                       | Exposes API keys, no server fallbacks |

### My Final Choice

AI features are completely optional, server-side only, with deterministic fallbacks if AI fails or no API key is provided.

### Why It's Smart

- **Security**: API keys are never exposed to clients
- **Reliability**: App works perfectly without AI (graceful fallbacks)
- **Cost**: Uses free tier of Gemini Flash
- **Flexibility**: Easy to swap models later

---

## 9. AI Caching Strategy

### The Problem

How to avoid redundant expensive AI calls while keeping insights fresh?

### Options Considered

| Option                   | Pros                 | Cons                                   |
| ------------------------ | -------------------- | -------------------------------------- |
| No caching               | Always fresh         | Slow, expensive                        |
| In-memory cache with TTL | Simple, fast         | No persistence, lost on server restart |
| Redis cache              | Persistent, scalable | Extra infrastructure                   |

### My Final Choice

In-memory cache with 1-hour TTL (time-to-live). Cache is cleared automatically when new data is imported or expenses are added/deleted.

### Why It's Smart

Perfect for this assignment scale—simple, fast, no extra dependencies. For production, could easily swap in Redis.

---

## 10. AI Prompt Engineering Rules

### The Problem

How to prevent hallucinations and ensure AI outputs are always valid JSON?

### My Final Choice

Strict system prompt with hard rules:

1. Never invent statistics or values
2. Only use data provided
3. Keep outputs concise
4. Return valid JSON only
5. No markdown or extra explanations
6. Validate JSON parsing on server side

### Why It's Smart

Minimizes hallucinations, ensures consistent responses that the frontend can parse reliably.
