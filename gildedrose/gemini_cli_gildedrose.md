# Gemini CLI Quickstart: Gilded Rose Kata
*A 30-minute hands-on adventure in Agentic AI Pair Programming*

## Overview
Welcome to the future of coding! In this session, you won't just be typing code; you'll be directing an autonomous AI agent. Gemini CLI isn't just a chatbot—it's a teammate that can run commands, edit files, and manage your project. You'll learn to wield this power while conquering the famous Gilded Rose Kata.


## Install Gemini CLI (when running locally)

### Prerequisites 
- Node.js 20+

### Installation
```bash
npm install -g @google/gemini-cli
```


## Part 1: Awakening the Agent

### 1.1 Setup the Playground
Let's get the environment ready. You can ask Gemini to do this, or run it yourself:

```bash
git clone https://github.com/emilybache/GildedRose-Refactoring-Kata.git
cd GildedRose-Refactoring-Kata
```

**Pick your poison (language):**
```bash
cd python  # or typescript, java, go, etc.
```

### 1.2 Start Gemini CLI Session
Start your Gemini CLI session.

```bash
gemini
```


### 1.3 The "Handshake"
The first step is to let the agent orient itself.

```bash
/init
```


This analyzes your project structure, identifies languages, frameworks, and dependencies.

💡 **Key Feature**: `/init` gives the agent deep understanding of your entire project
⚠️ **NOTE**: Depending on which [_approval mode_](https://geminicli.com/docs/get-started/configuration/#command-line-arguments) you've selected, you may need to approve commands (such as `ls`used by the init command) - But: _ingen minns en fegis_!


### 1.5 Check Session Status and Context
```
/stats
```

Shows current model, session and usage info.



## Part 2: Understanding & Memory Management

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













------






> **Prompt:** "Hi! Please analyze this project structure. Identify the source code and the test files. Tell me what language we are working in and how to run the tests."

💡 **Key Moment**: Watch as Gemini uses tools like `list_dir` and `find_by_name` to explore your drive. It's building its own mental map of your project.



## Part 2: Building Shared Brain (7 minutes)

### 2.1 The Knowledge Transfer
The Gilded Rose has complex rules. Instead of just pasting them into chat, let's create a **Persistent Memory** for the project. This ensures that even if the context window gets full, the knowledge remains.

> **Prompt:** "Read the code to understand the current logic. Then, create a file named `business-rules.md`. In it, create a markdown table explaining how Quality changes for each item type (Aged Brie, Backstage passes, Sulfuras, Normal). Include edge cases like max/min quality."

### 2.2 Verification
Open the generated `business-rules.md`.
> **Prompt:** "Does this cover the 'Conjured' item rules mentioned in the `TexttestFixture` or requirements? If not, note that they are missing for now."

💡 **Agentic Pattern**: *Documentation as Memory*. By writing to a file, you've given the agent a permanent reference point.

## Part 3: The Safety Net (8 minutes)

### 3.1 Establishing a Baseline
Before we change anything, we must ensure we don't break anything.
> **Prompt:** "Run the existing tests and report the results."

### 3.2 The "TextTest" Strategy
The current tests might be weak. Let's ask Gemini to fortify them.
> **Prompt:** "We need to refactor, but the tests are lacking. Please create a new test file (or update the existing one) to implement 'Golden Master' tests. I want you to generate output for 30 days for all items and verify it matches a known-good state. If you need to create a baseline file first, do so."

*Watch the agent run the code, capture the output, save it to a file, and then write a test that compares future runs against this file.*

### 3.3 The "Save Point"
Gemini CLI works directly on your files. This is powerful but dangerous. Let's create a save point.
> **Prompt:** "Great, the tests are passing. Please git add everything and commit with message 'Setup: Golden Master tests in place'."

💡 **Pro Tip**: Treat Git commits as your "Save Game" slots. You can always ask Gemini to "Revert the last commit" if things go sideways.

## Part 4: Refactoring with Superpowers (8 minutes)

### 4.1 The Architect's Eye
> **Prompt:** "Analyze `GildedRose.py` (or your language equivalent). Identify the deepest nesting and the most complex conditionals. Propose a refactoring plan to use Polymorphism or a Factory pattern to clean this up."

### 4.2 The Execution
Now, let the agent work.
> **Prompt:** "Execute the plan. Refactor the code to separate the logic for different items. **Crucial:** Run the tests after every significant change to ensure we haven't broken the Golden Master."

*Sit back and watch. You might see it edit the file, run the test, fail, read the error, edit the file again, and pass. This is the "Agentic Loop" in action.*

### 4.3 The "Undo" Button
Let's say it made a mess.
> **Prompt:** "That refactoring got too complicated. Please `git reset --hard HEAD` to go back to our save point. Let's try a simpler approach: just extract methods for now."

## Part 5: New Features & Workflows (2 minutes)

### 5.1 The "Conjured" Feature
Now that the code is clean (hopefully), adding features is easy.
> **Prompt:** "Now, implement the 'Conjured' item feature: they degrade twice as fast as normal items. Update the `business-rules.md` to reflect this, then add a test case for it, and finally implement the logic."

### 5.2 Automating the Future (Workflows)
You've been running tests manually. Let's automate that.
> **Prompt:** "Create a workflow file `.agent/workflows/test_and_commit.md`. It should have steps to: 1. Run the tests. 2. If they pass, git commit with a message provided by the user."

Now you can just say: "Run the test and commit workflow with message 'Added Conjured items'"!

## 30-Minute Checklist
By the end, you should have:
- [ ] Watched the agent explore your file system (`/init` equivalent)
- [ ] Created a persistent memory file (`business-rules.md`)
- [ ] Used Git as a safety checkpoint
- [ ] Watched the agent fail, debug, and fix its own code
- [ ] Created a custom Workflow to automate your tasks

## Agentic Design Patterns

### The "Supervisor" Pattern
You define the *what* and *why* (the strategy), and let the agent handle the *how* (the implementation).
*You: "Refactor this to use a Factory pattern."*
*Agent: (Edits 5 files, runs 3 tests)*

### The "Scribe" Pattern
Use the agent to maintain documentation that keeps *it* aligned.
*You: "Update the design-docs.md with the decision we just made."*

### The "Reviewer" Loop
Always ask the agent to verify its own work.
*You: "Did that change break any tests? Run them and check."*

---
*Enjoy your pair programming session! Remember, you are the pilot, Gemini is the engine.*
