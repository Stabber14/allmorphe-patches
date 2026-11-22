# AllMorphe

A project that aggregates **all Morphe patches** from [morphe-patches.software](https://morphe-patches.software/) into a single, easily installable patch source for the Morphe Android app.

## What is AllMorphe?

AllMorphe collects all 327 patch bundles (6,451 patches across 1,114 apps) from the morphe-patches.website community site and provides them as a single Morphe patch source that:

- **Installs all at once** with a single source addition
- **Auto-updates** when creators update their patches (Morphe fetches updates from the repository automatically)
- **Works with any Android device** running Morphe

## Installation

### Option 1: Add via GitHub repository (recommended)

Add this repository URL to Morphe's patch sources:

```
github.com/your-username/allmorphe-patches
```

*(Note: You'll need to host the repository yourself, or use the provided setup script below)*

### Option 2: Add via deep link (no hosting required)

Tap this link to add all patches directly in Morphe:

[morphe.software/add-source?github=MorpheApp%2Fmorphe-patches](morphe.software/add-source?github=MorpheApp%2Fmorphe-patches)

*This adds the official Morphe Patches source only. For all bundles from morphe-patches.software, use Option 1.*

### Option 3: Manual JSON metadata link

If you have a direct link to the patches bundle JSON metadata, add it in Morphe:
```
https://morphe-patches.software/patches-bundle.json
```

*(Verify this URL format with the morphe-patches.website site)*

## Project Structure

```
allmorphe/
├── README.md           # This file
├── patches-bundle.json # Combined patch metadata (generated)
├── scripts/
│   └── update.sh     # Update script for auto-updating patches
└── .github/
    └── workflows/
        └── update.yml # GitHub Actions for automatic updates
```

## How It Works

1. **Patch sources**: Each bundle from morphe-patches.software is a GitHub repository containing .mpp patch files and a `patches-bundle.json` metadata file
2. **Aggregation**: AllMorphe combines metadata from all bundles into a single index
3. **Morphe integration**: When added as a GitHub repository source, Morphe automatically:
   - Fetches available patches
   - Shows patch versions (Latest, Stable, Dev)
   - Keeps the source updated when creators push new versions
   - Lets you select which patches to apply per app

## Auto-Update Setup

To have patches update automatically when creators update them:

1. Host this repository on GitHub
2. The included GitHub Actions workflow (`.github/workflows/update.yml`) will:
   - Fetch the latest patches from morphe-patches.software
   - Update the `patches-bundle.json` metadata
   - Commit and push changes automatically
3. Morphe will detect the new version and offer updates

## License

MIT License - feel free to use, modify, and distribute.

## Related

- [Morphe Patches (official)](https://morphe.software/) - The official Morphe patch source
- [morphe-patches on GitHub](https://github.com/MorpheApp/morphe-patches) - The official patches repository
- [morphe-patches.software](https://morphe-patches.software/) - Community patches website