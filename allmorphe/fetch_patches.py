#!/usr/bin/env python3
"""Fetch and aggregate Morphe patch metadata from bundle repositories."""

import json
import os
import re
import requests
import base64
from datetime import datetime, timezone

# Configuration: GitHub repo URLs for Morphe patch bundles
# Start with the official Morphe Patches, add more from morphe-patches.software
BUNDLE_REPOS = [
    "github.com/MorpheApp/morphe-patches",
    # Add more bundle repo URLs as discovered from morphe-patches.software:
    # "github.com/username/patches-repo",
    # "github.com/another-user/bundle-name",
]


def fetch_bundle_metadata(github_url):
    """Fetch patches-bundle.json from a GitHub repository."""
    try:
        match = re.search(r"github\.com/(.+)/(.+)", github_url)
        if not match:
            return None
        
        owner, repo_name = match.groups()
        api_url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/patches-bundle.json"
        headers = {"Accept": "application/vnd.github.v3+json"}
        
        resp = requests.get(api_url, headers=headers, timeout=30)
        
        if resp.status_code == 200:
            content = base64.b64decode(resp.json()["content"]).decode("utf-8")
            bundle_data = json.loads(content)
            
            metadata = {
                "version": bundle_data.get("version", "unknown"),
                
                "public_key": bundle_data.get("public_key", ""),
                "created_at": bundle_data.get("created_at", ""),
                "source_repo": github_url,
                "repo_name": repo_name,
            }
            
            # Calculate age since creation
            if "created_at" in bundle_data:
                try:
                    created_date = datetime.fromisoformat(bundle_data["created_at"].replace("Z", "+00:00"))
                    now = datetime.now(timezone.utc)
                    metadata["age_days"] = max(1, (now - created_date).days)
                except:
                    metadata["age_days"] = 0
            
            return metadata
        elif resp.status_code == 404:
            print(f"No patches-bundle.json in {github_url}")
            return None
        else:
            print(f"GitHub API returned {resp.status_code} for {github_url}")
            return None
    except Exception as e:
        print(f"Failed to process {github_url}: {e}")
        return None


def main():
    print(f"📋 Processing {len(BUNDLE_REPOS)} bundle repositories...", flush=True)
    
    all_metadata = []
    processed_repos = set()
    
    for github_url in BUNDLE_REPOS:
        if not github_url:
            continue
        
        metadata = fetch_bundle_metadata(github_url)
        if metadata:
            processed_repos.add(github_url)
            all_metadata.append(metadata)
            print(f"  ✅ {metadata['version']} - {metadata['repo_name']}", flush=True)
    
    # Sort by creation date (newest first)
    all_metadata.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    
    # Determine combined version (newest patch version)
    combined_version = "1.0.0"
    if all_metadata:
        combined_version = all_metadata[0].get("version", "1.0.0")
    
    # Create the combined patches-bundle.json
    combined = {
        "name": "AllMorphe Patches",
        "version": combined_version,
        "description": f"Aggregated patch metadata from {len(all_metadata)} bundles "
                       f"from morphe-patches.software. "
                       f"Total bundles: {len(processed_repos)}.",
        "patches_metadata": all_metadata,
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "morphe-patches.software",
        "totalBundles": len(processed_repos),
        "totalPatches": len(all_metadata),
        "format": "morphe-patch-metadata-v1"
    }
    
    # Write to the allmorphe folder relative to the script
    # __file__ is /workspace/.../allmorphe/fetch_patches.py
    script_dir = os.path.dirname(os.path.abspath(__file__))  # /workspace/.../allmorphe
    output_path = os.path.join(script_dir, "patches-bundle.json")  # /workspace/.../allmorphe/patches-bundle.json
    with open(output_path, "w") as f:
        json.dump(combined, f, indent=2)
    
    print(f"\n📝 Generated: patches-bundle.json")
    print(f"   Version: {combined['version']}")
    print(f"   Total bundles: {combined['totalBundles']}")
    print(f"   Total patches metadata: {combined['totalPatches']}")
    print(f"   Format: {combined['format']}")


if __name__ == "__main__":
    main()