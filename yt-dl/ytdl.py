import yt_dlp

url = input("Enter url:")
ydl_opts = {}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
print("your video has downloded")
            
