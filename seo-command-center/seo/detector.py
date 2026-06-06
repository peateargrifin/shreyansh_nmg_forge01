"""
detector.py — deterministic SEO issue detection from a Screaming Frog internal_all.csv.
Coded with pandas for efficiency and robust NaN handling.
"""

from __future__ import annotations
import pandas as pd
import os
import sys
import json
from collections import defaultdict

def load_rows(export_dir: str) -> pd.DataFrame:
    path = os.path.join(export_dir, "internal_all.csv")
    # utf-8-sig handles UTF-8 with BOM
    df = pd.read_csv(path, encoding="utf-8-sig")
    # Replace NaN with empty strings for consistent processing
    df = df.fillna('')
    return df

def detect(df: pd.DataFrame) -> list[dict]:
    """
    Deterministic SEO issue detection based on the rulebook.
    Returns a list of issue dicts: {type, severity, affected_urls, count, explanation}.
    """
    issues = []

    def add_issue(issue_type, severity, urls, explanation):
        urls = sorted(list(set(urls)))
        if urls:
            issues.append({
                "type": issue_type,
                "severity": severity,
                "affected_urls": urls,
                "count": len(urls),
                "explanation": explanation
            })

    # --- Pre-filtering ---
    # HTML rows (for most checks)
    df_html = df[df['Content Type'].str.contains('text/html', case=False, na=False)]

    # Indexable 200 pages (for title/meta/orphan checks)
    df_idx200 = df_html[
        (df_html['Status Code'].astype(str) == '200') &
        (df_html['Indexability'].str.lower() == 'indexable')
    ]

    # Image rows (for alt text check)
    df_images = df[df['Content Type'].str.contains('image/', case=False, na=False)]

    # --- 1. Titles ---
    # Missing Title (Indexable 200)
    missing_title_urls = df_idx200[df_idx200['Title 1'].str.strip() == '']['Address'].tolist()
    add_issue("missing_title", "High", missing_title_urls, "Indexable pages with no title tag.")

    # Duplicate Titles (Indexable)
    # We check indexable pages generally for duplicates, as per rulebook
    df_idx = df_html[df_html['Indexability'].str.lower() == 'indexable']
    titles = df_idx['Title 1'].str.strip()
    duplicates = titles[titles.duplicated()].index
    dup_title_urls = df_idx.loc[duplicates, 'Address'].tolist()
    # Note: This identifies any page that has a title already seen.
    # To get all pages sharing a title (including the first one):
    title_counts = titles.value_counts()
    dup_titles = title_counts[title_counts > 1].index
    all_dup_title_urls = df_idx[df_idx['Title 1'].str.strip().isin(dup_titles) & (df_idx['Title 1'].str.strip() != '')]['Address'].tolist()
    add_issue("duplicate_title", "High", all_dup_title_urls, "Pages sharing an identical title.")

    # Title too long (> 561px or > 60 chars)
    # Using .astype(float).fillna(0) to handle numeric conversion safely
    too_long_urls = df_idx200[
        (pd.to_numeric(df_idx200['Title 1 Pixel Width'], errors='coerce').fillna(0) > 561) |
        (pd.to_numeric(df_idx200['Title 1 Length'], errors='coerce').fillna(0) > 60)
    ]['Address'].tolist()
    add_issue("title_too_long", "Medium", too_long_urls, "Titles likely truncated in search results.")

    # Title too short (< 30 chars and not empty)
    too_short_urls = df_idx200[
        (pd.to_numeric(df_idx200['Title 1 Length'], errors='coerce').fillna(0) < 30) &
        (df_idx200['Title 1'].str.strip() != '')
    ]['Address'].tolist()
    add_issue("title_too_short", "Low", too_short_urls, "Titles that are too short to be descriptive.")

    # --- 2. Meta Descriptions ---
    # Missing Meta Description (Indexable 200)
    missing_meta_urls = df_idx200[df_idx200['Meta Description 1'].str.strip() == '']['Address'].tolist()
    add_issue("missing_meta_description", "Medium", missing_meta_urls, "Indexable pages with no meta description.")

    # Duplicate Meta Descriptions (Indexable)
    meta_descriptions = df_idx['Meta Description 1'].str.strip()
    meta_counts = meta_descriptions.value_counts()
    dup_meta_vals = meta_counts[meta_counts > 1].index
    dup_meta_urls = df_idx[df_idx['Meta Description 1'].str.strip().isin(dup_meta_vals) & (df_idx['Meta Description 1'].str.strip() != '')]['Address'].tolist()
    add_issue("duplicate_meta_description", "Medium", dup_meta_urls, "Pages sharing an identical meta description.")

    # Meta too long (> 155 chars)
    meta_too_long_urls = df_idx200[
        pd.to_numeric(df_idx200['Meta Description 1 Length'], errors='coerce').fillna(0) > 155
    ]['Address'].tolist()
    add_issue("meta_description_too_long", "Low", meta_too_long_urls, "Meta descriptions likely truncated in search results.")

    # --- 3. H1s ---
    # Missing H1 (200 page)
    missing_h1_urls = df_html[
        (df_html['Status Code'].astype(str) == '200') &
        (df_html['H1-1'].str.strip() == '')
    ]['Address'].tolist()
    add_issue("missing_h1", "Medium", missing_h1_urls, "Pages missing an H1 tag.")

    # Duplicate H1s (Indexable)
    h1s = df_idx['H1-1'].str.strip()
    h1_counts = h1s.value_counts()
    dup_h1_vals = h1_counts[h1_counts > 1].index
    dup_h1_urls = df_idx[df_idx['H1-1'].str.strip().isin(dup_h1_vals) & (df_idx['H1-1'].str.strip() != '')]['Address'].tolist()
    add_issue("duplicate_h1", "Low", dup_h1_urls, "Pages sharing an identical H1 tag.")

    # Multiple H1s (Prompt asked for "Multiple/Duplicate H1s")
    # Note: Screaming Frog usually only reports H1-1. If there's an H1-2 column, we check it.
    if 'H1-2' in df.columns:
        multiple_h1_urls = df_html[df_html['H1-2'].str.strip() != '']['Address'].tolist()
        add_issue("multiple_h1", "Low", multiple_h1_urls, "Pages with more than one H1 tag.")

    # --- 4. Status Codes ---
    status_codes = pd.to_numeric(df['Status Code'], errors='coerce').fillna(0)

    # Broken links (4xx)
    broken_urls = df[(status_codes >= 400) & (status_codes <= 499)]['Address'].tolist()
    add_issue("broken_link", "High", broken_urls, "URLs returning a client error (4xx).")

    # Server errors (5xx)
    server_error_urls = df[(status_codes >= 500) & (status_codes <= 599)]['Address'].tolist()
    add_issue("server_error", "High", server_error_urls, "URLs returning a server error (5xx).")

    # Redirects (3xx)
    redirect_urls = df[(status_codes >= 300) & (status_codes <= 399)]['Address'].tolist()
    add_issue("redirect", "Medium", redirect_urls, "URLs that redirect (3xx).")

    # --- 5. Image Alt Text ---
    # Missing alt text (for image rows)
    # Usually the column is 'Alt Text'
    alt_col = 'Alt Text' if 'Alt Text' in df.columns else 'Alt Text 1'
    if alt_col in df.columns:
        missing_alt_urls = df_images[df_images[alt_col].str.strip() == '']['Address'].tolist()
        add_issue("missing_image_alt_text", "Low", missing_alt_urls, "Images missing alt text.")
    else:
        # Log this if we can't find the column
        pass

    # --- 6. Content & Links ---
    # Thin content (Word Count < 200 on indexable HTML)
    thin_content_urls = df_idx[
        pd.to_numeric(df_idx['Word Count'], errors='coerce').fillna(0) < 200
    ]['Address'].tolist()
    add_issue("thin_content", "Low", thin_content_urls, "Pages with very low word count.")

    # Orphan pages (Inlinks = 0 on indexable 200)
    orphan_urls = df_idx200[
        pd.to_numeric(df_idx200['Inlinks'], errors='coerce').fillna(0) == 0
    ]['Address'].tolist()
    add_issue("orphan_page", "Medium", orphan_urls, "Indexable pages with zero internal links.")

    return issues

def summarize(issues: list[dict]) -> dict:
    by_sev = defaultdict(int)
    for i in issues:
        by_sev[i["severity"]] += i["count"] # Total affected URLs, not issue types
    return {"total_issue_types": len(issues),
            "total_affected_urls": sum(i["count"] for i in issues),
            "by_severity": {"High": by_sev["High"], "Medium": by_sev["Medium"], "Low": by_sev["Low"]}}

if __name__ == "__main__":
    # Using the relative path provided in the prompt
    export_path = "../sample-export" if len(sys.argv) < 2 else sys.argv[1]

    # Adjusted path for when running from inside seo-command-center/
    # The prompt says "run the script against ../sample-export/internal_all.csv"
    # If we run from the root, we might need to be careful.

    try:
        df = load_rows(export_path)
        iss = detect(df)
        print(f"Loaded {len(df)} rows, detected {len(iss)} issue types.")
        print(json.dumps(summarize(iss), indent=2))
        for i in iss:
            print(f"  [{i['severity']:<6}] {i['type']:<24} x{i['count']}")
    except Exception as e:
        print(f"Error during execution: {e}")
        sys.exit(1)
