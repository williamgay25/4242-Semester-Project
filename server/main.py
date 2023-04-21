from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from api import artists, songs, cluster
from pydantic import BaseModel, validator
from typing import Optional

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
    playlistSize: Optional[str]
    artistName: Optional[str]
    songTitle: Optional[str]
    playlistYear: Optional[int]

    @validator('playlistYear', pre=True, always=True)
    def default_year(cls, value):
        return value

@app.post("/api/generate_music")
async def generate_music(
    playlist_data: PlaylistData
):
    form_data = {}

    print(playlist_data)

    if playlist_data.playlistSize:
        form_data["length"] = playlist_data.playlistSize
    if playlist_data.artistName:
        form_data["artist"] = playlist_data.artistName
    if playlist_data.songTitle:
        form_data["seed_song"] = playlist_data.songTitle
    if playlist_data.playlistYear:
        form_data["year"] = playlist_data.playlistYear

    print(form_data)
        
    resp = cluster.cluster(**form_data)

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
