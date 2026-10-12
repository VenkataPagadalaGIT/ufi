## What this changes

## Why

## Checks

- [ ] `python -m pytest -q` passes
- [ ] `ruff check` and `mypy src/ufi` pass
- [ ] `examples/nanp/build_example.py` still prints the same manifest digest, or the CHANGELOG says why it changed
- [ ] Any number that reaches a README or docstring comes from a script
- [ ] Synthetic data is flagged `synthetic=True`
