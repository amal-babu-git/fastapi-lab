# 🔒 Security Configuration Guide

## Overview

This guide explains the security configuration for this FastAPI project, including proper `.gitignore`, `.dockerignore`, and environment variable management.

---

## ⚠️ IMPORTANT: .env File Was Removed from Git

The `.env` file containing sensitive credentials was previously committed to git history (commit: 91a9975).

### Current Status
- ✅ `.env` removed from git tracking
- ✅ `.env` added to `.gitignore`
- ✅ `.env.example` created as template
- ⚠️ `.env` still exists in git history

### ⚠️ Security Recommendation

**If this repository was pushed to a remote (GitHub, GitLab, etc.), you should:**

1. **Change all passwords and secrets** that were in the committed `.env` file
2. **Remove .env from git history** (see instructions below)
3. **Force push to remote** (if applicable)

---

## 🗑️ Removing .env from Git History

### Option 1: Using git filter-repo (Recommended)

**Installation:**
```bash
# Windows (with Python)
pip install git-filter-repo

# Or download from https://github.com/newren/git-filter-repo
```

**Remove .env from history:**
```bash
# Backup your repository first!
cd ..
cp -r fastapi-learn fastapi-learn-backup

cd fastapi-learn

# Remove .env from all history
git filter-repo --path .env --invert-paths

# If you have a remote, force push (DANGEROUS - coordinate with team!)
git push origin --force --all
```

### Option 2: Using BFG Repo-Cleaner

**Installation:**
```bash
# Download BFG from https://rtyley.github.io/bfg-repo-cleaner/
```

**Remove .env:**
```bash
# Clone a fresh copy
cd ..
git clone --mirror file:///d:/fastapi-learn fastapi-learn.git

# Run BFG
java -jar bfg.jar --delete-files .env fastapi-learn.git

cd fastapi-learn.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Push to remote (if applicable)
git push
```

### Option 3: Simple Approach (If No Remote Yet)

If you haven't pushed to a remote repository yet:

```bash
# Just commit the removal
git add .gitignore .env.example
git commit -m "chore: remove .env from tracking and add to .gitignore"

# The .env file is now untracked and won't be committed in future
# It still exists in history but if you haven't pushed anywhere, it's not exposed
```

---

## 📁 File Configuration

### .gitignore

Our `.gitignore` now includes:

```gitignore
# Environment variables (CRITICAL)
.env
.env.local
.env.*.local
.env.development
.env.test
.env.production
*.env

# Virtual environments
.venv
venv/
ENV/

# Python cache
__pycache__/
*.py[cod]

# Database files
*.db
*.sqlite
*.sqlite3
postgres-data/

# IDE files
.vscode/
.idea/

# OS files
.DS_Store
Thumbs.db

# Logs
*.log
logs/
```

### .dockerignore

Our `.dockerignore` prevents sensitive files from being copied into Docker images:

```dockerignore
# Environment files (NEVER in Docker images)
.env
.env.*
*.env

# Git files
.git
.gitignore

# Virtual environments
.venv
venv/

# Development files
docker-compose.yml
README.md
docs/

# IDE files
.vscode/
.idea/
```

---

## 🔐 Environment Variables Management

### Local Development

1. **Copy the template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit with your values:**
   ```bash
   # Windows
   notepad .env

   # Or use VS Code
   code .env
   ```

3. **Update sensitive values:**
   ```env
   POSTGRES_PASSWORD=your_secure_password_here
   SECRET_KEY=generate_a_random_secret_key
   ```

### Docker Development

For Docker Compose, update `.env`:
```env
POSTGRES_HOST=db  # Use service name from docker-compose.yml
```

### Production

**Never commit production credentials!**

Options for production:

#### Option 1: Environment Variables (Recommended)
```bash
# Set directly in your hosting platform
# AWS ECS, Azure App Service, Heroku, etc.
```

#### Option 2: Secret Management Services
- AWS Secrets Manager
- Azure Key Vault
- HashiCorp Vault
- Google Cloud Secret Manager

#### Option 3: .env file on server (with restricted permissions)
```bash
# On server
chmod 600 .env  # Only owner can read/write
chown appuser:appuser .env
```

---

## 🔒 Security Best Practices

### 1. Never Commit Secrets

❌ **Never commit:**
- Passwords
- API keys
- Secret keys
- JWT secrets
- Database credentials
- OAuth tokens
- Private keys

✅ **Safe to commit:**
- `.env.example` (with placeholder values)
- Configuration templates
- Public API endpoints
- Non-sensitive configuration

### 2. Use Strong Passwords

```python
# Generate secure secrets
import secrets

# For SECRET_KEY
secret_key = secrets.token_urlsafe(32)
print(f"SECRET_KEY={secret_key}")

# For JWT secret
jwt_secret = secrets.token_hex(32)
print(f"JWT_SECRET_KEY={jwt_secret}")
```

### 3. Rotate Credentials

If credentials are exposed:
1. ✅ Change all passwords immediately
2. ✅ Rotate API keys
3. ✅ Generate new secrets
4. ✅ Update all environments
5. ✅ Remove from git history

### 4. Use Different Credentials per Environment

```
Development:  POSTGRES_PASSWORD=dev_password_123
Staging:      POSTGRES_PASSWORD=staging_password_456
Production:   POSTGRES_PASSWORD=prod_password_789_very_secure
```

### 5. Restrict .env File Permissions

```bash
# Linux/Mac
chmod 600 .env
ls -la .env
# -rw------- 1 user user 245 Sep 30 16:00 .env

# Windows (PowerShell)
icacls .env /inheritance:r /grant:r "$env:USERNAME:F"
```

---

## 📋 Checklist: Before First Push

Before pushing to GitHub/GitLab/etc:

- [ ] `.env` is in `.gitignore`
- [ ] `.env` is not tracked (`git ls-files | grep .env` returns nothing)
- [ ] `.env.example` exists with placeholder values
- [ ] `.dockerignore` includes `.env`
- [ ] All sensitive files are in `.gitignore`
- [ ] No passwords in code comments
- [ ] No API keys in code
- [ ] Database credentials are environment variables

---

## 📋 Checklist: After Exposure

If `.env` was pushed to remote:

- [ ] Backup repository
- [ ] Change all exposed passwords
- [ ] Rotate all API keys
- [ ] Generate new secrets
- [ ] Remove from git history (git filter-repo)
- [ ] Force push to remote (coordinate with team!)
- [ ] Verify removal with `git log --all -- .env`
- [ ] Update all deployment environments

---

## 🔍 Checking for Exposed Secrets

### Check Git History
```bash
# Search for .env in history
git log --all --full-history --oneline -- .env

# Search for common secret patterns
git log --all -S "password" --oneline
git log --all -S "secret" --oneline
git log --all -S "api_key" --oneline
```

### Check Current Repository
```bash
# Check tracked files
git ls-files | grep -E "\\.env|password|secret"

# Check for common patterns in code
grep -r "password\s*=\s*['\"]" --include="*.py" .
grep -r "api_key\s*=\s*['\"]" --include="*.py" .
```

### Use Tools

**GitHub Secret Scanning**
- GitHub automatically scans for known secret patterns
- Check Security tab → Secret scanning alerts

**GitGuardian**
```bash
# Install
pip install ggshield

# Scan repository
ggshield secret scan repo .
```

**TruffleHog**
```bash
# Install
pip install truffleHog

# Scan
trufflehog --regex --entropy=True .
```

---

## 🛡️ Pre-commit Hooks

Prevent accidental commits of secrets:

### Install pre-commit
```bash
pip install pre-commit
```

### Create `.pre-commit-config.yaml`
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-added-large-files
      - id: detect-private-key
      - id: check-yaml
      - id: check-json
      
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

### Install hooks
```bash
pre-commit install
```

---

## 📚 Additional Resources

- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [git-filter-repo Documentation](https://github.com/newren/git-filter-repo)
- [12 Factor App - Config](https://12factor.net/config)

---

## 🎯 Summary

### What We Did
1. ✅ Enhanced `.gitignore` with comprehensive patterns
2. ✅ Created `.dockerignore` to prevent secrets in images
3. ✅ Removed `.env` from git tracking
4. ✅ Created `.env.example` as safe template
5. ✅ Documented security best practices

### What You Should Do
1. 🔴 **If pushed to remote**: Remove `.env` from git history
2. 🟡 **If not pushed yet**: Just commit the changes
3. 🟢 **Always**: Use `.env.example` as template
4. 🟢 **Always**: Never commit actual `.env` file
5. 🟢 **Production**: Use secret management services

### Current Files Status

| File | Status | Safe to Commit? |
|------|--------|----------------|
| `.env` | Untracked (was in history) | ❌ Never |
| `.env.example` | Untracked | ✅ Yes |
| `.gitignore` | Modified | ✅ Yes |
| `.dockerignore` | New | ✅ Yes |
| `database.py` | Tracked | ✅ Yes (uses env vars) |
| `models.py` | Tracked | ✅ Yes |

---

## 🚀 Next Steps

1. **Commit the security improvements:**
   ```bash
   git add .gitignore .dockerignore .env.example
   git commit -m "chore: enhance security configuration and remove .env from tracking"
   ```

2. **If repository is public or shared:**
   - Remove `.env` from history (see instructions above)
   - Change all passwords
   - Force push changes

3. **Set up pre-commit hooks** (optional but recommended)

4. **Document for your team:**
   - Share this security guide
   - Update README with setup instructions
   - Add section about environment variables

Remember: **Security is not a one-time task, it's an ongoing practice!** 🔒
