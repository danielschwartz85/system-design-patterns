# System Design Patterns

A tutorial on the **8 system design patterns that keep coming up** in system design interviews, written as a small static website: one landing page plus one page per pattern.

[https://danielschwartz85.github.io/system-design-patterns/](https://danielschwartz85.github.io/system-design-patterns/)

Each page explains what the pattern is, why it exists, how it works, the trade-offs an interviewer will probe, concrete technologies, when *not* to use it, and how to say it out loud in an interview. Diagrams are inline SVG and work in light and dark mode.

## The patterns

| # | Pattern | The problem it solves |
|---|---------|-----------------------|
| 01 | [Scaling Reads](patterns/01-scaling-reads.html) | Reads outgrow the database: indexes, replicas, caches, CDNs |
| 02 | [Scaling Writes](patterns/02-scaling-writes.html) | Writes outgrow one database: sharding, consistent hashing, queues, batching, load shedding |
| 03 | [Dealing with Contention](patterns/03-contention.html) | Many users change the same data: conditional writes, locks, optimistic concurrency control |
| 04 | [Handling Large Blobs](patterns/04-large-blobs.html) | Big uploads and downloads: pre-signed URLs, multipart uploads, CDN delivery |
| 05 | [Long-Running Tasks](patterns/05-long-running-tasks.html) | Work that outlasts a request: queues, workers, retries, dead-letter queues |
| 06 | [Real-Time Updates](patterns/06-real-time-updates.html) | Pushing updates to clients: polling, SSE, WebSockets, pub/sub, hash-ring routing |
| 07 | [Multi-Step Processes](patterns/07-multi-step-processes.html) | Workflows across services: the saga pattern, Temporal, Step Functions |
| 08 | [Proximity Search](patterns/08-proximity-search.html) | Finding things near a location: geohash, quadtrees, S2, H3, PostGIS, Redis GEO |

Three techniques that appear inside several patterns get a full "why it exists, how it works" write-up:

- **Consistent hashing**: in [Scaling Writes](patterns/02-scaling-writes.html), applied in [Real-Time Updates](patterns/06-real-time-updates.html)
- **Optimistic concurrency control**: in [Dealing with Contention](patterns/03-contention.html)
- **The saga pattern**: in [Multi-Step Processes](patterns/07-multi-step-processes.html)

[Long-Running Tasks](patterns/05-long-running-tasks.html#messaging-models) also compares work queues with pub/sub, and Kafka with RabbitMQ (with a short answer in [Scaling Writes](patterns/02-scaling-writes.html)).

## Viewing it

There is no build step and no dependencies. Open `index.html` in a browser:

```bash
# either double-click index.html, or serve the folder:
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Exporting a PDF

To get the whole tutorial (overview plus all eight patterns) as a single PDF:

```bash
python3 scripts/build-pdf.py
# writes dist/system-design-patterns.pdf
```

The script merges every page into one document, expands the Q&A answers, uses the light theme and prints it with headless Chrome. It needs Python 3 and Google Chrome or Chromium on your `PATH`, and no other dependencies. The output goes to `dist/`, which is git-ignored, so rerun the script after changing the content. The script is not part of the published site.

## Publishing to GitHub Pages

A workflow in [`.github/workflows/pages.yml`](.github/workflows/pages.yml) deploys the site on every push to `main` (or on demand from the Actions tab). One-time setup: in the repository go to **Settings → Pages** and set **Source** to **GitHub Actions**. The site will then be served at `https://<user>.github.io/system-design-patterns/`.

## Structure

```
index.html              landing page: overview, pattern cards, how to use it in an interview
patterns/               one HTML page per pattern (same ten sections on every page)
assets/style.css        design tokens (light/dark), layout and components
assets/main.js          sidebar, "on this page" table of contents, theme toggle, prev/next links
scripts/build-pdf.py    builds the single-file PDF export into dist/
.github/workflows/      GitHub Pages deploy workflow
```

Every pattern page has the same sections: TL;DR, the problem, when it comes up, solutions in escalation order, trade-offs and pitfalls, technology options, when not to use it, an interview script, deep-dive Q&A, and related patterns.

## Source and caveats

The structure and the eight patterns follow a video walkthrough of common system design interview patterns from [Hello Interview](https://www.hellointerview.com). This site is an independent write-up and is not affiliated with or endorsed by them. Where the video only mentions a topic briefly, the pages expand on it from general engineering knowledge.

The text and diagrams were drafted with the help of an AI assistant (Claude). Figures such as throughput numbers, service limits and timeouts are approximate and hedged in the text. Check them against current documentation before relying on them.
