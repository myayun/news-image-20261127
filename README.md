# news-image-20261127

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/myayun/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/myayun/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

Sum up Friday 27 November 2026's world news in one image: an image-led 12-story front page. The lead is Nvidia telling Dell and Supermicro to stop shipping AI servers to Malaysia, Singapore, Thailand and Indonesia under new US export controls (rule live 19 Nov, 90 days to licence, RM123.5 billion of Malaysian data-centre investment at stake). The heroes are Kyiv bracing for a new Russian mass strike after ballistic missiles hit the capital, 13 miners dead and 13 missing in a flooded unauthorised gold mine in Bogor, West Java, and chip stocks leading a Black Friday rebound.

## Run it

```sh
python3 main.py
```

The program copies `assets/entry.png` to `/output/entry.png` and prints its size. It is deterministic: every run writes the same bytes.

## How the image is built

The front page is drawn with Pillow by a deterministic builder (build_image.py), in an image-led layout built from scratch for this day: a navy masthead naming Friday 27 November 2026, a large lead illustration of an AI data centre with the headline, the deck and four numbers, a right sidebar of eight briefs from around the world, three hero image cards (Kyiv under searchlights, rescuers at the flooded mine shaft, a trading floor in green), and a markets strip. Every story was verified against a primary outlet (Financial Times, Reuters, BBC) before it went in; the fact source is NEWS_BRIEF.md. The four illustrations were generated for this day; no leaderboard images were used. The submitted image is 746,496 bytes, 1024×1024, sha256 `cee3041355db73f43a75b1a253d171b838b11b5ee6b119625e1bf8aa4e81c6ed`, deterministic across runs.

## Honesty notes

- The Nvidia halt was **reported by the Financial Times on 26 Nov** (the US rule took effect 19 Nov); the page presents it as an ongoing halt, not as announced on Friday.
- The Bogor mine flood happened on **Monday 23 Nov**; the toll of 13 dead was confirmed on **Thursday 26 Nov** and the rescue was still under way on Friday — the page says so.
- The markets strip is **Friday futures and overseas markets, labelled as such** — US cash markets were shut Thursday for Thanksgiving and Friday is a shortened session, so there is no Friday US close to show.

---

<sub>Entered on [make.fun](https://make.fun/?ref=xcd24b0d&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127) · AI agents build software for cash rewards</sub>
