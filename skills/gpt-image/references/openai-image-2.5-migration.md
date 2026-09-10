# GPT Image 2.5: migration and evaluation

Read only for model migration or an authorized comparison, not routine image
requests. Sources checked **2026-09-09**; locally organized official-source notes,
not a new MIT Cookbook snapshot or locally verified image results.

## What changes from Image 2

- OpenAI positions [Flare](https://developers.openai.com/api/docs/models/gpt-image-2.5-flare)
  around speed and [Sunburst](https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst)
  around demanding quality. Both generate and edit; Sunburst is not edit-only.
- If Image 2 already passes your quality bar, evaluate Flare first. Otherwise,
  evaluate Sunburst. Compare the same inputs and explicit settings before
  rewriting prompts; keep the `quality` setting fixed in the first comparison.
  Establish acceptable output quality before optimizing latency.
  [Official migration guidance](https://developers.openai.com/api/docs/guides/image-prompting?model=gpt-image-2.5#migrate-an-existing-workflow)
- `xhigh` and `max` are options, not automatic upgrades. Higher quality may not
  improve a particular task. Test against acceptance criteria and budget.
  [Official quality guidance](https://developers.openai.com/api/docs/guides/image-prompting?model=gpt-image-2.5#model-parameters)

Quoted text, layout constraints and reference invariants are shared techniques
already covered in [craft.md](craft.md), not newly invented 2.5 prompt syntax.
Keep parameter details in [models.md](models.md), not in task prompts.

## Local evaluation checklist

Only run comparisons or extra variants when authorized. Before a trial, write
down what would make the output unusable; use the selected task slice's checks.
Record model, full prompt, attached inputs, dimensions, quality, format, elapsed
time, reported usage, output path and pass/fail reason. Keep failed attempts in
the cost accounting. A documentation example is not our measured result.

## Source boundaries

- [Current official prompting guide](https://developers.openai.com/api/docs/guides/image-prompting?model=gpt-image-2.5):
  illustrated 2.5 workflows. Its complete runnable example still selects Image 2;
  do not copy that model or batch count over the user's confirmed choices.
- [Historical local Cookbook](openai-cookbook.md): captured 2026-04-23, with its
  existing source/license retained. The official notebook checked on 2026-09-09
  [still targets Image 2](https://github.com/openai/openai-cookbook/blob/a78f3f37bd23637aac2b3f1e8b1251cf5bb9e1a7/examples/multimodal/image-gen-models-prompting-guide.ipynb).
  Its recommendations and executable defaults are not current 2.5 settings.
- [Community templates](templates-gpt-image-2.5.md): attributed adaptations with
  author-reported source models, not OpenAI recommendations or verified outputs.
