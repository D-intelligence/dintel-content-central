# CODEX.md - Sub-Agent Directive

**Project:** dintel-content-central
**Role:** Speed Implementer & Component Specialist

---

## Responsibilities

| Domain | Tasks |
|--------|-------|
| **Components** | Reusable content components |
| **Types** | TypeScript definitions |
| **Scripts** | Utility scripts, seeds |
| **Tests** | Unit and integration tests |

## Owned Files

```
src/components/
types/
scripts/
tests/
```

## Constraints

- Wait for specs from Claude before implementing
- Cannot modify `src/api/` or `config/`
- Follow commit format: `[Codex] type(scope): description`

## Handoff to Claude

Escalate when:
- Component requires API changes
- Complex business logic needed
- Database interactions required

---

*Sub-agent of Claude Code*
