---
sidebar_position: 2
---

# Creating Skills

## Structure

Every Skill follows this structure:

```
.claude/skills/<skill-name>/
├── SKILL.md           # Required: trigger conditions + instructions
├── REFERENCE.md       # Optional: detailed reference docs
├── scripts/           # Optional: executable scripts
│   ├── deploy.sh
│   └── verify.sh
└── templates/         # Optional: code templates
    └── main.py.tmpl
```

## SKILL.md Template

Keep under 100 tokens. Define when and how the skill activates.

```markdown
# Skill Name

## Trigger
When the user asks to [specific action]

## Instructions
1. Run `scripts/deploy.sh <args>`
2. Verify with `scripts/verify.sh`
3. Report results

## Inputs
- `NAMESPACE`: Kubernetes namespace (default: "default")
- `NAME`: Resource name (required)

## Outputs
- Deployment status
- Verification results
```

## Guidelines

1. **SKILL.md stays small** - Under 100 tokens. Only trigger conditions and steps.
2. **Scripts do the work** - Put logic in scripts, not in SKILL.md.
3. **Scripts return minimal output** - Under 50 tokens of output.
4. **Cross-agent compatible** - Must work on both Claude Code and Goose.
5. **Include verification** - Every skill should have a verify script.
6. **Idempotent** - Running a skill twice should not break anything.
