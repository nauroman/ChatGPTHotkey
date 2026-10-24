# Fact Checker

After installing `requirements.txt`, activate the prepared Python environment,
run `run_factchecking.bat`, focus the intended editable field and press
`Ctrl+F14`. The existing capture behavior selects all text in that field and
replaces it with the completed report. Use a separate scratch document first.
Restart the Fact Checker process after updating its shortcut. Ctrl+F16 is no
longer bound by default. Ctrl+F13 and Ctrl+Shift+F13 keep their writing modes.

The launcher uses the public API model `gpt-6-luna` with `medium` reasoning.
Change `MODEL`, `REASONING_EFFORT` or `HOTKEY` in the launcher when needed.
Edit `FACTCHECK_PROMPT` in `factchecking.py` to customize the checking policy.
The existing `OPENAI_API_KEY` is used; do not put keys in the launcher.

Fact Checker uses one Responses API request with live web search, compact
output and up to four web-tool actions (searches or page lookups). Confirmed,
false and misleading factual verdicts require source URLs returned by that request's search tool. Opinions,
predictions and missing context are distinguished from facts. Unresolved facts
remain unverified. Search results still require human judgment; URL provenance
does not prove that every interpretation is correct.

The prompt asks for a report in the input language and treats instructions
embedded in input text as data, rather than instructions to execute. Incomplete,
unsupported or failed responses leave the original text intact. The request is not retried automatically, and
there is no automatic model fallback. Maximum passage length is 24,000
characters; split longer text into sections. The network read timeout is 45
seconds. Source text and keys are not written to application logs.

The Responses endpoint is called through the `httpx` dependency listed in
`requirements.txt`, so the shared OpenAI SDK does not need upgrading. The text
editor entry point and its hotkeys are unchanged.

Web search charges are separate from model token charges. Review
[current API pricing](https://developers.openai.com/api/docs/pricing). A cheaper
model does not guarantee a lower total cost than the former search-free mode.
Runtime depends on the passage, available evidence, search activity and network;
no fixed response time or universal speed improvement is guaranteed.

Tests: `python -m unittest discover -s tests -p test_factchecking.py -v`

Official references: [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna),
[web search](https://developers.openai.com/api/docs/guides/tools-web-search).
