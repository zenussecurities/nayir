# 🚀 Vercel Deployment - Visual Quick Start

A visual guide to deploying your Nayi Raah site in 20 minutes.

---

## 📊 Deployment Timeline

```
Start (T=0)
    │
    ├─ T+2min  ──→ Generate Secret Key
    │              python -c "import secrets; print(secrets.token_urlsafe(50))"
    │
    ├─ T+5min  ──→ Set Environment Variables in Vercel
    │              DJANGO_SECRET_KEY (paste from above)
    │              DJANGO_DEBUG = false
    │              DJANGO_SITE_DOMAIN = nayiraah.org
    │              DJANGO_ALLOWED_HOSTS = ... (your domains)
    │              DJANGO_CSRF_TRUSTED_ORIGINS = https://... (your domains)
    │
    ├─ T+8min  ──→ Commit & Push to GitHub
    │              git add .
    │              git commit -m "Deploy"
    │              git push origin main
    │
    ├─ T+9min  ──→ Deploy (automatic or manual click)
    │              Vercel detects push and builds automatically
    │
    ├─ T+15min ──→ Build Complete ✅
    │              Vercel shows your deployment URL
    │
    ├─ T+20min ──→ Test & Go Live
    │              Visit your site and test
    │
    └─ Done! 🎉
```

---

## 🎯 The 5 Steps

### ① Generate Secret Key (Copy-Paste)
```powershell
python -c "import secrets; print(secrets.token_urlsafe(50))"
```
↓ **Copy the output** ↓

### ② Set Environment Variables
| Step | Variable | Value |
|------|----------|-------|
| 1 | `DJANGO_SECRET_KEY` | Paste from ① |
| 2 | `DJANGO_DEBUG` | `false` |
| 3 | `DJANGO_SITE_DOMAIN` | `nayiraah.org` |
| 4 | `DJANGO_ALLOWED_HOSTS` | `nayi-raah-abc123.vercel.app,nayiraah.org,www.nayiraah.org` |
| 5 | `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://nayi-raah-abc123.vercel.app,https://nayiraah.org,https://www.nayiraah.org` |

**Where**: Vercel Dashboard → Settings → Environment Variables

### ③ Commit & Push
```powershell
cd nayiraah
git add .
git commit -m "Deploy: Production ready"
git push origin main
```

### ④ Vercel Deploys (Automatic)
- Vercel detects push
- Builds Docker image
- Installs dependencies
- Collects static files
- Deploys to edge network
- ✅ **Done!**

### ⑤ Test Your Site
- [ ] Homepage loads
- [ ] All pages work
- [ ] Contact form submits
- [ ] No CSS/JS 404 errors

---

## 🎨 Visual Workflow

```
Your Computer
    │
    ├─ Generate SECRET_KEY
    │         │
    │         ↓
    │    Copy to clipboard
    │
    ├─ Vercel Dashboard
    │         │
    │         ├─ Environment Vars
    │         │   ├─ DJANGO_SECRET_KEY ← Paste here
    │         │   ├─ DJANGO_DEBUG = false
    │         │   ├─ DJANGO_SITE_DOMAIN = nayiraah.org
    │         │   ├─ DJANGO_ALLOWED_HOSTS = ...
    │         │   └─ DJANGO_CSRF_TRUSTED_ORIGINS = ...
    │         │
    │         └─ Click Deploy
    │
    ├─ Terminal
    │         │
    │         ├─ git add .
    │         ├─ git commit -m "Deploy"
    │         └─ git push origin main
    │
    └─ GitHub
         │
         └─ Vercel (detects push)
            │
            ├─ Install dependencies
            ├─ Collect static files
            ├─ Build server
            └─ Deploy to CDN
               │
               └─ ✅ Your site is live!
                  https://nayi-raah-abc123.vercel.app
```

---

## 📋 Checklist with Status

```
PRE-DEPLOYMENT
├─ [ ] Read DEPLOYMENT_ACTION_PLAN.md
├─ [ ] Have Python installed
├─ [ ] Have Git installed
└─ [ ] Have Vercel account

GENERATE SECRET KEY
├─ [ ] Run: python -c "import secrets; print(secrets.token_urlsafe(50))"
└─ [ ] Copy output

CONFIGURE VERCEL
├─ [ ] Log in to vercel.com
├─ [ ] Open your project
├─ [ ] Go to Settings → Environment Variables
├─ [ ] Add DJANGO_SECRET_KEY (paste from above)
├─ [ ] Add DJANGO_DEBUG = false
├─ [ ] Add DJANGO_SITE_DOMAIN = nayiraah.org
├─ [ ] Add DJANGO_ALLOWED_HOSTS = ...
├─ [ ] Add DJANGO_CSRF_TRUSTED_ORIGINS = https://...
└─ [ ] Click Deploy

PUSH CODE
├─ [ ] cd nayiraah
├─ [ ] git add .
├─ [ ] git commit -m "Deploy"
└─ [ ] git push origin main

WAIT FOR BUILD
├─ [ ] Vercel builds (2-5 minutes)
├─ [ ] Check logs for errors
└─ [ ] Wait for ✅ success

TEST SITE
├─ [ ] Visit homepage
├─ [ ] Click through all pages
├─ [ ] Test contact form
└─ [ ] Check no 404 errors

DONE ✅
└─ [ ] Your site is live!
```

---

## 🔍 Environment Variables Explained

### What is DJANGO_SECRET_KEY?
A random 50-character string that Django uses for security.
- Generate it once, keep it secret
- Never hardcode it in source
- Store in Vercel environment variables only
- Example: `L_Qj8mK9x2P_vWbY-fN3Q5rT7sU_zX1cA2dB_eF4gH_iJ5k6`

### What is DJANGO_ALLOWED_HOSTS?
List of domains that can access your site. Prevents spoofing attacks.
- `nayi-raah-abc123.vercel.app` = Your Vercel URL
- `nayiraah.org` = Your custom domain
- `www.nayiraah.org` = www subdomain
- Comma-separated, no spaces

### What is DJANGO_CSRF_TRUSTED_ORIGINS?
Whitelist of domains allowed to submit forms. Prevents cross-site attacks.
- Must start with `https://`
- Same domains as ALLOWED_HOSTS
- Includes `https://` prefix
- Example: `https://nayiraah.org,https://www.nayiraah.org`

---

## 🎯 Key Takeaways

| Concept | Remember |
|---------|----------|
| **SECRET_KEY** | Generate once, copy to Vercel, never share |
| **ALLOWED_HOSTS** | All domains your site uses (no https://) |
| **CSRF_TRUSTED_ORIGINS** | Same as ALLOWED_HOSTS but with https:// |
| **DJANGO_DEBUG** | Always `false` in production |
| **DATABASE_URL** | Only needed if using PostgreSQL |
| **BUILD TIME** | 2-5 minutes on Vercel |

---

## ⚡ Quick Troubleshooting

| Issue | Quick Fix |
|-------|-----------|
| "Can't find domain" | Check ALLOWED_HOSTS env var |
| "Form gives error" | Check CSRF_TRUSTED_ORIGINS env var |
| "CSS doesn't load" | Check Network tab for 404s |
| "Build failed" | Check Vercel logs for error |
| "50x Server Error" | Check Django logs for exceptions |

---

## 📱 Mobile-Friendly Checklist

After deployment, test on phone:

- [ ] Homepage loads
- [ ] Nav menu works
- [ ] Touch targets are big enough
- [ ] Forms are usable
- [ ] No horizontal scroll
- [ ] Images load fast

---

## 🎬 Visual Step-by-Step

### Step 1: Secret Key
```
Terminal                         PowerShell
┌─────────────────────────────────────────────┐
│ $ python -c "import secrets;                │
│   print(secrets.token_urlsafe(50))"         │
│                                             │
│ L_Qj8mK9x2P_vWbY-fN3Q5...                   │
│ ↑ COPY THIS                                 │
└─────────────────────────────────────────────┘
```

### Step 2: Vercel Dashboard
```
Browser                          Vercel.com
┌─────────────────────────────────────────────┐
│ Settings → Environment Variables            │
│                                             │
│ DJANGO_SECRET_KEY                          │
│ ├─ L_Qj8mK9x2P_vWbY-fN3Q5...  ← Paste!    │
│                                             │
│ DJANGO_DEBUG                                │
│ ├─ false                                    │
│                                             │
│ ... (add other 3 variables)                 │
│                                             │
│ [Deploy Button]                             │
└─────────────────────────────────────────────┘
```

### Step 3: Git Push
```
Terminal                         Git/GitHub
┌─────────────────────────────────────────────┐
│ $ git add .                                 │
│ $ git commit -m "Deploy"                    │
│ $ git push origin main                      │
│                                             │
│ → Vercel detects push                       │
│ → Starts building                           │
│ → 2-5 minutes...                            │
│ → ✅ Deployment complete!                   │
└─────────────────────────────────────────────┘
```

### Step 4: Test
```
Browser                          Your Site
┌─────────────────────────────────────────────┐
│ https://nayi-raah-abc123.vercel.app/       │
│                                             │
│ ✅ Homepage loads                           │
│ ✅ About page works                         │
│ ✅ Contact form submits                     │
│ ✅ CSS/JS load (no 404s)                    │
│ ✅ Mobile looks good                        │
│                                             │
│ 🎉 DONE! Site is live!                      │
└─────────────────────────────────────────────┘
```

---

## 🎯 Success Indicators

When you see these, you're done:

- ✅ Vercel shows "Production" badge
- ✅ Deployment URL is active
- ✅ Pages load in browser
- ✅ Contact form works
- ✅ No errors in browser console
- ✅ CSS and images visible
- ✅ Mobile view looks good

---

## ⏱️ Time Breakdown

```
Generating secret key ......... 2 min
Setting Vercel env vars ....... 3 min
Committing code ............... 1 min
Vercel build .................. 5 min (automatic)
Testing site .................. 4 min
                               ─────
TOTAL TIME ................... ~20 min
```

---

## 🚀 Let's Go!

Ready? Here's your path:

1. **Open**: [DEPLOYMENT_ACTION_PLAN.md](DEPLOYMENT_ACTION_PLAN.md)
2. **Follow**: 5 steps exactly as written
3. **Wait**: Build completes (2-5 min)
4. **Test**: Visit your site
5. **Celebrate**: 🎉 You're live!

---

**Questions?** Check [DEPLOYMENT_DOCS_INDEX.md](DEPLOYMENT_DOCS_INDEX.md)

**Let's deploy!** 🚀
