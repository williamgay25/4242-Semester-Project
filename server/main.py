from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import artists, songs, clustering

app = FastAPI()

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/generate_music")
async def generate_music(
    playlistSize: int = Form(...),
    artistName: str = Form(...),
    songTitle: str = Form(...)
):
    form_data = {
        "playlistSize": playlistSize,
        "artistName": artistName,
        "songTitle": songTitle
    }
    
    resp = clustering.cluster(form_data)

    return resp

@app.get("/api/artist")
def get_artist():
    return artists.get_artists()

@app.get("/api/song_title")
def get_song_title():
    return songs.get_songs()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=5000, log_level="info")
