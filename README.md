![Let's get started with agentic coding!](assets/barbro-ai.jpg?raw=true)

# Kom igång med Agentisk Kodning!

## Let's Build!

* **Steg 1**: 
    - _Klona_ detta repository

* **Steg 2**: 
   - Kicka igång en DevContainer eller Codespace (rekommenderat) _ELLER_ kör lokalt (om du har Python 3.11 eller senare installerat)


## Övningar

### Gilded Rose Kata med Claude Code
Följ instruktionerna i [gildedrose/claude_code_gildedrose.md](gildedrose/claude_code_gildedrose.md) för att lära dig grunderna i agentisk kodning med Claude Code genom att refaktorera Gilded Rose-koden.

### Bonusövning: Bildgenerering med Nano Banana
I katalogen banana finns en kom-igång-prompt för att skapa en enkel bilgenererings-app med som använder Googles Nano Banana.

### Bonusövning2: Bygg en enkel TODO-app med Claude Code
Kommer...


## Hemligheter / Secrets
...finns [här](https://docs.google.com/document/d/1GU-AHlKJ1WrakcmzZdqxsi9HrmI2nJY15bt23B0TWC0/edit?usp=drive_link) för inklistring på läpligt ställe (`.env`-fil etc)`. 


## Länkar
- [Anthropic Prompt Generator - generera en prompt givet ett mål/task](https://platform.claude.com/dashboard)
    - Välj "Generate a Prompt"
- Lite tips för agentisk kodning: [AGENTIC-CODING-TIPS.md](AGENTIC-CODING-TIPS.md)
- [Claude Code docs](https://docs.claude.com/en/docs/claude-code/overview)
- [Claude Code: Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices)


## Claude Code

### Autentisering via Console Account
![Sign in](assets/cc-sign-in.png?raw=true)

Om du inte redan har ett konto och prenumeration för Claude Code så kan du logga in via (Tobias) "Console account" - **säg till så får du en inbjudan**.

### Misc
- För en lista med redan på förhand godkända operationer (kolla gärna igenom först) - kopiera `.claude/settings.local-example.json` och byt namn till `.claude/settings.local.json`. Kom ihång att .claude mappen måste ligga i den katalog du kör igång claude från.
- Övriga potentiellt intressanta filer:
    - Guidelines under `docs/guidelines`
    - En "mall" för CLAUDE.md: [CLAUDE.template.md](CLAUDE.template.md)
    - Exempel på custom slash commands: `.claude/commands`


### YOLO
Dev containern sätter upp ett alias (_`yoloc`_) för att köra i så kallt "YOLO mode" (även kännt som "ingen-minns-en-fegis-läge"). Du kan också köra igång detta läge genom att starta claude med: _`claude --dangerously-skip-permissions`_.


## DevContainer (för nyfikna)
Se `.devcontainer/devcontainer.json` samt `setup-devcontainer.sh` för detaljer kring devcontainer-konfigurationen.



_**Detaljerade instruktioner följer nedan:**_


-----


## Configuration Development Environment

### Local (or Cloud) Development Environment Setup

#### 1. Use GitHub Codespaces - (requires a GitHub-account):
- _(Recommended first step if you want to save your changes: **Fork this repo**)_ <br/>
    <img src="assets/fork.png" height="30"/>

- Click "Code" and then "Create codespace on main" in the GitHub UI<br/>
    <img src="assets/code.png" height="30"/><br/>
    <img src="assets/codespacer.png" height="30"/>
    <br/>

- Wait for the codespace to be created and then create a `.env` file with the API-keys.
    (_**See below for screenshots**_)

#### 2. Use a Dev Container (requires Docker or similar installed locally):
1. Install [Docker](https://www.docker.com/get-started/) (or similar container runtime).
2. Open this folder in VSCode.
3. Install the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension if you haven't already.
3. When prompted, click "Reopen in Container".
4. Create a `.env` file with your API keys.



-----


## Troubleshooting

### Creating a Private Fork (_After_ Cloning)

If you've already cloned this repository and want to convert it to a private fork to save your work:

1. **Update your local repository's remote**:
   ```bash
   # Check your current remote
   git remote -v

   # Add your new private repo as a remote (or rename the existing origin)
   git remote add private https://github.com/YOUR_USERNAME/ai-agenter-2025-private.git

   # OR rename the existing origin to upstream and add your private repo as origin
   git remote rename origin upstream
   git remote add origin https://github.com/YOUR_USERNAME/ai-agenter-2025-private.git
   ```

2. **Push your code to the private repository**:
   ```bash
   # Push all branches and tags to your private repo
   git push -u origin main
   git push origin --all
   git push origin --tags
   ```

3. **Keep your private fork updated** (optional):
   ```bash
   # If you renamed origin to upstream, you can pull updates from the original repo
   git fetch upstream
   git merge upstream/main
   git push origin main
   ```

**Note**: GitHub doesn't allow traditional forking of public repositories into private ones. This method creates an independent private repository with the same history.
