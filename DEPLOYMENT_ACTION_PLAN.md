# 🚀 Vercel Deployment Action Plan (5 Steps)

**Status**: Ready to Deploy  
**Estimated Time**: 20 minutes  
**Difficulty**: Beginner-friendly  

---

## Step 1️⃣ : Generate Secure Secret Key (2 min)

Run this command in PowerShell to generate a 50-character secure key:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

**Example output**:
```
L_Qj8mK9x2P_vWbY-fN3Q5rT7sU_zX1cA2dB_eF4gH_iJ5k6
```

**💾 Copy this value** — you'll need it in Step 3.

---

## Step 2️⃣ : Commit Code to GitHub (3 min)

Push the latest code with deployment documentation:

```powershell
cd "d:\Microsoft_Nitesh\nayi_raah\nayi_raah\nayiraah"
git add .
git commit -m "Deployment: Add deployment readiness report and action plan"
git push origin main
```

**Verify**:
- ✅ No errors during push
- ✅ Your GitHub repo shows the latest commit

---

## Step 3️⃣ : Configure Vercel Environment Variables (5 min)

1. **Go to**: [https://vercel.com/dashboard](https://vercel.com/dashboard)
2. **Select**: Your `nayi_raah` project
3. **Navigate to**: Settings → Environment Variables
4. **Add these variables**:

### Critical Variables (REQUIRED)
| Name | Value | Notes |
|------|-------|-------|
| `DJANGO_SECRET_KEY` | Paste from Step 1 | Replace with your generated key |
| `DJANGO_DEBUG` | `false` | Enables production security |
| `DJANGO_SITE_DOMAIN` | `nayiraah.org` | Replace with your custom domain |
| `DJANGO_ALLOWED_HOSTS` | `nayi-raah-abc123.vercel.app,nayiraah.org,www.nayiraah.org` | Replace `nayi-raah-abc123` with your actual domain |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://nayi-raah-abc123.vercel.app,https://nayiraah.org,https://www.nayiraah.org` | Must include `https://` protocol |

**Where to find your Vercel domain** (if you haven't deployed yet):
- It will be something like: `nayi-raah-abc123.vercel.app`
- You can find it after the first deployment in Vercel dashboard
- For now, use a placeholder and update after first deployment

### Optional Variables
| Name | Value | Only if... |
|------|-------|-----------|
| `DATABASE_URL` | `postgresql://...` | Using PostgreSQL instead of SQLite |
| `DJANGO_EMAIL_HOST` | `smtp.gmail.com` | Want to send emails |
| `DJANGO_EMAIL_HOST_USER` | `your@email.com` | Want to send emails |
| `DJANGO_EMAIL_HOST_PASSWORD` | `<app-password>` | Want to send emails |

**Save screenshot** of all entered variables for reference.

---

## Step 4️⃣ : Deploy (5 min)

### Option A: Automatic Deployment (Easiest)
1. Go to your Vercel project
2. Wait for the build to automatically start (it detects your GitHub push)
3. Watch the build progress in real-time
4. Once complete, you'll see the deployment URL

### Option B: Manual Deployment
1. In Vercel dashboard, click **"Deploy"** button
2. Select the latest commit
3. Click **"Deploy"**
4. Wait 2-5 minutes for build to complete

**What to watch for**:
- ✅ Build starts: "npm install", "pip install", "collectstatic"
- ✅ Build succeeds: Green checkmark and "Production" badge
- ✅ ❌ Build fails: Check logs for errors (usually missing env vars)

---

## Step 5️⃣ : Test Deployment (5 min)

### 1. Visit Your Site
```
https://nayi-raah-abc123.vercel.app
```

✅ Homepage should load with CSS and images

### 2. Test Each Page
- [ ] `/` — Homepage with resource cards
- [ ] `/about/` — About page
- [ ] `/resources/` — Resources/Find a Path
- [ ] `/work/` — Timeline of work
- [ ] `/sunshine/` — Daily quote
- [ ] `/admin/` — Django admin interface

### 3. Test Contact Form (CRITICAL)
1. Go to `/contact/`
2. Fill out the form:
   - Name: "Test User"
   - Email: "test@example.com"
   - Message: "This is a test"
3. Click **Submit**
4. ✅ Expected: Success message appears
5. ❌ If you see **HTTP 400 error**: Check `DJANGO_CSRF_TRUSTED_ORIGINS` env var

### 4. Check Browser Console
- Open DevTools (F12)
- Go to **Network** tab
- Refresh page
- Look for any 404 errors on CSS/JS files
- ✅ All requests should be 200 or 304 (cached)

### 5. Monitor for 24 Hours
- Watch Vercel dashboard for any errors
- Check error logs occasionally
- Test forms every few hours

---

## ✅ Success Checklist

After completing all 5 steps:

- [ ] Secret key generated and used
- [ ] Code pushed to GitHub
- [ ] Environment variables set in Vercel
- [ ] Deployment completed successfully
- [ ] Homepage loads correctly
- [ ] Contact form works without errors
- [ ] No 404 errors for static files
- [ ] Admin interface accessible

---

## 🆘 If Something Goes Wrong

### Build Fails
**Solution**: Check Vercel build logs for errors
- Usually: Missing environment variable
- Fix: Add the missing var and redeploy

### 400 Error on Form Submit
**Solution**: Update `DJANGO_CSRF_TRUSTED_ORIGINS`
1. Find your actual Vercel URL in the deployment logs
2. Update the env var to include that URL
3. Redeploy

### Static Files 404
**Solution**: Ensure collectstatic ran
- Check Vercel build logs for collectstatic output
- Verify `vercel.json` buildCommand is correct
- Redeploy

### Page Looks Broken
**Solution**: Check browser console
- Open F12 → Console tab
- Look for any JavaScript errors
- Check Network tab for failed requests

---

## 📞 Quick Help

| Issue | Check |
|-------|-------|
| "Can't find domain" | Verify `DJANGO_ALLOWED_HOSTS` env var |
| "Form gives error" | Verify `DJANGO_CSRF_TRUSTED_ORIGINS` env var |
| "Build fails" | Check all env vars are set |
| "CSS doesn't load" | Check Network tab for 404 on static files |
| "Admin not working" | Ensure `DJANGO_DEBUG=false` for security |

**Full troubleshooting**: [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)

---

## 📅 Timeline

```
T+0min:    Start here
T+2min:    ✅ Secret key generated
T+5min:    ✅ Code pushed to GitHub
T+10min:   ✅ Environment variables configured
T+15min:   ✅ Deployment started
T+20min:   ✅ Deployment complete
T+25min:   ✅ Testing complete
```

---

## 🎉 Congratulations!

Once you complete all 5 steps and see a working site, you're done! Your Django Nayi Raah site is live on Vercel.

**Next steps**:
- Point your custom domain to Vercel (DNS setup)
- Configure email notifications
- Add more content via `/admin/`
- Monitor performance in Vercel dashboard

---

**Ready? Start with Step 1️⃣ above!** 🚀
