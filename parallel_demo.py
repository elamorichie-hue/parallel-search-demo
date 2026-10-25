"""
Parallel Search demo — Telegram scam research briefing.
Built by Elijah / ElamoLabs as a demo for Parallel Web Systems' Deployed Engineer track.

What it does:
  Runs 3 searches through Parallel's Search API and writes a short,
  cited briefing (briefing.md) a Telegram community admin could act on.

Setup (free, no card):
  1. Sign up at https://parallel.ai and create a free API key.
  2. pip install requests
  3. Run it WITHOUT hardcoding the key:
       PARALLEL_API_KEY=your_key_here python parallel_demo.py
  Never paste your key into the code or into a public repo.

If the API answers with an error, the script prints the status + body
so the problem can be fixed in one pass.
"""

import json
import os
import sys

import requests

API_URL = "https://api.parallel.ai/v1/search"

SEARCHES = [
    {
        "objective": "How fake Telegram support accounts scam crypto users, and the warning signs",
        "search_queries": [
            "fake Telegram support account crypto scam",
            "Telegram fake support DM wallet drain scam warning signs",
        ],
    },
    {
        "objective": "How flash USDT adverts and fake USDT flashing services work",
        "search_queries": [
            "flash USDT fake Tether flashing service scam",
            "fake USDT lookalike contract balance scam",
        ],
    },
    {
        "objective": "How Telegram community admins detect and prevent support-impersonation scams",
        "search_queries": [
            "Telegram group admin prevent impersonation scam",
            "community admin anti-scam verification Telegram crypto",
        ],
    },
]


def search(api_key, objective, queries):
    resp = requests.post(
        API_URL,
        headers={"x-api-key": api_key, "Content-Type": "application/json"},
        json={
            "objective": objective,
            "search_queries": queries,
            # v1 note: max_results is NOT a top-level field — it lives
            # inside advanced_settings (top-level sends a 422).
            "advanced_settings": {"max_results": 5},
        },
        timeout=60,
    )
    if resp.status_code != 200:
        print(f"[!] Search failed ({resp.status_code}): {resp.text[:500]}")
        return []
    data = resp.json()
    results = data.get("results", []) or []
    cleaned = []
    for r in results:
        excerpts = r.get("excerpts") or r.get("excerpt") or r.get("snippet") or ""
        if isinstance(excerpts, list):
            excerpts = " ".join(str(e) for e in excerpts)
        cleaned.append(
            {
                "title": r.get("title", "Untitled"),
                "url": r.get("url", ""),
                "excerpt": str(excerpts)[:600],
            }
        )
    return cleaned


def main():
    api_key = os.environ.get("PARALLEL_API_KEY", "").strip()
    if not api_key:
        print("Set your key first: PARALLEL_API_KEY=your_key_here python parallel_demo.py")
        sys.exit(1)

    lines = []
    lines.append("# Telegram scam research briefing (Parallel Search demo)")
    lines.append("")
    lines.append("Topic: fake Telegram support accounts + flash-USDT adverts,")
    lines.append("and what a community admin can do about them.")
    lines.append("")

    for job in SEARCHES:
        print(f"Searching: {job['objective']}")
        results = search(api_key, job["objective"], job["search_queries"])
        lines.append(f"## {job['objective']}")
        lines.append("")
        if not results:
            lines.append("- (no results returned for this search)")
        for r in results:
            lines.append(f"- **{r['title']}** — {r['url']}")
            if r["excerpt"]:
                lines.append(f"  > {r['excerpt']}")
        lines.append("")

    lines.append("## Admin takeaways (fill in after reading the sources)")
    lines.append("")
    lines.append("1. Trick being used: ...")
    lines.append("2. Warning sign: ...")
    lines.append("3. Defense: ...")
    lines.append("")
    lines.append("## Gap found (what the first answer missed)")
    lines.append("")
    lines.append("- ... (open every cited link above and note one miss here)")

    with open("briefing.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("\nDone. Briefing written to briefing.md — open every cited link,")
    print("fill in the takeaways + the gap, then publish it as a README.")


if __name__ == "__main__":
    main()
