const form = document.forms.myForm;

form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    console.log(formData)
    const response = await fetch('http://localhost:5000/api/generate_music', {
        method: 'POST',
        body: formData
    });
    const data = await response.json();
    console.log(data)
    // Do something with the response data
});
