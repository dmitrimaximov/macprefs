from os.path import join, exists
import logging as log
from config import get_macprefs_dir
from datetime import datetime


def generate_readme():
    """Generate a comprehensive restore guide in the backup directory"""
    backup_dir = get_macprefs_dir()
    readme_path = join(backup_dir, 'RESTORE.md')

    # Get current date for the backup timestamp
    backup_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    readme_content = f"""# Mac Preferences Restore Guide

**Backup Date:** {backup_date}
**Backup Location:** {backup_dir}

This guide provides step-by-step instructions to restore your Mac setup from this backup.

---

## Prerequisites

Before you start, ensure you have:

1. **macOS installed** on your new/clean Mac
2. **Terminal app access** (Applications > Utilities > Terminal)
3. **Full Disk Access** enabled for Terminal:
   ```bash
   open "x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles"
   ```
   Add Terminal.app to the Full Disk Access list

---

## Quick Start (Automatic Restore)

For most settings, simply run:

```bash
# Clone or copy the macprefs tool to your new Mac
cd /path/to/macprefs

# Set backup directory environment variable
export MACPREFS_BACKUP_DIR="{backup_dir}"

# Run restore
./macprefs restore
```

This will automatically restore:
- SSH keys and config
- Shell configs (zsh, bash)
- Git configuration
- Cloud credentials (AWS, Kubernetes, Docker)
- GPG keys
- Development environment configs
- IDE settings (VS Code, JetBrains, Sublime, Alfred)
- Custom fonts
- Finder preferences and sidebar
- Dock settings
- All application preferences
- And more...

---

## Step-by-Step Restore Guide

Follow these steps in order for the best experience.

### Step 1: Install Homebrew

Homebrew will be used to install most applications and tools.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Follow the instructions to add Homebrew to your PATH
# Usually something like:
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### Step 2: Install macprefs Tool Dependencies

```bash
# Install Python 3 (if not already installed)
brew install python@3

# Install rsync (usually pre-installed, but ensure it's available)
which rsync
```

### Step 3: Clone/Copy macprefs Tool

```bash
# Option 1: Clone from git (if you have it in a repo)
# git clone <your-repo-url> ~/macprefs

# Option 2: Copy from backup or another location
# cp -r /path/to/macprefs ~/macprefs

cd ~/macprefs
```

### Step 4: Set Backup Directory

```bash
export MACPREFS_BACKUP_DIR="{backup_dir}"

# Add to your shell config to persist
echo 'export MACPREFS_BACKUP_DIR="{backup_dir}"' >> ~/.zshrc
```

### Step 5: Restore All Settings

```bash
./macprefs restore
```

Wait for the restore to complete. This will take a few minutes.

---

## Step 6: Install Applications via Homebrew

Your Homebrew packages (formulas and casks) are backed up and can be auto-installed:

```bash
# This should happen automatically during restore, but if needed:
cd {backup_dir}/package_managers
brew bundle --file=Brewfile
```

This will install all your:
- Command-line tools (git, node, etc.)
- GUI applications (Chrome, Slack, Docker, etc.)
- Fonts
- Everything else you had installed via Homebrew

**Time estimate:** 15-45 minutes depending on number of packages

---

## Step 7: Install Runtime Versions

### .NET SDK

Check your backed up versions:
```bash
cat {backup_dir}/runtime_versions/dotnet-sdks.txt
```

Install via Homebrew (recommended):
```bash
# Install latest .NET
brew install dotnet

# Or install specific version (check available versions)
brew install dotnet@9
brew install dotnet@10

# Verify installation
dotnet --version
dotnet --list-sdks
```

**Alternative:** Download from https://dotnet.microsoft.com/download

### Node.js and npm

Your Node/npm versions can be managed via nvm (Node Version Manager):

```bash
# Install nvm via Homebrew
brew install nvm

# Follow nvm setup instructions
mkdir ~/.nvm
echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.zshrc
echo '[ -s "/opt/homebrew/opt/nvm/nvm.sh" ] && \\. "/opt/homebrew/opt/nvm/nvm.sh"' >> ~/.zshrc
source ~/.zshrc

# Install your backed up node version
cat {backup_dir}/runtime_versions/versions.txt | grep node
nvm install <version>  # e.g., nvm install 24.11.1
nvm use <version>
```

**Alternative:** Install via Homebrew:
```bash
brew install node
```

---

## Step 8: Install VS Code Extensions

```bash
# Your extensions list is backed up
cat {backup_dir}/vscode/extensions.txt

# Install all extensions
cat {backup_dir}/vscode/extensions.txt | xargs -L 1 code --install-extension
```

---

## Step 9: Install Mac App Store Apps (Optional)

First, install `mas` CLI tool:
```bash
brew install mas

# Sign in to App Store first via the GUI
open -a "App Store"

# Then check your backed up App Store apps
cat {backup_dir}/applications/MasApplications.txt

# Install specific apps by ID
# mas install <app-id>
```

---

## Step 10: Manual Steps

Some things require manual setup:

### Sign in to Applications
- Dropbox
- Slack
- Email clients
- Browser sync (Chrome, Safari)
- Any other apps that require authentication

### System Preferences (if needed)
Some system preferences may need manual adjustment:
- Display scaling and arrangement
- Mission Control settings
- Some Accessibility options
- Touch ID setup

### Development Tools
- Sign in to GitHub/GitLab
- Configure any IDE licenses
- Set up any project-specific tools

---

## Post-Restore Checklist

After restoring, verify everything works:

- [ ] Terminal opens and shell config loaded (`echo $PATH`)
- [ ] Git works (`git --version`, `git config --list`)
- [ ] SSH keys work (`ssh -T git@github.com`)
- [ ] Cloud CLI tools work (`aws --version`, `kubectl version`)
- [ ] Node/npm installed (`node --version`, `npm --version`)
- [ ] .NET installed (`dotnet --version`)
- [ ] VS Code opens with settings
- [ ] JetBrains IDEs open with settings
- [ ] Alfred has your workflows
- [ ] Finder sidebar has favorites
- [ ] Dock is configured
- [ ] Homebrew apps installed (`brew list`)

---

## Troubleshooting

### Issue: "Operation not permitted" errors
**Solution:** Enable Full Disk Access for Terminal app (see Prerequisites)

### Issue: Homebrew not found
**Solution:** Run:
```bash
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### Issue: SSH keys not working
**Solution:** Check permissions:
```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_*
chmod 644 ~/.ssh/*.pub
```

### Issue: Dotfiles not loading
**Solution:** Restart Terminal or run:
```bash
source ~/.zshrc
# or
source ~/.bash_profile
```

### Issue: Git credentials not working
**Solution:** Check git config:
```bash
git config --list
# Update if needed:
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

---

## Reference: What Was Backed Up

This backup includes:

**Automatic Restore:**
- ✅ SSH keys and config
- ✅ Shell configs (.zshrc, .bash_profile, etc.)
- ✅ Git configuration
- ✅ Cloud credentials (AWS, Kubernetes, Docker)
- ✅ GPG keys
- ✅ Environment configs (.aliases, .exports, etc.)
- ✅ VS Code settings and keybindings
- ✅ JetBrains IDE settings (Rider, IntelliJ, etc.)
- ✅ Sublime Text/Merge settings
- ✅ Alfred workflows and settings
- ✅ Custom fonts
- ✅ Finder preferences
- ✅ Dock settings
- ✅ All application preferences
- ✅ System preferences

**Semi-Automatic (via Homebrew):**
- ✅ All Homebrew packages (Brewfile)
- ✅ Command-line tools
- ✅ GUI applications

**Informational (for reference):**
- 📋 List of all installed applications
- 📋 Runtime versions (.NET, Node, npm, Python, Ruby)
- 📋 VS Code extensions list
- 📋 npm global packages list

---

## Tips

1. **Take your time** - Don't rush through the restore process
2. **Test as you go** - Verify each step works before moving to the next
3. **Keep this guide** - You'll thank yourself next time you need to restore
4. **Update the backup** - Run `./macprefs backup` regularly to keep it current

---

## Need Help?

If you encounter issues:
1. Check the Troubleshooting section above
2. Review the backup logs (if any errors occurred)
3. Check the macprefs GitHub repository for updates

---

**Last Updated:** {backup_date}
"""

    try:
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        log.info('Generated restore guide at: %s', readme_path)
        return True
    except Exception as e:
        log.warning('Could not generate restore guide: %s', str(e))
        return False
