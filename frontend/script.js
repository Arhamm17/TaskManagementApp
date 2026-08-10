async function loadTasks() {
    const response = await fetch("/api/tasks");
    const tasks = await response.json();

    const container = document.getElementById("tasks");
    container.innerHTML = "";

    tasks.forEach(task => {
        const div = document.createElement("div");
        div.className = "task";

        div.innerHTML = `
            <span class="${task.completed ? "completed" : ""}">
                ${task.title}
            </span>

            <div>
                <button onclick="toggleTask(${task.id}, ${!task.completed})">
                    ${task.completed ? "Undo" : "Done"}
                </button>

                <button onclick="deleteTask(${task.id})">
                    Delete
                </button>
            </div>
        `;

        container.appendChild(div);
    });
}


async function addTask() {
    const input = document.getElementById("taskInput");
    const title = input.value.trim();

    if (!title) {
        return;
    }

    await fetch("/api/tasks", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title: title
        })
    });

    input.value = "";

    loadTasks();
}


async function toggleTask(id, completed) {
    await fetch(`/api/tasks/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            completed: completed
        })
    });

    loadTasks();
}


async function deleteTask(id) {
    await fetch(`/api/tasks/${id}`, {
        method: "DELETE"
    });

    loadTasks();
}


loadTasks();
