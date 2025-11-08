# Minimal stubs so run_full_benchmark.py's import succeeds.
# Not actually used when --prompt is provided.
PROMPTS = {
    "dense": "\\nProduce a complete answer to <YOUR TOPIC HERE> in exactly two dense paragraphs without blank lines, continuous sentences, no headings, no extra whitespace, no code fences, no prefix text, no trailing notes. Keep content comprehensive and self-contained.",
    "medium": "Explain <YOUR TOPIC HERE> thoroughly.\n- Keep paragraphs tight but readable.\n- Include 3 bullet examples.\n- End with a 2-line summary.",
    "sparse": "# Sparse Prompt (human-friendly spacing)\nExplain the topic below clearly.\n\nTopic: <YOUR TOPIC HERE>\n\nGuidelines:\n- Use headings\n- Use short paragraphs\n\nProvide examples."
}
