const form = document.forms.myForm;
const playlistElement = document.getElementById('playlist'); // Add this line

form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    console.log(formData)
    const response = await fetch('http://localhost:5000/api/generate_music', {
        method: 'POST',
        body: formData
    });
    const data = await response.json();
    console.log(data);
    
    playlistElement.innerHTML = '';

    // Add the response data to the playlist element
    for (let i = 0; i < data.length; i++) {
        const group = data[i];
        const groupElement = document.createElement('ul');
        for (let j = 0; j < group.length; j++) {
            const itemElement = document.createElement('li');
            itemElement.innerText = group[j];
            groupElement.appendChild(itemElement);
        }
        playlistElement.appendChild(groupElement);
    }
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
    const artistDropdown = document.getElementById("artist");

    artists.forEach((artist) => {
        const option = document.createElement("option");
        option.value = artist;
        option.text = artist;
        artistDropdown.add(option);
    });
    
    const songs = await fetchSongs();
    const songDropdown = document.getElementById("title");
  
    songs.forEach((song) => {
      const option = document.createElement("option");
      option.value = song;
      option.text = song;
      songDropdown.add(option);
    });
  }
  
document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM loaded")
    populateDropdowns();
});