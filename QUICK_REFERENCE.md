# Quick Reference - Testing, Committing, Deploying & Debugging

## 1. TEST LOCALLY

### Run Django checks
```bash
cd c:\Users\mamir\Desktop\nayi_raah\nayi_raah\nayiraah

# Basic system checks
python manage.py check

# Production deployment checks
python manage.py check --deploy

# Collect static files (as Vercel build will do)
python manage.py collectstatic --noinput

# Start local development server
python manage.py runserver
# Visit http://127.0.0.1:8000 in browser
# Test form submission at http://127.0.0.1:8000/contact/
```

### Expected Local Test Results
```
✅ python manage.py check
   System check identified no issues (0 silenced).

✅ python manage.py check --deploy
   System check identified some issues:
   WARNINGS:
   ?: (security.W008) SECURE_SSL_REDIRECT not set...  [OK - Vercel handles]
   ?: (security.W009) SECRET_KEY has less than 50 characters...  [OK - Env var will override]

✅ python manage.py collectstatic --noinput
   131 static files copied to 'staticfiles', 391 post-processed.

✅ Forms submit successfully at /contact/ → see success message
```

---

## 2. COMMIT TO GIT

### Review changes
```bash
$env:PATH = "C:\Program Files\Git\bin;$env:PATH"
cd "c:\Users\mamir\Desktop\nayi_raah\nayi_raah\nayiraah"

# View what changed
git status
git diff

# View last few commits
git log --oneline -5
```

### Commit all changes
```bash
# Add all modified files
git add .

# Commit with descriptive message
git commit -m "Your descriptive message about the changes"

# Or use: git commit -am "message" to add and commit in one step
```

### Example commit for this fix (already done):
```bash
git commit -m "Fix: Resolve HTTP 400 Bad Request errors on Vercel deployment

- Fix CSRF_TRUSTED_ORIGINS to dynamically include Vercel domain
- Improve ALLOWED_HOSTS configuration for Vercel
- Change DEBUG default to False for production
- Update vercel.json to modern format
- Add comprehensive logging
- Add deployment documentation"
```

### Push to GitHub
```bash
git push origin main

# Verify
git log --oneline -1
# Should show: ef85210 Add comprehensive deployment fix summary
```

---

## 3. DEPLOY TO VERCEL

### Automatic Deployment (if connected)
- Push to GitHub → Vercel automatically detects and deploys
- Takes 2-5 minutes
- Watch deployment progress in Vercel Dashboard

### Manual Deployment via Vercel CLI
```bash
# Install Vercel CLI (one time)
npm install -g vercel

# Login
vercel login

# Deploy from project directory
cd "c:\Users\mamir\Desktop\nayi_raah\nayi_raah\nayiraah"
vercel --prod

# Check deployment status
vercel inspect <URL>
```

### Set Environment Variables in Vercel

**Via Vercel Dashboard:**
1. Go to https://vercel.com/dashboard
2. Select your project: `nayi-raah` (or whatever name)
3. Click "Settings" → "Environment Variables"
4. Add each variable:

```
Variable Name                Value
─────────────────────────────────────────────────────────────
DJANGO_SECRET_KEY           [Generate with: python -c "import secrets; print(secrets.token_urlsafe(50))"]
DJANGO_DEBUG                false
DJANGO_ALLOWED_HOSTS        nayi-raah-xxxxx.vercel.app,nayiraah.org,www.nayiraah.org
DJANGO_CSRF_TRUSTED_ORIGINS https://nayi-raah-xxxxx.vercel.app,https://nayiraah.org,https://www.nayiraah.org
DJANGO_SITE_DOMAIN          nayiraah.org
```

**Via Vercel CLI:**
```bash
vercel env add DJANGO_SECRET_KEY
# Paste: <your-50-char-random-string>

vercel env add DJANGO_DEBUG
# Paste: false

vercel env add DJANGO_ALLOWED_HOSTS
# Paste: nayi-raah-xxxxx.vercel.app,nayiraah.org,www.nayiraah.org

# ... etc for each variable
```

### Redeploy with New Environment Variables
```bash
# After adding env vars, redeploy
vercel --prod

# Or in Dashboard: Click "Redeploy" on latest deployment
```

---

## 4. INSPECT VERCEL LOGS & DEBUG

### View Real-Time Logs
```bash
# Using Vercel CLI
$env:PATH = "C:\Program Files\Git\bin;$env:PATH"
vercel logs --tail

# Output will show:
# ✓ GET /static/css/style.css
# ✓ GET /
# ✓ POST /contact/
# ✗ DisallowedHost at /contact/ [means ALLOWED_HOSTS issue]
# ✗ CSRF token missing or incorrect [means CSRF_TRUSTED_ORIGINS issue]
```

### View Deployment Logs in Dashboard
1. Go to https://vercel.com/dashboard
2. Select project
3. Click "Deployments" tab
4. Click latest deployment
5. Scroll to "Build Logs" and "Runtime Logs"

### Common Log Messages & Solutions

```
Error: DisallowedHost at /
Invalid HTTP_HOST header

→ SOLUTION: Add domain to DJANGO_ALLOWED_HOSTS environment variable
→ EXAMPLE: DJANGO_ALLOWED_HOSTS=nayi-raah-xyz.vercel.app,nayiraah.org
```

```
Error: CSRF token missing or incorrect
Reason given for failure:
  CSRF failure: Origin checking failed - domain not in CSRF_TRUSTED_ORIGINS.

→ SOLUTION: Add domain to DJANGO_CSRF_TRUSTED_ORIGINS environment variable
→ EXAMPLE: DJANGO_CSRF_TRUSTED_ORIGINS=https://nayi-raah-xyz.vercel.app,https://nayiraah.org
→ IMPORTANT: Must include https:// prefix!
```

```
[INFO] Starting Django...
[INFO] Collecting static files...
System check identified no issues (0 silenced).

→ GOOD: Django started successfully
→ NEXT: Test form submission at /contact/
```

### Test Deployment from Command Line
```bash
# Get your Vercel URL (e.g., nayi-raah-xyz.vercel.app)
$VERCEL_URL = "nayi-raah-xyz.vercel.app"

# Test GET request (should return 200)
curl -i https://$VERCEL_URL/

# Test POST request to contact form (most important for 400 fix)
curl -i -X POST https://$VERCEL_URL/contact/ `
  -H "Content-Type: application/x-www-form-urlencoded" `
  -d "name=Test&email=test@example.com&phone=1234567890&message=Test%20message"

# Should return:
# ✓ 200 OK if successful
# ✗ 400 Bad Request if ALLOWED_HOSTS or CSRF_TRUSTED_ORIGINS issue
```

---

## 5. QUICK VERIFICATION CHECKLIST

### Before Deploying to Vercel
```bash
☐ cd c:\Users\mamir\Desktop\nayi_raah\nayi_raah\nayiraah
☐ python manage.py check
☐ python manage.py check --deploy
☐ python manage.py collectstatic --noinput
☐ Test local development server at http://127.0.0.1:8000/
☐ Test form submission at http://127.0.0.1:8000/contact/
☐ git status (no uncommitted changes)
☐ git log --oneline -1 (see latest commit)
```

### After Deploying to Vercel
```bash
☐ Vercel deployment shows "Ready" status
☐ Visit https://your-vercel-domain/
☐ Homepage loads successfully (GET request)
☐ Visit /contact/ page
☐ Fill contact form and click Submit (POST request)
☐ See success message "Thank you — your message has been sent"
☐ No 400 errors in Vercel logs
☐ Check Vercel logs for INFO messages (not ERROR)
```

### If 400 Error Occurs
```bash
☐ Run: vercel logs --tail
☐ Look for: "DisallowedHost" or "CSRF token missing"
☐ Check Vercel Dashboard → Environment Variables
☐ Verify DJANGO_ALLOWED_HOSTS includes your domain
☐ Verify DJANGO_CSRF_TRUSTED_ORIGINS includes your domain with https://
☐ Click "Redeploy" in Vercel Dashboard
☐ Wait 2-5 minutes for redeploy to complete
☐ Test again
```

---

## 6. HELPFUL COMMANDS REFERENCE

```bash
# Git operations
git status                          # See what changed
git add .                          # Stage all changes
git commit -m "message"            # Commit changes
git push origin main               # Push to GitHub
git log --oneline -5               # See recent commits

# Django operations
python manage.py check             # Basic checks
python manage.py check --deploy    # Production checks
python manage.py collectstatic     # Collect static files
python manage.py runserver         # Start dev server

# Vercel operations
vercel login                        # Login to Vercel
vercel --prod                       # Deploy to production
vercel logs --tail                  # Watch logs in real-time
vercel env add VAR_NAME             # Add environment variable

# Useful for testing
curl https://your-domain/                    # Test GET
curl -X POST https://your-domain/contact/ -d "data"  # Test POST
```

---

## 7. VERCEL DOMAIN LOCATIONS

### Find Your Vercel Domain
```
1. Go to https://vercel.com/dashboard
2. Click on your project (nayi-raah or similar)
3. Click "Deployments" tab
4. Latest deployment shows URL like:
   nayi-raah-abc123.vercel.app
   
   ^ This is your VERCEL_DOMAIN for environment variables
```

### Use in Environment Variables
```
DJANGO_ALLOWED_HOSTS = nayi-raah-abc123.vercel.app,nayiraah.org,www.nayiraah.org
DJANGO_CSRF_TRUSTED_ORIGINS = https://nayi-raah-abc123.vercel.app,https://nayiraah.org
```

---

## 8. GENERATE SECURE SECRET_KEY

```bash
# In Python:
python -c "import secrets; print(secrets.token_urlsafe(50))"

# Output: something like:
# bB7zQk9xC2F_xL8mA1nR3D5qW6sT7uV8yZ9aB0cE1fG2hJ3kL4m

# Copy this value to DJANGO_SECRET_KEY in Vercel
```

---

## Emergency: Rollback to Previous Deployment

```bash
# In Vercel Dashboard:
1. Go to Deployments tab
2. Find the working deployment (before your changes)
3. Click "..." menu
4. Select "Promote to Production"

# This instantly reverts to that deployment while you fix issues
```

---

## Summary of All Changes Made

**File: nayiraah_project/settings.py**
- ✅ DEBUG default changed to False
- ✅ ALLOWED_HOSTS expanded with *.vercel.app pattern
- ✅ CSRF_TRUSTED_ORIGINS now dynamically includes Vercel domain
- ✅ Added logging configuration

**File: vercel.json**
- ✅ Updated to modern Vercel functions format
- ✅ Added proper routing for Django app
- ✅ Configured static file caching

**File: nayiraah_project/wsgi.py**
- ✅ Added logging configuration

**File: .env.example**
- ✅ Added comprehensive documentation
- ✅ Added Vercel-specific instructions

**Files Added:**
- ✅ VERCEL_DEPLOYMENT.md - Full deployment guide
- ✅ DEPLOYMENT_FIX_SUMMARY.md - This summary

---

## Files to Share with Your Team

1. **DEPLOYMENT_FIX_SUMMARY.md** - Complete technical explanation
2. **VERCEL_DEPLOYMENT.md** - Step-by-step deployment guide  
3. **.env.example** - Environment variable template
4. This file - Quick reference for commands

---
