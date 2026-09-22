# Security

## Secret custody

Store the administration credential only as the GitHub Actions secret:

```text
REPO_ADMIN_TOKEN
```

The token value must never appear in configuration, Issue bodies, logs or
commits.

## Narrow mutation surface

The beta supports only:

```text
/repo-admin create <name> <private|public>
```

Existing repositories are never renamed, deleted, archived, transferred or
silently switched between public/private.

## Personal-owner verification

GitHub's personal repository creation endpoint creates under the authenticated
user. Therefore, when `owner_type=user`, the product first reads
`GET /user` and requires the returned login to match the configured owner.

## Authorization

Use `allowed_author_associations` to define which GitHub Issue author
associations may request a repository. Keep the allowlist as small as possible.
