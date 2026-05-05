#!/bin/bash
# Test harness for GTM Agent Skills
# Usage: bash tests/run.sh [skill-name]
# If skill-name is omitted, runs all tests.

set -euo pipefail

SKILLS_DIR="$(cd "$(dirname "$0")/.." && pwd)"
FAILURES=0
TOTAL=0

check_skill() {
  local skill_dir="$1"
  local skill_name="$(basename "$skill_dir")"
  local skill_md="$skill_dir/SKILL.md"

  TOTAL=$((TOTAL + 1))

  # 1. SKILL.md must exist
  if [ ! -f "$skill_md" ]; then
    echo "FAIL: $skill_name — no SKILL.md found"
    FAILURES=$((FAILURES + 1))
    return
  fi

  # 2. SKILL.md must be valid YAML frontmatter + markdown
  if ! head -1 "$skill_md" | grep -q '^---$'; then
    echo "FAIL: $skill_name — SKILL.md missing YAML frontmatter opener"
    FAILURES=$((FAILURES + 1))
    return
  fi

  # 3. Frontmatter must contain required fields
  local body="$(sed -n '/^---$/,/^---$/p' "$skill_md")"
  for field in name description version author license; do
    if ! echo "$body" | grep -q "^${field}:"; then
      echo "FAIL: $skill_name — missing frontmatter field '$field'"
      FAILURES=$((FAILURES + 1))
      return
    fi
  done

  # 4. Frontmatter must have metadata.hermes with tags and related_skills
  if ! echo "$body" | grep -q "tags:"; then
    echo "FAIL: $skill_name — missing metadata.hermes.tags"
    FAILURES=$((FAILURES + 1))
    return
  fi

  # 5. SKILL.md must have required body sections
  for section in "When to Use" "Quick Reference" "Procedure" "Pitfalls" "Verification"; do
    if ! grep -q "## $section" "$skill_md"; then
      echo "FAIL: $skill_name — missing required section '## $section'"
      FAILURES=$((FAILURES + 1))
      return
    fi
  done

  # 6. SKILL.md must be ≤120 lines
  local lines="$(wc -l < "$skill_md")"
  if [ "$lines" -gt 120 ]; then
    echo "FAIL: $skill_name — SKILL.md is $lines lines (max 120)"
    FAILURES=$((FAILURES + 1))
    return
  fi

  # 7. references/ directory must exist
  if [ ! -d "$skill_dir/references" ]; then
    echo "FAIL: $skill_name — missing references/ directory"
    FAILURES=$((FAILURES + 1))
    return
  fi

  # 8. scripts/ directory must exist
  if [ ! -d "$skill_dir/scripts" ]; then
    echo "FAIL: $skill_name — missing scripts/ directory"
    FAILURES=$((FAILURES + 1))
    return
  fi

  # 9. scripts/push_to_crm.py must exist
  if [ ! -f "$skill_dir/scripts/push_to_crm.py" ]; then
    echo "FAIL: $skill_name — missing scripts/push_to_crm.py"
    FAILURES=$((FAILURES + 1))
    return
  fi

  # 10. push_to_crm.py must compile
  if ! python3 -c "import py_compile; py_compile.compile('$skill_dir/scripts/push_to_crm.py', doraise=True)" 2>/dev/null; then
    echo "FAIL: $skill_name — scripts/push_to_crm.py has syntax error"
    FAILURES=$((FAILURES + 1))
    return
  fi

  echo "PASS: $skill_name ($lines lines, all checks)"
}

# Find and check all SKILL.md files
if [ -n "${1:-}" ]; then
  # Test specific skill
  for dir in intelligence lead-gen outreach conversations pipeline analytics; do
    if [ -d "$SKILLS_DIR/$dir/$1" ]; then
      check_skill "$SKILLS_DIR/$dir/$1"
    fi
  done
else
  # Test all skills
  for dir in intelligence lead-gen outreach conversations pipeline analytics; do
    if [ -d "$SKILLS_DIR/$dir" ]; then
      for skill in "$SKILLS_DIR/$dir"/*/; do
        if [ -f "$skill/SKILL.md" ]; then
          check_skill "$skill"
        fi
      done
    fi
  done
fi

echo ""
echo "========================================="
echo "Results: $((TOTAL - FAILURES)) passed, $FAILURES failed, $TOTAL total"
echo "========================================="

if [ "$FAILURES" -gt 0 ]; then
  exit 1
fi
