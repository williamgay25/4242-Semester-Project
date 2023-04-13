from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

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
    print(form_data)
    return {"message": "Music generated successfully"}

@app.get("/api/artist")
def get_artist():
    return {"message": "Artist name"}

@app.get("/api/song_title")
def get_song_title():
    return {"message": "Song title"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=5000, log_level="info")
