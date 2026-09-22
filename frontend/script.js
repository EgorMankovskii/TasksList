const API_URL = "http://127.0.0.1:8000/items";

async function loadTasks() {
    const filterValue = document.getElementById("status-task").value;
    const URL = filterValue !== "" ? `${API_URL}?completed=${filterValue}` : API_URL;
    const response = await fetch(URL);
    const tasks = await response.json();
    const list = document.getElementById("taskList")
    list.innerHTML = ""
    tasks.forEach(task => {
        list.innerHTML += `<li>${task.title}<button onclick="updateTaskStatus(${task.id})">${task.completed ? "Выполнено" : "Не выполнено"}</button><button onclick="deleteTask(${task.id})">❌</button></li>`
    });
}

async function addTask() {
    const input = document.getElementById("taskTitle");
    await fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title: input.value
        })
    });
    input.value = ""
    loadTasks();
};

async function deleteTask(id) {
    await fetch(`${API_URL}/${id}`, {
        method: "DELETE",
    });
    loadTasks()
};

async function updateTaskStatus(id) {
    await fetch(`${API_URL}/${id}/completed`, {
        method: "PUT"
    });
    loadTasks();
};

loadTasks();
