# memi românia

A Romanian memory card game built on [memi-engine](https://github.com/filias/memi-engine).

Live at [ro.memi.games](https://ro.memi.games) (not deployed yet)

## Categories

- **Geografie: județe** — the 41 Romanian counties and Bucharest, as locator maps

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
