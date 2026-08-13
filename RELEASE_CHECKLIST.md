# Release checklist

Use this checklist before publishing Hysplex publicly.

## Before committing source

- [ ] Confirm `hysplex_apps.json` is not committed. It can contain personal local paths.
- [ ] Confirm `dist/`, `build/`, and `release/` are not committed.
- [ ] Confirm no API keys, account names, or private paths are present in committed files.
- [ ] Run the app from source once after changes.

## Before uploading a GitHub Release zip

- [ ] Build a fresh executable with `pyinstaller Hysplex.spec`.
- [ ] Package only public-safe files.
- [ ] Do **not** include your personal `hysplex_apps.json`.
- [ ] If including a config file, use `hysplex_apps.example.json` or a clean default config.
- [ ] Include `LICENSE.txt`.
- [ ] Include `README.md`.
- [ ] Generate a SHA256 checksum for the final zip.

## Suggested release contents

```text
Hysplex-v1.0.0-win64/
  H Y S P L E X.exe
  README.md
  LICENSE.txt
  hysplex_apps.example.json
```

## Suggested GitHub workflow

1. Commit the source repository.
2. Push to GitHub.
3. Create a tag, for example `v1.0.0`.
4. Create a GitHub Release from the tag.
5. Upload the packaged zip and checksum as release assets.
