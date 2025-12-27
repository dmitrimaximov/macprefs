# Mac Preferences Backup

A tool to backup and restore Mac preferences.

This will backup and restore Application as well as System Preferences.

## Motivation (.macos problems)

I wanted a solution to back up my settings for my Mac and one didn't really exist. Time Machine is a bit overkill for this.

At first I was trying to create a bash script to restore all my settings. I was trying to adapt the ~~`.osx`~~ `.macos` file from [Mathias Bynens](https://github.com/mathiasbynens/dotfiles/blob/master/.macos). I noticed that some of the cases for the domains were wrong/outdated and weren't actually changing the preferences they were intended to change.

Running `defaults write` with the wrong case for the keys or domains also causes problems as the defaults command may fail silently.

## Requirements

- Mac OS X greater than 10.9 (maybe older… didn't test)
- Python 3.6

## Installation

Install [Homebrew](https://brew.sh/)

``` bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

``` bash
brew install clintmod/formulas/macprefs
```

## Config

You can set the MACPREFS_BACKUP_DIR environment variable to specify where you'd like to backup the prefs too.

The default backup directory is `~/Dropbox/Configuration/Backup/{machine_name}/{YYYY-MM-DD}`, where:
- `{machine_name}` is your Mac's hostname (e.g., "dima-macbook-pro")
- `{YYYY-MM-DD}` is the date of the backup (e.g., "2025-12-26")

This structure allows you to:
- Store backups from multiple Macs in the same Dropbox folder
- Keep version history with daily snapshots
- Easily identify which backup came from which machine

To override the default location:

```bash
export MACPREFS_BACKUP_DIR="$HOME/SomeOtherDir"
```

## Backing Up

You can backup your preferences by running:

``` bash
macprefs backup
```

You can also choose to backup selected preferences by running:

```bash
macprefs backup -t system_preferences startup_items preferences app_store_preferences internet_accounts
```

Following backups are currently possible:

**`system_preferences`** : Backs up system-level preferences including PowerManagement, TimeMachine, SoftwareUpdate, Bluetooth, and NetworkSharing

**`startup_items`** : Backs up `user launch agents`, `system launch agents` and `system daemon agents`

**`dotfiles`** : Backs up all your `dotfiles` from your home directory

**`shared_file_lists`** : Backs up `~/Library/Application Support/com.apple.sharedfilelist/` (Finder sidebar favorites)

**`ssh_files`** : Backs up `~/.ssh/` directory including keys and config

**`preferences`** : Backs up `~/Library/Preferences/` (all application preferences)

**`app_store_preferences`** : Backs up your App Store preferences

**`internet_accounts`** : Backs up your `~/Library/Accounts`

**`git_config`** : Backs up `.gitconfig` and `.gitignore_global`

**`cloud_credentials`** : Backs up AWS, Kubernetes, and Docker credentials

**`gpg_keys`** : Backs up GPG keys from `~/.gnupg/`

**`package_managers`** : Backs up Homebrew packages (Brewfile), npm global packages, and asdf tool versions

**`vscode_settings`** : Backs up VS Code settings, keybindings, snippets, and extension list

**`env_configs`** : Backs up environment configuration files (`.aliases`, `.exports`, `.config/`, etc.)

**`jetbrains_settings`** : Backs up JetBrains IDE settings (Rider, IntelliJ, WebStorm, etc.)

**`custom_fonts`** : Backs up custom fonts from `~/Library/Fonts/`

**`applications_list`** : Creates a list of all installed applications and Mac App Store apps (informational only)

**`runtime_versions`** : Records installed runtime versions (.NET, Node, npm, Python, Ruby, Go) (informational only)

**`alfred_settings`** : Backs up Alfred workflows and preferences

**`sublime_settings`** : Backs up Sublime Text and Sublime Merge settings

#### Note:

Make sure you have given full disk access to your terminal app for this script to work properly.
You can run this command to open system preference window

```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles"
```

## Restoring

You can restore your preferences by running:

``` bash
macprefs restore
```

Similar to **Backing**, you can choose to restore selected preferences by running

```bash
macprefs restore -t system_preferences startup_items preferences app_store_preferences internet_accounts
```

- **You might have to log out and then log back in for the settings to take effect.**

## New Mac Setup

If you're setting up a brand new Mac and want to restore your settings, follow these steps:

### 1. Install Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Follow the instructions to add Homebrew to your PATH
# Usually something like:
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### 2. Install macprefs

```bash
brew install clintmod/formulas/macprefs
```

### 3. Enable Full Disk Access for Terminal

```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles"
```

Add Terminal.app to the Full Disk Access list.

### 4. Set up Dropbox (if using Dropbox for backups)

- Download and install [Dropbox](https://www.dropbox.com/install)
- Sign in and wait for your Configuration/Backup folder to sync
- Make sure your backup folder is fully synced before proceeding

### 5. Restore your preferences

```bash
# If using the default Dropbox location, just run:
macprefs restore

# Or specify a custom backup location:
export MACPREFS_BACKUP_DIR="/path/to/your/backup/folder"
macprefs restore
```

### 6. Install your applications via Homebrew

If you backed up your Homebrew packages, restore them:

```bash
# Navigate to your backup's package_managers folder
cd ~/Dropbox/Configuration/Backup/{machine_name}/{date}/package_managers

# Install all packages from the Brewfile
brew bundle --file=Brewfile
```

This will automatically install:
- All command-line tools (git, node, etc.)
- All GUI applications (Chrome, Slack, Docker, etc.)
- All fonts
- Everything else you had installed via Homebrew

### 7. Check the detailed restore guide

After running the backup, a comprehensive `RESTORE.md` guide is generated in your backup folder with step-by-step instructions for:
- Installing runtime versions (.NET, Node.js)
- Installing VS Code extensions
- Installing Mac App Store apps
- Manual setup steps
- Troubleshooting common issues

```bash
# View the restore guide
open ~/Dropbox/Configuration/Backup/{machine_name}/{date}/RESTORE.md
```

## Testing the Restore

- Create a new user on your Mac
- Make sure he's in the admin group
- Log in as that user
- Do the [Getting Started](#getting-started) steps
- Update the [Config](#config)
- Grant the admin group read access to your backup files (substitute ~/Dropbox with your backup dir if different)

```bash
# grant admin group read on ~/Dropbox
chmod +a "group:admin allow list,search,readattr,readextattr,readsecurity" ~/Dropbox/
# grant admin group read on ~/Dropbox/MacPrefsBackup recursively (-R)
chmod -R +a "group:admin allow list,search,readattr,readextattr,readsecurity" ~/Dropbox/MacPrefsBackup
# grant dir list (execute) permission on all subfolders of ~/Dropbox recursively (-R)
chmod -R +X ~/Dropbox
# remove execute permission for other on all files and folders because
# +X adds other permissions
chmod -R o=-x ~/Dropbox
```

- Run the [Restore](#restoring)
- Log out and log back in to confirm the restore succeeded

## What it Does

### System & Application Preferences
- Backs up all the preferences in `~/Library/Preferences` and `/Library/Preferences`
- Backs up system preferences (PowerManagement, TimeMachine, SoftwareUpdate, Bluetooth, NetworkSharing)
- Backs up all 'Internet Accounts' databases in `~/Library/Accounts`
- Backs up shared file lists (Finder Favorites in Sidebar) `~/Library/Application Support/com.apple.sharedfilelist`
- Backs up App Store preferences

### Development Environment
- Backs up SSH keys and config (`~/.ssh/`)
- Backs up Git configuration (`.gitconfig`, `.gitignore_global`)
- Backs up GPG keys (`~/.gnupg/`)
- Backs up cloud credentials (AWS, Kubernetes, Docker)
- Backs up dotfiles (`~/.bash_profile`, `.zshrc`, `.aliases`, `.exports`, etc.)
- Backs up environment configs (`~/.config/`)

### Package Managers & Tools
- Creates Homebrew Brewfile for easy package reinstallation
- Records npm global packages
- Records asdf tool versions
- Records runtime versions (.NET SDKs, Node, npm, Python, Ruby, Go)

### IDE & Editor Settings
- Backs up VS Code settings, keybindings, snippets, and extensions list
- Backs up JetBrains IDE settings (Rider, IntelliJ, WebStorm, PyCharm, etc.)
- Backs up Sublime Text and Sublime Merge settings
- Backs up Alfred workflows and preferences

### Additional
- Backs up custom fonts (`~/Library/Fonts/`)
- Creates list of all installed applications (for reference)
- Backs up launch items (`/Library/LaunchAgents`, `/Library/LaunchDaemons`, `~/Library/LaunchAgents`)
- Generates comprehensive `RESTORE.md` guide with step-by-step restore instructions

## Notes

- ### Mackup
  - These scripts makes copies of plist files in `~/Library/Preferences` and is not compatible with the way [Mackup](https://github.com/lra/mackup) creates symlinks for some of these files. On the bright side though, if you use this as well as Mackup to backup and restore, everything should just work. Just remember that any preferences Mackup backs up won't be backed up by this tool.

- ### Using `defaults write`
  - When you run `defaults write` and use the wrong/old case for the domain you can create a new plist file with the wrong case (e.g. com.apple.addressbook instead of com.apple.AddressBook).
  - The `defaults` app has a tendency to fail silently for some things. You might be trying to use old `defaults write` commands where the key is the wrong name.
  - Because of the above 2 reasons maintaining a bunch of `defaults write` commands in bash script can be error prone and the defaults command will fail silently.

## Todo

- [x] Backup and restore `/Library/Preferences` (e.g. PowerManagement)
- [x] Installable via homebrew
- [x] Backup and restore shared file lists (Finder sidebar) `~/Library/Application Support/com.apple.sharedfilelist`
- [x] Backup and restore dotfiles (e.g. $HOME/.bash_profile)
- [x] $HOME/.ssh dir
- [x] Startup Items `/Library/LaunchAgents`, `/Library/LaunchDaemons`, `~/Library/LaunchAgents`
- [ ] Verify backup and restore
- [ ] Write a util to generate a `bash` script of `defaults write` commands by diffing a new user account against the owned account

## Problems

- If you find a problem or a have a question feel free to file a bug here and/or send a pull request and I'll be happy to look at it and/or merge it.

## Contributing

### Getting started

- Fork and clone then cd to this git repository
- Run `pip install -r requirements.txt`

### Running the tests

- Run `make test lint` (make sure you've done the [Getting Started](#getting-started))

### Getting your changes merged

- Make your changes and push them to github
- Make sure your changes have tests and pass linting
- Open a pull request
