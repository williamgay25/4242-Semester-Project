from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from api import artists, songs, cluster
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PlaylistData(BaseModel):
    playlistSize: int
    artistName: str
    songTitle: str
    playlistYear: int

@app.post("/api/generate_music")
async def generate_music(
    playlist_data: PlaylistData
):
    form_data = {
        "playlistSize": playlist_data.playlistSize,
        "artistName": playlist_data.artistName,
        "songTitle": playlist_data.songTitle,
        "playlistYear": playlist_data.playlistYear,
    }

    resp = cluster.cluster(form_data["songTitle"], form_data["artistName"], form_data["playlistYear"], form_data["playlistSize"])

    return resp

@app.get("/api/artists")
def get_artist():
    return artists.get_artists()

@app.get("/api/songs")
def get_song_title():
    return songs.get_songs()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=5000, log_level="info")
