# Contributing to Startup Launch List

First off, thank you for considering contributing! Every addition and correction makes this resource better for the entire startup community.

## How Can I Contribute?

### 🆕 Adding New Directories

1. Fork the repository
2. Edit `data/directories.json`
3. Add your entry in the correct position (sorted by DR, highest first; no-DR entries at the end)
4. Submit a Pull Request with a brief description

**Required fields:**
```json
{
  "name": "Directory Name",
  "url": "https://example.com",
  "domain_rating": null,
  "link_type": null,
  "pricing": null,
  "category": "🚀 Startup Directory",
  "description": null
}
```

**Ideal entry (all fields filled):**
```json
{
  "name": "Directory Name",
  "url": "https://example.com",
  "domain_rating": 45,
  "link_type": "Dofollow",
  "pricing": "Freemium",
  "category": "🚀 Startup Directory",
  "description": "Brief description of what this directory offers."
}
```

### 📝 Updating Existing Data

Found incorrect or outdated data? We especially appreciate:

- **DR score updates** — Include the date you checked and tool used (Ahrefs preferred)
- **Link type corrections** — Dofollow vs Nofollow changes
- **Pricing changes** — Free → Paid, or vice versa
- **Broken URLs** — If a directory has moved or shut down
- **Better descriptions** — More accurate or detailed descriptions

### 🐛 Reporting Issues

Use GitHub Issues to report:

- Dead directories (site no longer exists)
- Incorrect data
- Duplicate entries
- Spam/low-quality directories that should be removed

## Guidelines

### What We Accept
- ✅ Legitimate startup/SaaS/AI tool directories
- ✅ Review platforms (G2, Capterra-style)
- ✅ Communities with a submission/listing feature
- ✅ Press outlets that accept startup coverage
- ✅ Marketplaces for software/apps

### What We Don't Accept
- ❌ Pure link farms or spam directories
- ❌ Directories that are permanently offline
- ❌ Personal blogs without a directory feature
- ❌ Paid-only directories with no free option (unless high DR)
- ❌ Duplicate entries

### Categories

Use one of these standard categories:

| Emoji + Category | When to Use |
|-----------------|-------------|
| 🚀 Startup Directory | General product/startup listing sites |
| ⭐️ Review Directory | Software review & comparison platforms |
| 🤖 AI Directory | AI/ML tools directories |
| 👥 Community | Forums, maker communities |
| 🗞 Press Coverage | Tech news, media outlets |
| 📂 General Directory | Web/link directories |
| 🧩 SaaS Marketplace | App stores, marketplaces |
| 🤝 API Marketplace | API listing platforms |
| 🌍 International | Non-English directories |
| 💫 Other | Doesn't fit other categories |

### Domain Rating

- Use Ahrefs Domain Rating (DR) when available
- If you don't have access to Ahrefs, leave `domain_rating` as `null`
- Don't use Moz DA or other metrics — we standardize on Ahrefs DR

### Code Style

- JSON should be properly formatted with 2-space indentation
- URLs should not have trailing slashes
- Names should use title case

## Pull Request Process

1. Ensure your JSON is valid (use a JSON validator)
2. Keep entries sorted: DR entries first (highest to lowest), then null-DR entries alphabetically
3. Write a clear PR description explaining what you added/changed
4. One PR per batch of changes (don't mix additions with corrections)

## Questions?

Open an issue with the `question` label and we'll get back to you!

---

Thank you for making this list better! 🎉
