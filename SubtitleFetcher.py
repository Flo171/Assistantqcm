from fastapi import FastAPI, HTTPException, Query
from pytube import YouTube
from typing import List, Optional

app = FastAPI(
    title="YouTube Subtitles API",
    description="API pour récupérer les sous-titres d'une vidéo YouTube.",
    version="1.0.0"
)

@app.get("/subtitles", summary="Récupère les sous-titres d'une vidéo YouTube.")
async def get_subtitles(videoId: str = Query(..., description="L'ID de la vidéo YouTube.", example="dQw4w9WgXcQ"),
                        language: Optional[str] = Query("en", description="Le code de la langue des sous-titres (par exemple, 'en' pour anglais).", example="en")):
    try:
        yt = YouTube(f'https://www.youtube.com/watch?v={videoId}')
        caption = yt.captions.get_by_language_code(language)
        
        if not caption:
            raise HTTPException(status_code=404, detail="Subtitles not found for the specified videoId")
        
        subtitle = caption.generate_srt_captions()
        subtitles = []

        for line in subtitle.split('\n\n'):
            if line:
                parts = line.split('\n')
                times = parts[1].split(' --> ')
                subtitles.append({
                    "startTime": times[0],
                    "endTime": times[1],
                    "text": " ".join(parts[2:])
                })

        return {
            "videoId": videoId,
            "language": language,
            "subtitles": subtitles
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
