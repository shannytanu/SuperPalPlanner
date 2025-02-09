const API_URL = "https://superpalplanner.onrender.com"; 

async function fetchGoals(user) {
    let selectedDay = document.getElementById(`day-selector-${user}`).value;
    let response = await fetch(`${API_URL}/get-goals/${user}/${selectedDay}`);
    let data = await response.json();
    let goalsDiv = document.getElementById(`${user}-goals`);
    goalsDiv.innerHTML = "";

    data.goals.forEach(goal => {
        let goalItem = document.createElement("div");
        goalItem.innerHTML = `
            <p ${goal.completed ? 'style="text-decoration: line-through;"' : ''}>
                ${goal.goal} ${goal.completed ? "🔥" : ""}
                <button onclick="completeGoal(${goal.id})">✅</button>
                <button onclick="deleteGoal(${goal.id})">❌</button>
            </p>
        `;
        goalsDiv.appendChild(goalItem);
    });
}

async function addGoal(user) {
    let input = document.getElementById(`${user}-input`);
    let goalText = input.value;
    let selectedDay = document.getElementById(`day-selector-${user}`).value;

    if (!goalText) return;

    await fetch(`${API_URL}/add-goal`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user, day: selectedDay, goal: goalText, completed: false })
    });

    input.value = "";
    fetchGoals(user);
}

async function completeGoal(goalId) {
    await fetch(`${API_URL}/update-goal/${goalId}`, { method: "PUT" });
    fetchGoals("shantanu");
    fetchGoals("gauri");
}

async function deleteGoal(goalId) {
    await fetch(`${API_URL}/delete-goal/${goalId}`, { method: "DELETE" });
    fetchGoals("shantanu");
    fetchGoals("gauri");
}

// Load goals on page load
document.addEventListener("DOMContentLoaded", () => {
    fetchGoals("shantanu");
    fetchGoals("gauri");

    document.getElementById("day-selector-shantanu").addEventListener("change", () => fetchGoals("shantanu"));
    document.getElementById("day-selector-gauri").addEventListener("change", () => fetchGoals("gauri"));
});
