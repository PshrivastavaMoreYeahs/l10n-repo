# L10n Practical Test Notes

## Merge Conflict Resolution

I merged `feature/de-locale` into `feature/prashant-locale-qa` and resolved the conflict in `locales/en.json` from the command line.

In the navigation section, I kept both keys:

- `nav.support`
- `nav.help`

I kept both because they represent different possible entry points. Dropping either one could remove product functionality. Whether the product should expose both long term is a product/design decision I would confirm with the team.

For `battery.status`, I kept the current `main` wording:

```json
"battery.status": "Battery: {percent}%"
```

I deliberately discarded the German branch's English wording:

```json
"battery.status": "Battery level: {percent}%"
```

My reasoning was that the German branch's main purpose was adding German localization, while `main` had the more current English source copy.

For `footer.copyright`, I kept the current `main` wording:

```json
"footer.copyright": "© {year} Lenovo Group Limited. All rights reserved."
```

I deliberately discarded:

```json
"footer.copyright": "Copyright {year} Lenovo. All rights reserved."
```

I chose the `main` version because it is more legally specific and includes the full company name.

After resolving the conflict, I confirmed `locales/en.json` was valid JSON and reran the locale validation. The validator correctly picked up issues in the newly merged `de.json`.

## Unfinished Work

The validator and CI pipeline are complete, but the locale content itself is intentionally still failing validation. The remaining work would be to fix the translation files:

- `fr.json`
- `ja.json`
- `de.json`

Examples include missing keys, empty translations, and placeholder mismatches such as `{pct}` or `{prozent}` where English expects `{percent}`.

I did not fix the translation content because the exercise asks the validator to detect these issues, and the broken locale files are part of the test data.

## Verification

I verified the Python validator locally:

```bash
python3 tools/check_locales.py
python3 tools/check_locales.py --locales-dir locales
```

I verified the Bash wrapper locally:

```bash
bash tools/run_checks.sh
cd tools && bash run_checks.sh
```

I also ran the Jenkins pipeline locally in Docker. Jenkins checked out `feature/prashant-locale-qa`, ran `tools/run_checks.sh locales`, archived `reports/locale-report.txt`, and finished as `UNSTABLE` because locale issues were found.

I chose `UNSTABLE` for validation failures because the CI pipeline itself ran correctly and produced a report; the issue was content quality, not infrastructure failure.

## AI Tools Used

I used ChatGPT/Codex as a coding assistant while working through the exercise.

I used it to:

- Interpret the practical test requirements.
- Draft the initial Python validator structure.
- Draft the Bash CI wrapper.
- Draft the Jenkins declarative pipeline.
- Talk through the Git merge conflict resolution.

I reviewed the generated output before committing. One correction I made during the process was around shell usage: on macOS, `python` was not available but `python3` was, so the Bash wrapper detects `python3` first and falls back to `python`. I also verified that the wrapper works from both the repo root and the `tools` directory.

For the merge conflict, I did not blindly accept either side. I reviewed the conflict markers manually, kept both navigation keys, and deliberately chose the current `main` versions for the English battery and copyright strings.
