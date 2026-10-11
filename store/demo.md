---
title: Project Kickoff Notes
author: Demo Team
---

<!-- This comment is hidden in the rendered preview. -->

# Project Kickoff Notes

> **Goal:** ship the first public release of *Orbit Planner* by **March 31**.

## Milestones

| Phase | Owner | Due | Status |
| --- | --- | --- | :---: |
| Design review | Alice | Jan 15 | ✅ |
| Beta build | Ben | Feb 20 | 🚧 |
| Public launch | Chloe | Mar 31 | ⏳ |

## This week

- [x] Finalize the onboarding flow
- [x] Write the API reference
- [ ] Prepare the release checklist
- [ ] Book the launch webinar

## Quick start

```bash
npm install orbit-planner
orbit init my-project
```

```js
import { Planner } from 'orbit-planner';

const planner = new Planner({ timezone: 'UTC' });
planner.addTask('Write release notes', { due: '2026-03-28' });
console.log(planner.summary());
```

## Notes

1. Keep pull requests **small** and focused.
2. Use `orbit lint` before every commit.
3. Questions? See the [Markdown guide](https://www.markdownguide.org/).

---

*Last updated by the Demo Team.*
