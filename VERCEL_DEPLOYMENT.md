# Django Nayi Raah - Vercel Deployment Guide

## Overview
This guide explains how to deploy the Nayi Raah Django application to Vercel and debug any deployment issues.

## Root Cause of HTTP 400 "Bad Request" Error

The HTTP 400 error typically occurs in two scenarios on Vercel:

### 1. **ALLOWED_HOSTS Mismatch** (Most Common)
- **Cause**: Django receives a request for a domain not in `ALLOWED_HOSTS`
- **Symptoms**: Any request to the app returns 400
- **Example**: Vercel domain is `my-app.vercel.app` but ALLOWED_HOSTS doesn't include it
- **Fix**: Add your Vercel domain to `DJANGO_ALLOWED_HOSTS` environment variable

### 2. **CSRF_TRUSTED_ORIGINS Mismatch** (For POST Requests)
- **Cause**: Form submission (POST request) comes from a domain not in `CSRF_TRUSTED_ORIGINS`
- **Symptoms**: Clicking "Submit" on forms returns 400; GET requests work fine
- **Example**: Contact form POST from `my-app.vercel.app` but CSRF_TRUSTED_ORIGINS only has `https://example.com`
- **Fix**: Add your Vercel domain to `DJANGO_CSRF_TRUSTED_ORIGINS` environment variable

## Vercel Deployment Steps

### Step 1: Verify Local Setup
```bash
# Test locally first
cd nayiraah
python manage.py check --deploy
python manage.py test
python manage.py runserver
```

### Step 2: Push to GitHub
```bash
git add .
git commit -m "Update: Fix Vercel deployment configuration"
git push origin main
```

### Step 3: Connect to Vercel

1. Go to https://vercel.com
2. Sign in with GitHub
3. Click "Add New" → "Project"
4. Select the `nayi_raah` repository
5. Click "Import"

### Step 4: Configure Environment Variables

**Critical for fixing 400 errors!**

In Vercel Project Settings → Environment Variables, add:

```
DJANGO_SECRET_KEY=<generate-a-secure-random-string>
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS=<your-vercel-domain>,<your-custom-domain>
DJANGO_CSRF_TRUSTED_ORIGINS=https://<your-vercel-domain>,https://<your-custom-domain>
DJANGO_SITE_DOMAIN=<your-custom-domain>
```

**Where to find your Vercel domain:**
- After first deployment, check Vercel project → Deployments
- It will be something like: `nayi-raah-abc123.vercel.app`

**Example for custom domain `nayiraah.org`:**
```
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS=nayi-raah-abc123.vercel.app,nayiraah.org,www.nayiraah.org
DJANGO_CSRF_TRUSTED_ORIGINS=https://nayi-raah-abc123.vercel.app,https://nayiraah.org,https://www.nayiraah.org
DJANGO_SITE_DOMAIN=nayiraah.org
```

### Step 5: Configure Database (Optional)

If using PostgreSQL instead of SQLite:

1. Set up a PostgreSQL database (e.g., via Vercel Postgres, Railway, or managed service)
2. Add environment variable:
   ```
   DATABASE_URL=postgresql://user:password@host:5432/dbname
   ```

### Step 6: Deploy

After setting environment variables:
1. Click "Deploy" button in Vercel
2. Wait for build to complete
3. Check deployment URL

### Step 7: Test the Deployment

1. Visit your Vercel domain (e.g., `https://nayi-raah-abc123.vercel.app`)
2. Test various pages: Home, About, Resources, Sunshine, Work
3. **Most Important**: Test form submission:
   - Go to /contact/
   - Fill out contact form
   - Click submit
   - Should see success message (not 400 error)

## Troubleshooting

### Error: "Bad Request (400)"

**Check 1: ALLOWED_HOSTS**
```bash
# View what Vercel is receiving
# This is visible in Vercel logs
```

**Check 2: CSRF_TRUSTED_ORIGINS**
- Error appears when submitting forms (POST requests)
- View Vercel logs for Django security warnings

**Check 3: DEBUG Mode**
- Should be `false` in production
- Set `DJANGO_DEBUG=false` in environment variables

### View Vercel Logs

```bash
# Using Vercel CLI
npm install -g vercel
vercel login
vercel logs --tail

# Or in Vercel Dashboard
# Project → Deployments → Latest → Logs
```

### Common Log Messages

```
DisallowedHost at /contact/
Invalid HTTP_HOST header

→ Fix: Add domain to DJANGO_ALLOWED_HOSTS
```

```
CSRF token missing or incorrect

→ Fix: Add domain to DJANGO_CSRF_TRUSTED_ORIGINS
```

## Production Security Checklist

- [ ] `DJANGO_DEBUG=false`
- [ ] `DJANGO_SECRET_KEY` is long and random (50+ characters)
- [ ] `DJANGO_ALLOWED_HOSTS` includes your production domain
- [ ] `DJANGO_CSRF_TRUSTED_ORIGINS` includes your production domain with `https://`
- [ ] Email configuration set up (if needed)
- [ ] Database configured (if not using SQLite)
- [ ] Static files collected (handled by `build.py`)

## Key Files Modified for Vercel

1. **nayiraah_project/settings.py**
   - Updated ALLOWED_HOSTS to be more flexible
   - Enhanced CSRF_TRUSTED_ORIGINS handling
   - Changed DEBUG default to False
   - Added logging configuration

2. **vercel.json**
   - Updated to modern Vercel format
   - Configured Python 3.11 runtime
   - Set up proper routing for Django app

3. **.env.example**
   - Added comprehensive documentation
   - Included Vercel-specific instructions

4. **nayiraah_project/wsgi.py**
   - Added logging configuration

## Local Development vs Production

| Setting | Local | Vercel |
|---------|-------|--------|
| DJANGO_DEBUG | true | false |
| DJANGO_ALLOWED_HOSTS | localhost,127.0.0.1 | your-domain.vercel.app,your-domain.com |
| DATABASE | SQLite (db.sqlite3) | PostgreSQL (DATABASE_URL) |
| Static files | served by Django | served by WhiteNoise |
| Email | console backend | SMTP backend |

## Additional Resources

- [Vercel Python Documentation](https://vercel.com/docs/functions/python)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)
- [dj-database-url Documentation](https://github.com/jacobian/dj-database-url)

## Support

If you continue to see 400 errors after deployment:

1. Check Vercel logs for the exact error message
2. Verify environment variables are set correctly
3. Check Django logs in Vercel output
4. Ensure the domain you're accessing matches ALLOWED_HOSTS
5. For form errors, check CSRF_TRUSTED_ORIGINS
