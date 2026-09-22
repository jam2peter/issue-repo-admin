# Architecture

Issue Repo Admin is a narrow GitHub-native provisioning primitive.

```text
Issue comment
  -> GitHub Actions
  -> author-association gate
  -> command parser
  -> repository lookup
  -> authenticated-owner verification (personal owner)
  -> create only when absent
  -> visibility consistency check
  -> sanitized Issue result
```

The product intentionally does not expose a generic GitHub administration API.
The control repository owns the workflow, configuration and secret custody.
