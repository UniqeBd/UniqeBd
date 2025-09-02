# 🔐 Personal Access Token Setup Guide

To include **private repositories** in your language statistics, you need to set up a Personal Access Token (PAT).

## 📋 **Quick Setup Steps:**

### 1. **Create a Personal Access Token**
1. Go to [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name: `Language Stats Token`
4. Set expiration: `90 days` or `No expiration` 
5. Select these scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `read:user` (Read user profile data)

6. Click **"Generate token"**
7. **Copy the token** (you won't see it again!)

### 2. **Add Token to Repository Secrets**
1. Go to your repository: `https://github.com/UniqeBd/UniqeBd/settings/secrets/actions`
2. Click **"New repository secret"**
3. Name: `PERSONAL_ACCESS_TOKEN`
4. Value: paste your token
5. Click **"Add secret"**

## 🚀 **Using Private Repository Access:**

### **Automatic Workflows:**
- The workflows will automatically detect the token
- Private repos will be included in scheduled runs

### **Manual Workflow:**
1. Go to [Actions → Simple Language Statistics Update](https://github.com/UniqeBd/UniqeBd/actions/workflows/simple-language-stats.yml)
2. Click **"Run workflow"**
3. Set **"Include private repositories"** to `true`
4. Click **"Run workflow"**

## 🔍 **What You'll See:**

### **Without Personal Token:**
```
Total repositories found: 23
  🌐 Public: 23
  🔒 Private: 0
```

### **With Personal Token:**
```
Total repositories found: 35
  🌐 Public: 23
  🔒 Private: 12
```

## ⚠️ **Security Notes:**

- **Never commit tokens to code**
- **Use repository secrets only**
- **Regenerate tokens periodically**
- **Only grant minimum required permissions**

## 🧪 **Testing:**

You can test the setup by:
1. Running the **Test Language Statistics Update** workflow
2. Set `include_private` to `true` 
3. Check the logs for private repository detection

## 🆘 **Troubleshooting:**

### **No private repos showing:**
- Check if `PERSONAL_ACCESS_TOKEN` secret exists
- Verify token has `repo` scope
- Make sure token hasn't expired

### **Workflow still failing:**
- Token may be invalid
- Check token permissions
- Try regenerating the token

### **Rate limiting:**
- Use Personal Access Token (higher rate limits)
- Reduce frequency of runs
- Token gives 5000 requests/hour vs 60 for unauthenticated
