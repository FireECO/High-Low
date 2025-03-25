let balance = 1000.00;
let lastNumber = null; // null initially
let rollTimer = 10;
let allowBetting = true;
let betHistory = [];
let countdownInterval;

document.addEventListener("DOMContentLoaded", () => {
    updateButtons();
    startRolling(); // Start the first roll sequence
    setInterval(startRolling, 12000); // Ensure proper cycle timing
});

function setMaxBet() {
    document.getElementById("bet-amount").value = balance.toFixed(2);
}

function startCountdown() {
    clearInterval(countdownInterval); // Avoid multiple intervals running
    countdownInterval = setInterval(() => {
        if (rollTimer > 0) {
            rollTimer--;
            document.getElementById("timer").innerText = rollTimer;
        }
    }, 1000);
}

function updateMessage(msg, color = "#00ffcc") {
    const messageBox = document.getElementById("message-box");
    messageBox.innerText = msg;
    messageBox.style.color = color;
}

function updateButtons() {
    const buttonContainer = document.getElementById("button-container");
    document.getElementById("rolling-text").style.display = "block";
    document.getElementById("rolling-text").style.opacity = 0;
    buttonContainer.innerHTML = "";

    if (lastNumber === 0 || lastNumber === 100) {
        addButton("Even 🔵 x2", "even");
        addButton("Odd 🔴 x2", "odd");
    } else {
        let payoutLower = (lastNumber > 0) ? (1 / (lastNumber / 100)).toFixed(2) : "∞";
        let payoutHigher = (lastNumber < 100) ? (1 / ((100 - lastNumber) / 100)).toFixed(2) : "∞";

        addButton(`Lower ⬇ x${payoutLower}`, "l");
        addButton("Equal 🎯 x100", "e");
        addButton(`Higher ⬆ x${payoutHigher}`, "h");
    }
}

function addButton(label, guess) {
    const button = document.createElement("button");
    button.classList.add("bet-btn");
    button.innerText = label;
    button.disabled = !allowBetting;
    button.onclick = () => placeBet(guess);
    document.getElementById("button-container").appendChild(button);
}

function placeBet(choice) {
    if (!allowBetting) {
        updateMessage("⚠ Betting is closed!", "red");
        return;
    }

    let betAmount = parseFloat(document.getElementById("bet-amount").value);
    if (isNaN(betAmount) || betAmount <= 0 || betAmount > balance) {
        updateMessage("⚠ Invalid bet amount!", "red");
        return;
    }

    balance -= betAmount;
    document.getElementById("balance").innerText = balance.toFixed(2);

    let betText;
    if (choice === "l") betText = `${betAmount.toFixed(2)} → ⬇ Lower`;
    else if (choice === "e") betText = `${betAmount.toFixed(2)} → 🎯 Equal`;
    else if (choice === "h") betText = `${betAmount.toFixed(2)} → ⬆ Higher`;
    else if (choice === "even") betText = `${betAmount.toFixed(2)} → 🔵 Even`;
    else if (choice === "odd") betText = `${betAmount.toFixed(2)} → 🔴 Odd`;

    betHistory.push(betText);
    updateBetHistory();

    updateMessage("✅ Bet placed!", "green");
}

function updateBetHistory() {
    let betList = document.getElementById("bet-list");
    betList.innerHTML = "";
    betHistory.forEach(bet => {
        let li = document.createElement("li");
        li.innerText = bet;
        betList.appendChild(li);
    });
}

function startRolling() {
    rollTimer = 10;
    allowBetting = true;
    betHistory = [];
    updateBetHistory();
    updateButtons();
    
    startCountdown(); // Start the countdown at the beginning of the rolling cycle

    setTimeout(() => {
        allowBetting = false;
        updateButtons();
    }, 9000); // Disable betting before roll

    setTimeout(() => {
        document.getElementById("rolling-text").style.opacity = 1;
        clearInterval(countdownInterval); // Stop the countdown at roll time
        document.getElementById("timer").innerText = "10"; // Display 10 during rolling
        
        setTimeout(rollNumber, 2000); // Simulate roll delay
    }, 10000);
}

function rollNumber() {
    lastNumber = Math.floor(Math.random() * 101);
    document.getElementById("last-number").innerText = lastNumber;
    document.getElementById("rolling-text").style.opacity = 0;
    
    updateButtons(); // Update betting options based on the new number
}
