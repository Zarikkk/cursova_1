const buttons = document.querySelectorAll('.buttonLed');
const realTimeButton = document.querySelector(".realTime");
const createAlgorithm = document.querySelector(".createAlgorithm");

function send(id) {
    const btn = document.getElementById(id);
    if (btn.className === 'buttonInput') {
        if (btn.id === 'clear') {
            sendCommandToServer(id)
        } else if (btn.id === 'send') {
            sendCommandToServer(document.getElementById("textInput").value)
        }
    }
}


function sendCommandToServer(command) {
    fetch("http://127.0.0.1:5000/sendText", {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(command)
    }).then(function (response) {
        if (response.status !== 200) {
            console.log('Error');
        } else window.location.reload()
    })

}

const itemsList = document.getElementById("items_list");

let items = []

const itemTemplate = ({ id, text }) => `
    <li>
        <div>
            <p>${text}</p>
        </div>
    </li>
`

const refetchAllItems = () => {
    getExamples();
}

const renderItemsList = (items) => {
    itemsList.innerHTML = "";
    for (const item of items) {
        console.log(item)
        addItemToPage(item);
    }
}

const addItemToPage = ({ id, text }) => {
    itemsList.insertAdjacentHTML(
        "afterbegin",
        itemTemplate({ id, text })
    );
};


function getExamples() {
    fetch("http://127.0.0.1:5000/text")
        .then(res => res.json())
        .then(out => renderItemsList(out))
}

refetchAllItems()