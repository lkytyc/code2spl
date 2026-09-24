## Free Summary Workflow

The environment contains a generated free-form source summary at
`/tmp/spl_tools/free_summary_context.txt` and a helper:

```bash
python /tmp/spl_tools/free_summary_search.py "issue keywords"
```

Step 1: Read the issue and extract the required behavior.

Step 2: Use the free-summary search only to recall likely files or functions
whose source should be inspected.

Step 3: Inspect the real source code before deciding the edit owner.

Step 4: Generate the smallest source-code patch and verify it with a focused
reproduction or test.

The summary is not source code and must not be copied into the patch.
