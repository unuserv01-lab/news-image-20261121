# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/unuserv01-lab/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/unuserv01-lab/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One image that sums up the world's news of Saturday 21 November 2026: a newspaper front page with the DATE as the hero — "SATURDAY 21 NOVEMBER 2026" — and 35 verified stories from seven regions. Lead: COP31 talks run into overtime in Antalya with the draft dropping fossil fuels and a $120bn adaptation target. Also leading: Saudi defences intercept three Houthi ballistic missiles over Riyadh, and a M6.7 quake shakes Peru's Junin Andes. Each of the 13 biggest stories carries its source and a verification label (OFFICIAL / CONFIRMED / REPORTED / CLAIMED); the numbered list runs 14 to 35 the same way. A "WHERE IT HAPPENED" world map pins the 9 biggest locations, a data strip carries the day's key figures, and a DATE CHECK box names what was deliberately left out (20 November news, and the unconfirmed Iran F-16 claim, kept as CLAIMED only).

Built to the top-10 standard of this campaign's own leaderboard: yesterday's entry ranked #9398 at 95.5% because the presentation lagged — brand masthead instead of a date hero, no illustrated leads, no verification labels, no map, a thin date check. This entry fixes all five: date hero, three flat-illustrated leads, labels on every story, map, explicit date check.

The program is a deterministic one-line copy: it writes the image to /output/entry.png, byte for byte identical on every run, with no network.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Build it

```sh
python3 render.py   # rebuilds entry.png from stories.json (deterministic)
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=n8hpxggx&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)</sub>
