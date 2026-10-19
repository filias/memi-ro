# memi romania

A Romanian memory card game built on [memi-engine](https://github.com/filias/memi-engine).

Live at [ro.memi.games](https://ro.memi.games)

## Categories

- **Geography: counties** — the 41 Romanian counties and Bucharest, as locator maps
- **Geography: cities** — 52 cities and towns, tagged with their historical region
- **Culture: sights** — 64 castles, fortresses, monasteries, ancient sites and natural wonders
- **Culture: food** — 37 Romanian dishes, cheeses, sweets and drinks

## Setup

```bash
uv sync
uv run python -m memi_ro.app
```

## How it works

Each category is a `CategoryProvider` subclass that tells the engine what items to show and where to fetch images. Adding a new category is just a Python class with a list of items and a `get_image` method.

Built with [memi-engine](https://github.com/filias/memi-engine) — anyone can create their own country version.

## License

MIT
