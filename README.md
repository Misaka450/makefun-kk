# Sum up 23 November's world news in one image

make.fun bounty: [news-image-20261123](https://make.fun/bounty/news-image-20261123)
— $100 total, 50 places (1st $20). Round 1 closes 2026-11-23 20:00 CST,
final deadline 2026-11-25 08:00 CST.

## What it is

A 1024×1024 infographic: a dark-navy header naming the day
**MONDAY 23 NOVEMBER 2026**, then six panels, one per story:

1. **CLIMATE — Antalya, Turkey:** COP31 ends without a deal — EU and
   about 130 parties reject a text omitting fossil fuels.
2. **CONFLICT — Dymer, Ukraine:** Russian strike kills at least 10 —
   a 7-year-old boy is pulled alive from the rubble in Dymer, north
   of Kyiv.
3. **MARKETS — Tokyo / New York:** AI sell-off rattles markets —
   Nikkei falls 5.06%; S&P 500 falls 3.7%.
4. **CONFLICT — Khartoum, Sudan:** Drone strikes kill five children —
   strikes hit homes and a UN building in Khartoum.
5. **JUSTICE — Sinaloa, Mexico:** ‘El Chapo Isidro’ captured — FBI
   most-wanted fugitive seized; 11 killed in violence during the capture.
6. **SPACE — Mercury:** BepiColombo reaches Mercury — probe enters
   Mercury orbit after an eight-year journey.

Every headline and number is as reported on 23 November 2026; nothing
else was invented.

## Files

- `main.py` — the entrypoint (Python 3.13, stdlib only). Copies
  `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`, default `/output`,
  byte for byte, after checking the PNG signature.
- `entry.png` — the image itself, 1024×1024, ~115 KB (limit 1 MiB).
- `build_image.py` — the generator that drew `entry.png` with Pillow
  (build-time only; the grader never runs it).
- `LICENSE` — MIT.
- `.makefun/owner.json` — claim file naming the payout wallet
  `937mXGg2kV6EcrtpB8uTdJTwYLwrv9c6Q6gZTWdLyQ4D`.

## Run and verify locally

```sh
# rebuild the image (optional; entry.png is already in the repo)
python3 build_image.py

# run the entrypoint twice, into two different output dirs
mkdir -p out1 out2
MAKEFUN_OUTPUT_DIR=out1 python3 main.py
MAKEFUN_OUTPUT_DIR=out2 python3 main.py

# byte-identical check
cmp out1/entry.png out2/entry.png && echo IDENTICAL
python3 -c "from PIL import Image; im = Image.open('out1/entry.png'); print(im.size, im.format)"
```

Expected: `IDENTICAL`, `1024×1024 PNG`, file well under 1 MiB.

## To submit (not done here)

Create a public GitHub repo **after the competition opened**
(2026-11-23 00:00 UTC), push these files, then follow the kit's
`RULES.txt`: bundle the agent session transcripts that built this
entry, run `node cli/makefun.mjs check`, and submit with the Solana
wallet above signing the entry. No private key or seed phrase is
needed by, or stored in, this repo.
