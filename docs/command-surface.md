# V1 Command Surface

Claude Code exposes every user-invocable plugin skill as a namespaced slash
command. Claude Chat and Cowork display the same installed skills as short
commands without the plugin prefix. For v1, each Endgame skill is its own 1:1
command entrypoint:

| Claude Code | Chat and Cowork | Argument hint |
|-------------|-----------------|---------------|
| `/endgame:account-brief` | `/account-brief` | `[account name or domain]` |
| `/endgame:meeting-prep` | `/meeting-prep` | `[meeting, account, or time]` |
| `/endgame:meeting-follow-up` | `/meeting-follow-up` | `[meeting, account, or date]` |
| `/endgame:pipeline-review` | `/pipeline-review` | `[owner, team, segment, or period]` |
| `/endgame:call-review` | `/call-review` | `[call, meeting, or account]` |
| `/endgame:stakeholder-map` | `/stakeholder-map` | `[account or opportunity]` |
| `/endgame:customer-evidence` | `/customer-evidence` | `[topic and optional timeframe]` |

The skill descriptions drive automatic discovery. The `argument-hint`
frontmatter describes the optional input for direct invocation.

## Why There Is No `commands/` Directory

Claude Code has merged custom commands into skills. A flat Markdown file under
`commands/` remains supported for compatibility, but it is another skill
definition. If a command and a skill share a name, the skill takes precedence.
Adding seven same-name wrappers would therefore create shadowed files rather
than delegation.

The v1 package uses the current `skills/<name>/SKILL.md` format as both the
model-invocable workflow and user-invocable command.

References:

- [Create plugins](https://code.claude.com/docs/en/plugins)
- [Extend Claude with skills](https://code.claude.com/docs/en/slash-commands)
