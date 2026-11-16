"""Refreshes data/stats.json from GitHub, LeetCode and the four Sj practice repos.

Every source is optional: if a call fails, the last known values stay in place,
so the cards never break. Run by .github/workflows/refresh.yml once a day.
"""
import datetime as dt
import json
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "data", "stats.json")
LOGIN = "Sayandip-Jana-1018"
LC_USER = "sayandip_jana"
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
UA = "Mozilla/5.0 (X11; Linux x86_64) sj-profile-refresh"


def http(url, data=None, headers=None, timeout=25):
    h = {"User-Agent": UA, "Accept": "application/json"}
    h.update(headers or {})
    body = json.dumps(data).encode() if data is not None else None
    if body is not None:
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def gh_rest(path):
    h = {"Accept": "application/vnd.github+json"}
    if TOKEN:
        h["Authorization"] = f"Bearer {TOKEN}"
    return http(f"https://api.github.com{path}", headers=h)


def gh_graphql(query, variables):
    if not TOKEN:
        raise RuntimeError("no token")
    res = http("https://api.github.com/graphql", {"query": query, "variables": variables},
               {"Authorization": f"Bearer {TOKEN}"})
    if res.get("errors"):
        raise RuntimeError(res["errors"])
    return res["data"]


LEVEL = {"NONE": "0", "FIRST_QUARTILE": "1", "SECOND_QUARTILE": "2", "THIRD_QUARTILE": "3", "FOURTH_QUARTILE": "4"}


def github(stats):
    q = """query($login:String!){ user(login:$login){
      followers{totalCount}
      contributionsCollection{ contributionCalendar{ totalContributions
        weeks{ contributionDays{ date contributionCount contributionLevel } } } }
      repositories(ownerAffiliations:OWNER, privacy:PUBLIC, first:100, isFork:false){
        totalCount nodes{ stargazerCount primaryLanguage{name} } } } }"""
    u = gh_graphql(q, {"login": LOGIN})["user"]
    cal = u["contributionsCollection"]["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    days.sort(key=lambda d: d["date"])
    days = days[-366:]
    counts = [d["contributionCount"] for d in days]
    # streaks
    cur = 0
    i = len(counts) - 1
    if i >= 0 and counts[i] == 0:      # today not yet active doesn't break the streak
        i -= 1
    while i >= 0 and counts[i] > 0:
        cur += 1
        i -= 1
    best = run = 0
    for n in counts:
        run = run + 1 if n > 0 else 0
        best = max(best, run)
    langs = {}
    for n in u["repositories"]["nodes"]:
        if n["primaryLanguage"]:
            langs[n["primaryLanguage"]["name"]] = langs.get(n["primaryLanguage"]["name"], 0) + 1
    top = dict(sorted(langs.items(), key=lambda kv: -kv[1])[:5])
    g = stats["github"]
    g.update({
        "contrib_year": cal["totalContributions"],
        "current_streak": cur,
        "longest_streak": best,
        "active_days": sum(1 for n in counts if n > 0),
        "max_day": max(counts) if counts else g.get("max_day", 0),
        "public_repos": u["repositories"]["totalCount"],
        "stars": sum(n["stargazerCount"] for n in u["repositories"]["nodes"]),
        "followers": u["followers"]["totalCount"],
        "languages": top or g["languages"],
        "levels": "".join(LEVEL.get(d["contributionLevel"], "0") for d in days),
        "levels_start": days[0]["date"],
    })


def leetcode(stats):
    q = """query($u:String!){ matchedUser(username:$u){
      profile{ ranking }
      submitStatsGlobal{ acSubmissionNum{ difficulty count } }
      userCalendar{ streak totalActiveDays } } }"""
    res = http("https://leetcode.com/graphql/", {"query": q, "variables": {"u": LC_USER}},
               {"Referer": f"https://leetcode.com/u/{LC_USER}/", "Origin": "https://leetcode.com"})
    m = res["data"]["matchedUser"]
    ac = {x["difficulty"]: x["count"] for x in m["submitStatsGlobal"]["acSubmissionNum"]}
    lc = stats["leetcode"]
    lc.update({"solved": ac.get("All", lc["solved"]), "easy": ac.get("Easy", lc["easy"]),
               "medium": ac.get("Medium", lc["medium"]), "hard": ac.get("Hard", lc["hard"]),
               "ranking": m["profile"]["ranking"] or lc["ranking"]})
    if m.get("userCalendar"):
        lc["streak"] = m["userCalendar"]["streak"]
        lc["active_days"] = m["userCalendar"]["totalActiveDays"]


def practice_repos(stats):
    rp = stats["repos"]
    for repo in ["LeetCodeSj", "CodeforcesSj", "AtCoderSj", "CodeChefSj"]:
        items = gh_rest(f"/repos/{LOGIN}/{repo}/contents/")
        dirs = [x for x in items if x["type"] == "dir" and not x["name"].startswith(".")]
        rp[repo] = len(dirs)


def main():
    stats = json.load(open(PATH))
    for name, fn in [("github", github), ("leetcode", leetcode), ("repos", practice_repos)]:
        try:
            fn(stats)
            print(f"[ok] {name}")
        except Exception as e:  # keep cached values
            print(f"[skip] {name}: {e}", file=sys.stderr)
    stats["updated"] = dt.date.today().isoformat()
    with open(PATH, "w") as f:
        json.dump(stats, f, indent=1, ensure_ascii=False)
        f.write("\n")


if __name__ == "__main__":
    main()
