# Claude Code Quickstart: Gilded Rose Kata
*A 30-minute hands-on introduction to AI pair programming with a coding agent*

## Overview
Claude Code is a powerful terminal-based AI coding assistant with automatic checkpointing, memory management, and code review capabilities. You'll learn these features while refactoring the Gilded Rose Kata.

## Prerequisites
- Node.js 18 or newer
- Claude.ai account (recommended) or Claude Console account  
- Git installed

## Part 1: Setup & Core Features (5 minutes)

### 1.1 Install Claude Code
```bash
npm install -g @anthropic/claude-code
```

### 1.2 Clone and Navigate
```bash
git clone https://github.com/emilybache/GildedRose-Refactoring-Kata.git
cd GildedRose-Refactoring-Kata
```

**Choose a language you're less familiar with:**
```bash
cd python  # or typescript, java, go, etc.
```

### 1.3 Start Claude Code Session
```bash
claude
```

### 1.4 Initialize Project Context
Once in Claude Code:
```
/init
```

This analyzes your project structure, identifies languages, frameworks, and dependencies.

💡 **Key Feature**: `/init` gives Claude deep understanding of your entire project
⚠️ **NOTE**: Depending on which [_approval mode_](https://geminicli.com/docs/get-started/configuration/#command-line-arguments) you've selected, you may need to approve commands (such as `ls`used by the init command) - But: _ingen minns en fegis_!


### 1.5 Check Session Status and Context
```
/stats
```

Shows current model, session and usage info.


## Part 2: Understanding & Memory Management (7 minutes)

### 2.1 Initial Analysis
```
Now that you've analyzed the project, explain what the Gilded Rose kata is about. 
What are the main code quality issues you can see?
```

### 2.2 Add Project Memory
After Claude explains, capture key insights using the `#` shortcut:
```
The Gilded Rose is a refactoring kata with complex business rules for item quality degradation

Main issues: deeply nested conditionals, no abstraction, difficult to add new item types  

Goal: Refactor to make adding "Conjured" items easy
```

When prompted, select which CLAUDE.md file to add to **project-level** `./CLAUDE.md`.

💡 **Key Feature**: `#` at line start adds memories that persist across sessions

### 2.3 Create Documentation
```
Create a business-rules.md file with a clear table showing how each item type changes over time.
Include examples for normal items, Aged Brie, Backstage passes, and Sulfuras.
```

### 2.4 View/Edit Memories
Open your memory files in your editor:
```
/memory
```

You can organize and expand the memories Claude will use in future sessions.

## Part 3: Test-Driven Safety Net (8 minutes)

### 3.1 Check Automatic Checkpointing
Remember: **Every prompt you send creates an automatic checkpoint!** You can always rewind if needed.

### 3.2 Assess Current Testing
```
Check if there are existing tests in this project. If they exist, run them and show me the output.
What test coverage do we currently have?
```

### 3.3 Write Comprehensive Tests
```
Write characterization tests that capture all current behavior:
- Normal items degrading in quality
- Aged Brie increasing in quality  
- Backstage passes with their complex rules
- Sulfuras never changing
- Quality bounds (0-50)
- Sell-by date edge cases

Then run the tests to verify they pass.
```

### 3.4 Capture Test Success as Memory
Now that tests are passing, document this milestone. Type this at the Claude prompt (starting with `#`):
```
Characterization tests complete - all item types covered with edge cases
```
And also add:
```
Tests passing - safe to refactor without breaking existing behavior
```

💡 **Why this matters**: These memories persist across sessions. If you return to this project later, Claude will know you have a comprehensive test suite ready.

### 3.5 Navigate Command History
- Use `↑` and `↓` arrow keys to navigate through previous commands
- Quickly re-run test commands this way

## Part 4: Refactoring with Rewind Safety (8 minutes)

### 4.1 Analyze Code Quality
```
What are the main code quality issues in this implementation? 
List the top 3 problems that make this code hard to maintain.
```

### 4.2 First Refactoring
```
Let's start refactoring. Extract the logic for each item type into separate methods.
Make the changes and run the tests to ensure they still pass.
```

### 4.3 Experiment with Bigger Changes
```
I need an additional refactoring - add an additional test case for the item type "Vegemite". Treat this as a normal item.
```

Check the code to ensure "Vegemite" is added correctly.

### 4.4 Use Rewind Feature
Press `Esc` twice (or type `/rewind`) to open the rewind menu:
- Choose a previous checkpoint to restore
- Options:
  - **Restore code and conversation**: Full restoration to that point
  - **Restore conversation**: Keep code changes, rewind conversation
  - **Restore code**: Revert file changes, keep conversation  

💡 **Key Feature**: Automatic checkpoints at each prompt + `/rewind` = fearless experimentation

### 4.5 Add New Feature
```
Perfect! Now add support for "Conjured" items that degrade in quality twice as fast as normal items.
Write tests first, then implement the feature, and verify tests pass.
```

## Part 5: Advanced Features & Workflows (2 minutes)

### 5.1 Check Token Usage and Context
```
/cost
```
Shows how many tokens you've used in this session.

```
/context
```
Shows your current context window usage - helpful to know when you're approaching limits.

### 5.2 Review Your Work
```
Can you summarize all the refactoring changes we made today?
What improvements did we achieve in terms of code quality?
```

### 5.3 Create Commit
```
Create a git commit with all our changes. Write a detailed commit message explaining 
the refactoring steps and the new Conjured items feature.
```

## Command Reference

### Essential Claude Code Commands

| Command | Purpose | Usage |
|---------|---------|-------|
| `/init` | Analyze project structure | Start of project session |
| `/rewind` | Access checkpoint history | Undo changes/conversation |
| `/memory` | Open memory files in editor | Organize persistent context |
| `/context` | Show context window usage | Monitor available space |
| `/cost` | Show token usage | Monitor session usage |
| `/compact [focus]` | Compress conversation | Manage long sessions |
| `/status` | Session information | Check model, tools, state |
| `/help` | List all commands | Discover features |
| `Ctrl+D` | Exit session | End Claude Code |

### Keyboard Shortcuts

| Shortcut | Action | Context |
|----------|--------|---------|
| `#` at line start | Add to memory | Persistent across sessions |
| `Esc` | Interrupt | Interrupt the current operation |
| `Esc + Esc` | Open rewind menu | Restore previous state. Also clears the current message. |
| `↑/↓` arrows | Command history | Recall previous inputs |
| `Shift+Tab` | Toggle permissions | Auto-accept/Plan/Normal |
| `Ctrl+C` | Cancel generation | Stop current output |
| `Ctrl+L` | Clear screen | Keep conversation history |

### Multiline Input
For pasting code or writing multiple lines:
- **Quick escape**: `\` + Enter
- **macOS**: Option + Enter
- **After setup**: Shift + Enter (run `/terminal-setup` first)

## Memory Hierarchy

| Type | Location | Purpose |
|------|----------|---------|
| Project | `./CLAUDE.md` | Team-shared context |
| User | `~/.claude/CLAUDE.md` | Personal preferences |
| Project Local | `./CLAUDE.local.md` | Personal + project specific |

## Pro Tips

### Effective Memory Usage
- Use `#` to capture decisions, patterns, and project conventions
- Memories persist across sessions - build knowledge over time
- Review with `/memory` to organize and refine

### Checkpoint Strategy
- **Automatic**: Every prompt creates a checkpoint (configurable in settings)
- **Rewind Options**: Restore code, conversation, or both
- **Experiment Freely**: Know you can always go back

### Permission Modes
- Start in **Normal mode** to learn what Claude does
- Switch to **Auto-Accept** when you trust the changes
- Use **Plan Mode** for complex operations

### Session Management
- `/context` to monitor context window usage
- `/cost` to monitor token usage
- `/compact` to compress long conversations
- `/status` to check current state

## 30-Minute Checklist

By session end, you should have:
- [ ] Used `/init` to analyze the project
- [ ] Added memories with `#` (at least 3)
- [ ] Used `/rewind` to restore a checkpoint
- [ ] Navigated history with arrow keys
- [ ] Written and run tests
- [ ] Refactored with automatic checkpoints as safety
- [ ] Added new feature with TDD
- [ ] Checked usage with `/cost` and `/context`

## Common Patterns

### Safe Experimentation Pattern
```
"Try a radical refactoring approach"    # Auto-checkpoint created
"Run tests"                             # Check if it worked
/rewind                                 # Restore if needed
Select: Code only                       # Keep conversation, revert code
```

### Memory Building Pattern
```
"Explain this complex business logic"
# Aged Brie increases quality up to 50
# Backstage passes increase by 2 when 10 days, by 3 when 5 days
/context                                # Check if approaching limits
/memory                                 # Review and organize
```

### Incremental Refactoring Pattern
```
"Analyze the code quality issues"       # Get baseline understanding
"Extract method for normal items"       # Small change
"Run tests"                             # Verify
"Extract method for special items"      # Next small change
"Run tests"                             # Verify
"How much cleaner is the code now?"     # Assess improvements
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Lost in conversation | `/compact` to focus on current state |
| Want to undo | `/rewind` or `Esc + Esc` |
| High token usage | Check with `/cost`, use `/compact` |
| Context window filling | Check with `/context`, use `/compact` if needed |
| Forgot what you added | `/memory` to review |
| Tests not running | Ask "What command runs tests?" |
| Need multiline input | `/terminal-setup` then use Shift+Enter |

## Next Steps

1. Explore more commands with `/help`
2. Set up team conventions in shared `CLAUDE.md`
3. Try `/agents` for specialized tasks
4. Explore `/mcp` for external tool integration
5. Create custom slash commands in `.claude/commands/`

## Quick Reference

```bash
# Start session
claude

# Essential in-session commands
/init                    # Analyze project
/rewind                  # Access checkpoints (or Esc+Esc)
/memory                  # Edit memory files
/context                 # Check context window usage
/cost                    # Token usage
/compact                 # Compress conversation
/help                    # All commands

# Shortcuts
# memory note            # Add to CLAUDE.md
Esc + Esc               # Open rewind menu
Shift + Tab             # Toggle permissions
↑/↓                     # Command history
Ctrl + D                # Exit session
```

---

*Remember: Claude Code automatically checkpoints every prompt, so experiment fearlessly! The combination of memories, checkpoints, and code review makes it a true AI pair programmer.*