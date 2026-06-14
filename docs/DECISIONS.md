# LedgerLens AI — Key Engineering Decisions

This document records all significant technical decisions made during the development of LedgerLens AI, including the options considered, tradeoffs analyzed, and rationale behind the final choice.

---

## 1. Frontend Framework: React vs Next.js

### Context
We needed a modern frontend framework for building the expense intelligence platform UI.

### Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **React + Vite** | - Faster initial setup<br>- Simple, lightweight<br>- Great developer experience<br>- Hot module replacement works seamlessly | - No built-in SSR/SSG<br>- Need to set up routing manually |
| **Next.js** | - Built-in routing<br>- SSR/SSG support<br>- Excellent SEO<br>- Production optimizations out of the box | - More complex<br>- Overkill for this project scope<br>- Slower initial load for development |

### Final Choice
**React + Vite**

### Rationale
- The project doesn't require SEO (internal business tool)
- Simpler stack means faster development and easier debugging
- Vite provides excellent development experience with instant feedback
- Avoided unnecessary complexity that doesn't add value for this use case

---

## 2. Backend Framework: Django vs FastAPI

### Context
We needed a robust backend framework with REST API support, authentication, and ORM.

### Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **Django REST Framework** | - Mature, battle-tested<br>- Built-in admin interface<br>- Excellent ORM<br>- Authentication out of the box<br>- Great for rapid development | - Heavier than FastAPI<br>- Slightly more boilerplate |
| **FastAPI** | - Blazing fast<br>- Automatic OpenAPI docs<br>- Modern async support<br>- Lightweight | - No built-in admin<br>- More manual setup for auth<br>- Less mature ecosystem for full-featured apps |

### Final Choice
**Django REST Framework**

### Rationale
- Django Admin is invaluable for debugging and data auditing during development
- Built-in authentication system saved significant development time
- Mature ORM handles complex relationships and queries elegantly
- The project doesn't need the extreme performance of FastAPI; Django is more than fast enough

---

## 3. Database: PostgreSQL vs SQLite

### Context
We needed a relational database for structured expense data.

### Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **PostgreSQL** | - Production-ready<br>- Excellent concurrency<br>- Advanced features<br>- Great for scaling | - Requires separate installation<br>- More complex setup<br>- Resource-heavy for local dev |
| **SQLite** | - Zero configuration<br>- Built into Python<br>- File-based, easy to backup<br>- Perfect for local development | - Not ideal for high concurrency<br>- No network access<br>- Limited advanced features |

### Final Choice
**SQLite (local), PostgreSQL (production)**

### Rationale
- SQLite for local development: Zero setup means recruiters can run the project in <5 minutes
- PostgreSQL in production: Takes advantage of Railway's managed PostgreSQL service
- Django ORM abstracts away database differences, so switching is seamless
- Best of both worlds: Easy development and production-ready scaling

---

## 4. AI Provider: NVIDIA NIM vs OpenAI

### Context
We needed an LLM API for generating insights and import summaries.

### Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **NVIDIA NIM** | - Powerful Llama models<br>- Competitive pricing<br>- Good for enterprise use cases | - Less familiar to many developers<br>- Smaller ecosystem |
| **OpenAI** | - Extremely popular<br>- Excellent documentation<br>- Wide range of models<br>- Great developer experience | - Higher pricing at scale<br>- Overused in demos; less unique |

### Final Choice
**NVIDIA NIM (with fallback)**

### Rationale
- NVIDIA NIM provides excellent performance for enterprise analytics use cases
- Standout choice compared to the overused OpenAI in coding assignments
- Implemented a robust deterministic fallback, so the app works perfectly even without an API key
- Demonstrates ability to work with multiple LLM providers

---

## 5. Hosting: Cloudflare vs Vercel

### Context
We needed a hosting platform for the frontend static assets.

### Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **Cloudflare Pages** | - Lightning-fast CDN<br>- Generous free tier<br>- Excellent global performance<br>- Easy to deploy | - Less feature-rich than Vercel for Next.js apps |
| **Vercel** | - Perfect for Next.js<br>- Great deployment experience<br>- Many convenience features | - More expensive at scale<br>- Overkill for React-only apps |

### Final Choice
**Cloudflare Pages**

### Rationale
- Cloudflare's edge network provides exceptional performance worldwide
- Generous free tier is perfect for this project
- Deployment process is straightforward and reliable
- Since we're using React (not Next.js), Vercel's Next-specific features aren't needed

---

## 6. Fallback Strategy: Rule-based Fallback vs AI-only System

### Context
What happens if the AI API is unavailable or no API key is provided?

### Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **AI-only System** | - Simpler architecture<br>- All features use AI | - App breaks if API fails<br>- Requires API key for basic functionality<br>- Risky for demos |
| **Rule-based Fallback** | - App works 100% without AI<br>- Graceful degradation<br>- Demo-friendly | - More code to write<br>- Need to maintain two systems |

### Final Choice
**Rule-based Fallback**

### Rationale
- Critical for coding assignments: The app must work perfectly when the recruiter runs it
- Deterministic logic provides consistent, predictable results
- AI enhances the app but isn't required for core functionality
- Demonstrates engineering judgment in prioritizing reliability over "flashy" features

---

## 7. Import Processing: Server-side vs Client-side

### Context
Should CSV parsing and anomaly detection happen on the server or client?

### Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **Client-side Only** | - Faster initial feedback<br>- Less server load | - No audit trail<br>- Security concerns<br>- Can't handle large files<br>- Duplicate detection is limited |
| **Server-side Processing** | - Full audit trail in database<br>- Better security<br>- Can handle large files<br>- Duplicate detection across imports | - Slightly more latency<br>- More server resources |

### Final Choice
**Server-side Import Processing**

### Rationale
- Audit trail is critical for an expense intelligence platform
- Server-side processing allows for cross-import duplicate detection
- Database persistence ensures no data loss
- Better security: No need to send sensitive expense data back and forth unnecessarily

---

## 8. Data Preservation: Keep All Data vs Purge Old Data

### Context
What data retention policy should we implement?

### Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **Keep All Data** | - Full historical record<br>- Audit trail forever<br>- Great for analytics | - Database grows indefinitely<br>- Privacy concerns |
| **Purge Old Data** | - Smaller database<br>- Better performance<br>- Complies with data minimization | - Lost historical insights<br>- No audit trail for old data |

### Final Choice
**Keep All Data (with proper access controls)**

### Rationale
- Historical data is invaluable for expense analytics and trend detection
- Full audit trail is a key feature of the platform
- For the scope of this assignment, storage concerns are negligible
- Demonstrates understanding of data importance for business intelligence

---

## 9. Anomaly Storage: Database vs In-memory

### Context
Should detected anomalies be stored in the database or only kept in memory during import?

### Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **In-memory Only** | - Faster<br>- Less database load | - No historical record<br>- Can't review past anomalies<br>- No audit trail |
| **Database-persisted** | - Full audit trail<br>- Can review past imports<br>- Historical anomaly analytics<br>- Better debugging | - More database writes<br>- Slightly slower imports |

### Final Choice
**Database-persisted Anomalies**

### Rationale
- Audit trail is a requirement for enterprise expense systems
- Historical anomaly data enables trend analysis (e.g., "are duplicate rates increasing?")
- Makes debugging import issues much easier
- The performance tradeoff is negligible for the project scope

---

## 10. UI Design: Professional SaaS vs Fun/Playful

### Context
What visual style should the application have?

### Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **Fun/Playful Design** | - More "visually interesting"<br>- Can show off animation skills | - Not appropriate for business/expense tool<br>- Distracts from core functionality |
| **Professional SaaS Design** | - Appropriate for business use case<br>- Clean and focused<br>- Recruiter-friendly | - Less "flashy"<br>- Fewer opportunities to show off animations |

### Final Choice
**Professional SaaS Design**

### Rationale
- The project is positioned as an enterprise expense intelligence platform
- Professional design demonstrates understanding of target audience
- Clean UI keeps focus on functionality, which is what matters most for a coding assignment
- Avoided unnecessary animations that don't add value

---

## Decision Log Template (for future decisions)

```markdown
## [Decision Number]. [Short Title]

### Context
[What problem are we solving? What's the background?]

### Options Considered

| Option | Pros | Cons |
|--------|------|------|
| [Option 1] | [List pros] | [List cons] |
| [Option 2] | [List pros] | [List cons] |

### Final Choice
[Choice made]

### Rationale
[Why this choice? What tradeoffs were prioritized?]
```
