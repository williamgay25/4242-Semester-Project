from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import artists, songs, cluster

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
    songTitle: str = Form(...),
    playlistYear: int = Form(...),
):
    form_data = {
        "playlistSize": playlistSize,
        "artistName": artistName,
        "songTitle": songTitle,
        "playlistYear": playlistYear,
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
