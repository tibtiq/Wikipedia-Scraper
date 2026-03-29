default: sync format lint type

# sync environment with project dependencies
sync:
    uv sync

# run formatter
format:
    uvx ruff format .

# run linter
lint:
    uvx ruff check .

# run type checker
type:
    uv run pyright .

# run scraper
run: sync
    uv run src/wikipedia_scraper.py
