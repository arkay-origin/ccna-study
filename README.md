# CCNA Study

A self-contained study course for the Cisco CCNA 200-301 **v2.0** exam (the only version available from February 3, 2027).

**Open it:** https://arkay-origin.github.io/ccna-study/

## What's inside

- **Lessons**: 25 beginner-friendly v2.0 lessons following a learning path (Foundations → Addressing and Clients → Wireless → Switching → IP Routing → Services and Security → AI and Operations). Each lesson has diagrams, command examples, exam tips, "Check yourself" questions, and lists the exam topics it covers.
- **v1.1 extras**: 5 optional lessons for topics v1.1 has but v2.0 dropped (architectures/WAN/cloud, security concepts, QoS/NTP/TFTP, wireless architectures and WLC, REST/JSON/SD architectures), clearly marked.
- **Subnetting drill**: endless generated practice (subnet facts, sizing, masks, binary) with worked block-size answers.
- **Study guide**: 462 questions with tap-to-reveal answers and a short "Why".
- **Flash cards**: mark each card "Got it" or "Review again", with spaced repetition.
- **Practice test**: shuffled multiple-choice tests by section, instant or exam-style feedback, and "retry missed".
- **Mock exam**: 50 scenario questions weighted like the v2.0 blueprint, 60 minutes, scored by exam domain.
- **Weak areas and test-day summary**, **bookmarks**, **cheat sheet** (23 topics), **progress backup**.
- **Works offline**: on your phone, "Add to Home screen".

Progress is saved in your own browser (localStorage) and isn't shared.

## Updating

Content lives in `src/` (one Python file per group of sections, plus `cheat.py` and `exam.py`). Run `python3 src/build.py` to rebuild `index.html`, then commit and push. GitHub Pages redeploys automatically.

Written from Cisco's published CCNA 200-301 v2.0 exam topics. Check Cisco's current topic list before you book.
