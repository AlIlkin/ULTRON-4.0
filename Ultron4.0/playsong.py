import urllib.parse
import webbrowser
import yt_dlp

from ultron_bootstrap import ANSI_RED, ANSI_RESET


def play_song(command):
    song = command.replace("watch", "").replace("play", "").replace("sing the song", "").replace("sing", "").strip()
    
    if song:
        print(f"\n{ANSI_RED}[Ultron]{ANSI_RESET}: Searching and playing '{song}' on YouTube...")
        try:
            search_keyword = f"ytsearch1:{song}"
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(search_keyword, download=False)
                if 'entries' in info and len(info['entries']) > 0:
                    video_id = info['entries'][0]['id']
                    # Construct the standard watch link that auto-plays
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    webbrowser.open(video_url)
                    return True
                       
        except Exception as e:
            print(f"{ANSI_RED}[Ultron Error]{ANSI_RESET}: Direct play failed, falling back to search page: {e}")
            
        encoded_query = urllib.parse.quote(song)
        webbrowser.open(f"https://www.youtube.com/results?search_query={encoded_query}")
        return True
    else:
        print("\n[Ultron] What song would you like me to play?")
        return False