"""
YouTube Transcript Fetcher
Topic: AI-Powered SEO Content Production
Usage: python fetch_transcripts.py
"""

import os
import re
import json
from youtube_transcript_api import YouTubeTranscriptApi

# ============================================================
# DAFTAR VIDEO DARI PARA EXPERT
# Ganti/tambah video_id sesuai video terbaru mereka
# video_id = bagian setelah ?v= di URL YouTube
# Contoh: https://www.youtube.com/watch?v=dQw4w9WgXcQ -> id = dQw4w9WgXcQ
# ============================================================

VIDEOS = [
    {
        "expert": "koray-tugberk",
        "title": "Topical Authority for AI SaaS",
        "video_id": "FAJonNdKqw0",
        "url": "https://www.youtube.com/@HolisticSEODigital"
    },
    {
        "expert": "kevin-indig",
        "title": "Google Will Kill Your Traffic - Here's How You Adapt ",
        "video_id": "jQXvbeYF5go",
        "url": "https://www.youtube.com/@ahrefspodcast"
    },
    {
        "expert": "lily-ray",
        "title": "Google's 2026 Crackdown: Lily Ray Says Your SEO Strategy is Failing",
        "video_id": "-pUMNtq8Bp0",
        "url": "https://www.youtube.com/@SterlingSkyInc"
    },
    {
        "expert": "cyrus-shepard",
        "title": "Link Building in 2025: First 10 Links, Linkable Assets & HCU Wins",
        "video_id": "TPEkoQnwErc",
        "url": "https://www.youtube.com/@buildinpublic"
    },
    {
        "expert": "kyle-roof",
        "title": "Kyle Roof DEEP Interview [His BEST SEO Tactics]",
        "video_id": "frxMhxQXJLc",
        "url": "https://www.youtube.com/@MattDiggity"
    },
    {
        "expert": "ryan-law",
        "title": "How to Win in AI Search (Real Data, No Hype)",
        "video_id": "mL1W1SMtTT4",
        "url": "https://www.youtube.com/@ahrefspodcast"
    },
    {
        "expert": "britney-muller",
        "title": "The Future of AI in Search | Whiteboard Friday Revisited | Britney Muller",
        "video_id": "N2fb2b_hSOU",
        "url": "https://www.youtube.com/@Moz"
    },
    {
        "expert": "michal-suski",
        "title": "Learn on-page SEO with Michal Suski!",
        "video_id": "wcgvstd8yLE",
        "url": "https://www.youtube.com/@SurferSEO"
    },
    {
        "expert": "nathan-gotch",
        "title": "How to ACTUALLY Learn AI SEO (in 2026)",
        "video_id": "HzgMpTVJpz0",
        "url": "https://www.youtube.com/@nathangotch"
    },
]


# ============================================================
# OUTPUT FOLDER
# ============================================================
OUTPUT_BASE = "research/youtube-transcripts"


def sanitize_filename(name):
    return re.sub(r'[^a-z0-9\-_]', '-', name.lower())


def fetch_transcript(video_id):
    try:
        ytt = YouTubeTranscriptApi()
        transcript = ytt.fetch(video_id)
        return list(transcript)
    except Exception as e:
        print(f"  [ERROR] Gagal ambil transkrip: {e}")
        return None


def transcript_to_text(transcript):
    lines = []
    for entry in transcript:
        start = entry.start
        text = entry.text.strip()
        minutes = int(start // 60)
        seconds = int(start % 60)
        lines.append(f"[{minutes:02d}:{seconds:02d}] {text}")
    return "\n".join(lines)

def save_transcript(expert, title, video_id, url, transcript):
    folder = os.path.join(OUTPUT_BASE, expert)
    os.makedirs(folder, exist_ok=True)

    safe_title = sanitize_filename(title)
    filepath = os.path.join(folder, f"{safe_title}.md")

    full_text = transcript_to_text(transcript)

    content = f"""# {title}

**Expert:** {expert}  
**Video ID:** {video_id}  
**URL:** https://www.youtube.com/watch?v={video_id}  
**Channel:** {url}  
**Fetched:** Auto-fetched via youtube-transcript-api  

---

## Transcript

{full_text}
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  [OK] Disimpan: {filepath}")
    return filepath


def main():
    print("=" * 60)
    print("YouTube Transcript Fetcher")
    print("Topic: AI-Powered SEO Content Production")
    print("=" * 60)

    # Cek apakah ada video_id yang belum diisi
    unfilled = [v for v in VIDEOS if v["video_id"] == "GANTI_DENGAN_VIDEO_ID"]
    if unfilled:
        print(f"\n[WARNING] {len(unfilled)} video belum diisi video_id-nya:")
        for v in unfilled:
            print(f"  - {v['expert']}: {v['title']}")
        print("\nCara cari video_id:")
        print("  1. Buka YouTube, cari video dari expert")
        print("  2. Copy URL-nya, ambil bagian setelah ?v=")
        print("  3. Paste ke bagian VIDEOS di atas\n")

    # Proses video yang sudah ada video_id-nya
    filled = [v for v in VIDEOS if v["video_id"] != "GANTI_DENGAN_VIDEO_ID"]

    if not filled:
        print("[INFO] Belum ada video_id yang diisi. Isi dulu video_id di script ini.")
        return

    print(f"\nMemproses {len(filled)} video...\n")

    results = []
    for video in filled:
        print(f"-> {video['expert']}: {video['title']}")
        transcript = fetch_transcript(video["video_id"])
        if transcript:
            path = save_transcript(
                video["expert"],
                video["title"],
                video["video_id"],
                video["url"],
                transcript
            )
            results.append({"status": "ok", "path": path, **video})
        else:
            results.append({"status": "error", **video})

    print("\n" + "=" * 60)
    print(f"Selesai! {sum(1 for r in results if r['status'] == 'ok')}/{len(filled)} berhasil")
    print("=" * 60)


if __name__ == "__main__":
    main()