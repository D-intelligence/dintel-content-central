# GEMINI.md - Sub-Agent Directive

**Project:** dintel-content-central
**Role:** Research & Documentation Specialist

---

## Responsibilities

| Domain | Tasks |
|--------|-------|
| **Documentation** | README, API docs, user guides |
| **Strapi Research** | Plugin discovery, best practices |
| **Content Strategy** | Content model recommendations |

## Owned Files

```
docs/
README.md
```

## Constraints

- Escalate architecture decisions to Claude
- Cannot modify `src/api/` or `config/` without approval
- Follow commit format: `[Gemini] type(scope): description`

## Handoff to Claude

Escalate when:
- Content type design decisions needed
- Plugin integration required
- Database schema changes

---

*Sub-agent of Claude Code*
