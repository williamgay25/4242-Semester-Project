const form = document.forms.myForm;

form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData(form);

    console.log("Form data")
    console.log(formData)

    const data = {
        playlistSize: formData.get('duration'),
        artistName: formData.get('artist'),
        songTitle: formData.get('song'),
        playlistYear: parseInt(formData.get('period').slice(0, -1), 10),
    };

    console.log("Data")
    console.log(data)
    
    const response = await fetch('http://localhost:5000/api/generate_music', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    const responseData = await response.json();

    console.log("Response data");
    console.log(responseData);

    if (response.status === 422) {
        console.error("Validation errors:", responseData.detail);
    }

    // Save data to local storage
    localStorage.setItem('playlistData', JSON.stringify(responseData));

    // Redirect to the output page
    // window.location.href = 'output.html';
});

async function fetchArtists() {
    const response = await fetch("http://localhost:5000/api/artists");
    const data = await response.json();
    return data;
  }
  
async function fetchSongs() {
    const response = await fetch("http://localhost:5000/api/songs");
    const data = await response.json();
    return data;
}
  
async function populateDropdowns() {
    const artists = await fetchArtists();
    const artistDropdown = document.getElementById("artists");
    

    artists.forEach((artist) => {
        const option = document.createElement("option");
        option.value = artist;
        option.text = artist;
        artistDropdown.appendChild(option);
    });
    
    const songs = await fetchSongs();
    const songDropdown = document.getElementById("songs");
  
    songs.forEach((song) => {
      const option = document.createElement("option");
      option.value = song;
      option.text = song;
      songDropdown.appendChild(option);
    });
  }
  
document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM loaded")
    populateDropdowns();
});