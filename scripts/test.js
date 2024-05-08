function convertJson(event) {
    event.preventDefault();

    const data = new FormData(event.target);

    const value = Object.fromEntries(data.entries())

    console.log(value);
}

const form = document.getElementById('former');
form.addEventListener('submit', convertJson)