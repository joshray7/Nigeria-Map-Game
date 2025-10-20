let states = [];
let guessed = [];
let score = 0;
let totalTime = 7 * 60; // 7 minutes

// Fetch state data
fetch("/states")
  .then(res => res.json())
  .then(data => states = data);

const timerElement = document.getElementById("timer");
const scoreElement = document.getElementById("score");
const input = document.getElementById("guessInput");
const submitBtn = document.getElementById("submitBtn");
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const map = document.getElementById("map");

// Ensure the canvas size matches the map
map.onload = () => {
    canvas.width = map.width;
    canvas.height = map.height;
};

ctx.fillStyle = "red";
ctx.font = "3px Arial";
ctx.fillText("TEST", 200, 200);


// Update timer every second
let countdown = setInterval(() => {
    if (totalTime <= 0) {
        clearInterval(countdown);
        alert("⏰ Time’s up! Final score: " + score);
        return;
    }
    totalTime--;
    const minutes = Math.floor(totalTime / 60);
    const seconds = totalTime % 60;
    timerElement.textContent = `Time: ${minutes}:${seconds.toString().padStart(2, '0')}`;
}, 1000);


submitBtn.addEventListener("click", () => {
    const guess = input.value.trim().toLowerCase();
    const match = states.find(s => s.state.toLowerCase() === guess);

    if (match && !guessed.includes(match.state)) {
        guessed.push(match.state);
        score++;
        scoreElement.textContent = `Score: ${score}`;

        // Draw state name
        ctx.font = "12px Arial";
        ctx.fillStyle = "green";
        ctx.fillText(match.state, match.x, match.y);
    }

    input.value = "";

    if (guessed.length === states.length) {
        clearInterval(countdown);
        alert("🎉 You named all 36 states!");
    }
});
