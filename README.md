# Issue Repo Admin

Create GitHub repositories from a deliberately narrow Issue-comment command.

```text
/repo-admin create my-tool public
/repo-admin create internal-tool private
```

Issue Repo Admin is for teams that want repository provisioning to be explicit,
reviewable and auditable without exposing a general-purpose administration
console.

> Status: `v0.1-beta`

## What it does

- validates the command;
- validates the comment author's GitHub association;
- looks up the repository first;
- creates only when absent;
- returns success when an existing repository already matches;
- refuses to silently mutate visibility;
- verifies the authenticated user before personal-account creation;
- posts a sanitized result back to the Issue.

## What it does not do

It does not delete, rename, transfer, archive, unarchive, mutate existing
visibility, administer secrets, manage collaborators or proxy arbitrary GitHub
API calls.

## Quick start

1. Copy `repo-admin.example.json` to `repo-admin.json`.
2. Set the GitHub Actions secret `REPO_ADMIN_TOKEN`.
3. Copy `templates/repository-admin.yml` to
   `.github/workflows/repository-admin.yml`.
4. Copy `scripts/repo_admin.py` into the control repository.
5. Open an Issue and comment:

```text
/repo-admin create example-service private
```

## Configuration

```json
{
  "owner": "example-owner",
  "owner_type": "user",
  "allowed_author_associations": ["OWNER"],
  "default_description": "Managed by Issue Repo Admin",
  "auto_init": true
}
```

`owner_type` may be `user` or `organization`.

## Security

The administration credential belongs only in GitHub Actions Secrets.
For a personal owner, Issue Repo Admin verifies that the token's authenticated
login matches the configured owner before `POST /user/repos`.

See [Security](docs/SECURITY.md) and [Architecture](docs/ARCHITECTURE.md).

## Development

```bash
python3 -m py_compile scripts/repo_admin.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

## License

MIT
