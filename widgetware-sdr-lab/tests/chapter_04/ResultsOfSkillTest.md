# Account Research Skill — Test Results

Ran the `account-research` Skill on **ABB**, **Siemens**, and **Rockwell
Automation**. All three profiles validated against
[`schema.json`](../../.claude/skills/account-research/schema.json) and were
saved to `outputs/`:

| Company | Confidence | Key signals found |
|---|---|---|
| [abb-profile.json](../../outputs/abb-profile.json) | 0.7 | New CEO (Aug 2024), "Automation Extended" (AI into legacy control systems), Vale AI/mining partnership, ~$75M India investment |
| [siemens-profile.json](../../outputs/siemens-profile.json) | 0.75 | CES 2026 keynote, NVIDIA "Industrial AI" partnership, Eigen AI engineering agent, humanoid robots in production |
| [rockwell-automation-profile.json](../../outputs/rockwell-automation-profile.json) | 0.65 | "Automation to autonomy" strategic pivot (Nov 2025 keynote), AI-driven refrigeration optimization (-17% energy), growing OT-cybersecurity focus |

## Notes from actually running the procedure

- ABB's direct homepage fetch timed out after a redirect, so that profile
  leans more heavily on search-indexed press releases — reflected in
  `evidence` and the slightly lower confidence relative to Siemens.
- Rockwell's root domain (`rockwellautomation.com`) is only a
  region-selector page with no content — I followed the redirect logic the
  Skill's procedure implies (use the site as primary source) to
  `/en-us.html` instead of stopping there.
- All three correctly declined to state specific employee/revenue figures
  since none were confirmed via a fetched source this session, per the
  Skill's "never invent to fill the schema" rule — `size_estimate` says so
  explicitly rather than guessing a number that "sounds right" for a
  company this size.

## Standing flag

None of these three fit `config/icp.yaml` (they're 20,000–100,000+
employee industrial conglomerates in Europe/US, not 50–2,000 employee
B2B SaaS/fintech/ecommerce/healthtech companies) — that mismatch between
the new `data/accounts.csv` and the existing ICP/config files will still
break `tests/chapter_03/` once run, independent of this Skill test.

## Sources

- [ABB: Do More With Digital campaign](https://new.abb.com/news/detail/117381/abb-launches-do-more-with-digital-campaign-to-accelerate-digitalization-across-process-industries)
- [ABB: Automation Extended](https://new.abb.com/news/detail/133058/abb-introduces-automation-extended-enabling-industrial-innovation-with-continuity)
- [Vale and ABB partnership](https://www.automation.com/article/vale-abb-sign-partnership-accelerate-digital-transformation-iron-ore-operations-brazil)
- [How ABB is reshaping an engineering icon (IMD)](https://www.imd.org/ibyimd/podcasts/ceo-dialogue-podcast-series/how-abb-is-reshaping-an-engineering-icon-for-the-future/)
- [ABB Robotics at MACH 2026](https://www.automation.com/article/abb-robotics-next-generation-automation-digital-solutions-mach-2026)
- [Siemens unveils industrial tech for the AI era (CES 2026)](https://press.siemens.com/global/en/pressrelease/siemens-unveils-industrial-tech-ai-era-ces-2026-keynote)
- [Siemens Realize LIVE 2026: Intelligence Center X](https://techhq.com/news/siemens-realize-live-2026-intelligence-center-x-digital-twins/)
- [Rockwell Automation + Actemium AI refrigeration optimization](https://www.americanrecruiters.com/2026/05/14/rockwell-automation-actemium-deploy-ai-to-cut-refrigeration-energy-use-by-17-in-frozen-food-production/)
- [Rockwell Automation charts an autonomous, human-centered industrial future](https://www.oemmagazine.org/engineering/automation/article/22957273/rockwell-automation-charts-an-autonomous-humancentered-industrial-future)
