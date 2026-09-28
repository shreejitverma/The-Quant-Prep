#!/bin/sh
# Scan the commits a change introduces (<base>..HEAD, default origin/main) for secrets with gitleaks.
# Rules come from .gitleaks.toml; for a full-tree audit run `gitleaks dir . --no-banner --redact` instead.
set -eu
base="${1:-origin/main}"
if ! command -v gitleaks >/dev/null 2>&1; then
  echo "scan-secrets: gitleaks is not installed; install it with 'brew install gitleaks' or from https://github.com/gitleaks/gitleaks/releases" >&2
  exit 1
fi
git rev-parse --verify --quiet "$base^{commit}" >/dev/null || {
  echo "scan-secrets: base '$base' is not a known commit; fetch it first" >&2
  exit 1
}
exec gitleaks git --no-banner --redact --log-opts="$base..HEAD" .
