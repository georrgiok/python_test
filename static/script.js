const app = document.querySelector('#app');

let options = {
  weekday: "long",
  year: "numeric",
  month: "long",
  day: "numeric",
};

const fetchData = async (link) => {
    const response = await fetch(link)
    const data = await response.json()
    return await data
}

const fetchClients = async () => {
    const link = '/clients'
    const data = await fetchData(link)
    return data
}

const fetchPets = async () => {
    const link = '/pets'
    const data = await fetchData(link)
    return data
}

const placeContent = async () => {
    const [clients, animals] = await Promise.all([fetchClients(), fetchPets(),])
    const data = [];
    clients.forEach(client => {
        const pets = animals.filter(animal => animal.client_id === client.client_id)
        data.push({
            ...client,
            pets: [...pets]
        })
    })

    console.log(data)

    const content = data.map(client => {
        return `
<div style="padding-left: 0.5rem; margin-bottom: 1rem">
    <p>${client.first_name} ${client.last_name} ${client.patronymic}</p>
    <p><strong>Date of Birthday: </strong> ${(new Intl.DateTimeFormat('ru-RU', options).format(client.birthday))}</p>
    <p><strong>Document: </strong> ${client.document}</p>
    <div style="padding-left: 1rem">
        <p><strong>Pets:</strong></p>
        ${client.pets.map(pet => {
            return `
            <div>
                <p><strong>Name:</strong> ${pet.name}</p>
                <p><strong>Birthday:</strong> ${new Intl.DateTimeFormat('ru-RU', options).format(pet.birthday)}</p>
            </div>`
                }).join('')}
    </div>
</div>
<hr />`
    })

    console.log(content)

    app.innerHTML = content.join('')
}

document.addEventListener('DOMContentLoaded', () => {
    placeContent();
})