const mazeContainer = document.getElementById("maze-container");
const BASE_URL = "http://127.0.0.1:8000";  // Django backend URL

let currentMaze = [];  // Store generated maze
let timerInterval;

function generateMaze() {
    const size = parseInt(document.getElementById("difficulty").value);
    fetch(`${BASE_URL}/generate/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ size })
    })
    .then(response => response.json())
    .then(data => {
        currentMaze = data.maze;
        drawMaze(currentMaze);
    })
    .catch(error => console.error("Error generating maze:", error));
}

function drawMaze(grid) {
    const size = grid.length;
    mazeContainer.innerHTML = "";
    mazeContainer.style.display = "grid";
    mazeContainer.style.gridTemplateColumns = `repeat(${size}, 32px)`;
    
    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            const cell = document.createElement("div");
            cell.classList.add("cell");
            if (grid[i][j] === 1) cell.classList.add("wall");
            mazeContainer.appendChild(cell);
        }
    }
    
    // Highlight start and end points
    mazeContainer.children[0].classList.add("start");
    mazeContainer.children[size * size - 1].classList.add("end");
    
    mazeContainer.dataset.gridSize = size;
}

function solveMaze() {
    const algorithm = document.getElementById("algorithm").value;
    if (currentMaze.length === 0) {
        alert("Please generate a maze first.");
        return;
    }

    clearPreviousPath(); // Clear previous path before solving


    fetch(`${BASE_URL}/solve/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ maze: currentMaze, algorithm })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.error); });
        }
        return response.json();
    })
    .then(data => {
        animateSolution(data.steps, data.shortest_path);
    })
    .catch(error => {
        console.error("Error solving maze:", error);
        alert("Error: " + error.message);
    });
}

function clearPreviousPath() {
    const cells = mazeContainer.children;
    for (let cell of cells) {
        cell.classList.remove("solution", "shortest-path");
    }
}


function animateSolution(steps, shortestPath) {
    if (!steps || steps.length === 0) {
        console.error("No solution steps received.");
        alert("No solution found. Try regenerating the maze.");
        return;
    }

    let index = 0;
    const cells = mazeContainer.children;
    const gridSize = parseInt(mazeContainer.dataset.gridSize);

    const interval = setInterval(() => {
        if (index >= steps.length) {
            clearInterval(interval);
            setTimeout(() => highlightShortestPath(shortestPath), 500); // Delay highlighting shortest path
            return;
        }

        const [x, y] = steps[index];
        const pos = x * gridSize + y;

        if (cells[pos]) {
            cells[pos].classList.add("solution");
        } else {
            console.error(`Invalid cell position: (${x}, ${y}) -> ${pos}`);
            clearInterval(interval);
        }

        index++;
    }, 30);
}

function highlightShortestPath(shortestPath) {
    if (!shortestPath || shortestPath.length === 0) return;
    
    const cells = mazeContainer.children;
    const gridSize = parseInt(mazeContainer.dataset.gridSize);

    shortestPath.forEach(([x, y]) => {
        const pos = x * gridSize + y;
        if (cells[pos]) {
            cells[pos].classList.add("shortest-path");
        }
    });
}