// const balance = document.getElementById('balance')
// const money_plus = document.getElementById('money-plus')
// const money_minus = document.getElementById('money-minus')
// const list = document.getElementById('list')
// const from = document.getElementById('from')
// const text = document.getElementById('text')
// const amount = document.getElementById('amount')

// app.js

// Define global variables
const balanceElement = document.getElementById("balance");
const moneyPlusElement = document.getElementById("money-plus");
const moneyMinusElement = document.getElementById("money-minus");
const listElement = document.getElementById("list");
const formElement = document.getElementById("form");
const textElement = document.getElementById("text");
const amountElement = document.getElementById("amount");

// Define transactions array and initialize it from local storage
let transactions = JSON.parse(localStorage.getItem('transactions')) || [];

// Function to initialize the app
function init() {
    listElement.innerHTML = "";
    transactions.forEach(addTransactionDOM);
    updateBalance();
}

// Function to add a new transaction
function addTransaction(e) {
    e.preventDefault();
    const text = textElement.value.trim();
    const amount = amountElement.value.trim();

    if (text === "" || amount === "") {
        alert('Please add text and amount');
        return;
    }

    const transaction = {
        id: generateID(),
        text,
        amount: parseFloat(amount),
    };

    transactions.push(transaction);
    addTransactionDOM(transaction);
    updateBalance();
    updateLocalStorage();
    textElement.value = "";
    amountElement.value = "";
}

// Function to generate a random ID for transactions
function generateID() {
    return Math.floor(Math.random() * 1000000000);
}

// Function to add a transaction to the DOM
function addTransactionDOM(transaction) {
    const sign = transaction.amount < 0 ? "-" : "+";
    const item = document.createElement("li");
    item.classList.add(transaction.amount < 0 ? "minus" : "plus");
    item.innerHTML = `
        ${transaction.text} <span>${sign}${Math.abs(transaction.amount.toFixed(2))}</span>
        <button class="delete-btn" onclick="removeTransaction(${transaction.id})">x</button>
    `;
    listElement.appendChild(item);
}

// Function to update balance, income, and expenses
function updateBalance() {
    const amounts = transactions.map(transaction => transaction.amount);
    const total = amounts.reduce((acc, item) => acc + item, 0).toFixed(2);
    const income = amounts.filter(item => item > 0).reduce((acc, item) => acc + item, 0).toFixed(2);
    const expense = (amounts.filter(item => item < 0).reduce((acc, item) => acc + item, 0) * -1).toFixed(2);

    balanceElement.innerText = `₹${total}`;
    moneyPlusElement.innerText = `₹${income}`;
    moneyMinusElement.innerText = `₹${expense}`;
}

// Function to remove a transaction by ID
function removeTransaction(id) {
    transactions = transactions.filter(transaction => transaction.id !== id);
    updateLocalStorage();
    init();
}

// Function to update local storage
function updateLocalStorage() {
    localStorage.setItem('transactions', JSON.stringify(transactions));
}

// Initialize the app when the DOM is ready
document.addEventListener("DOMContentLoaded", init);

// Add event listener to the form for adding transactions
formElement.addEventListener('submit', addTransaction);

// ... (existing code)

const incomeRadio = document.getElementById("incomeRadio");
const expenseRadio = document.getElementById("expenseRadio");

// Function to update the balance and history based on income or expense selection
function handleTransactionSelection(transaction) {
    if (incomeRadio.checked) {
        // Handle income
        // Update the balance (add the transaction amount)
        const total = parseFloat(balanceElement.innerText.replace("₹", ""));
        const newTotal = total + transaction.amount;
        balanceElement.innerText = `₹${newTotal.toFixed(2)}`;
    } else if (expenseRadio.checked) {
        // Handle expense
        // Update the balance (subtract the transaction amount)
        const total = parseFloat(balanceElement.innerText.replace("₹", ""));
        const newTotal = total - transaction.amount;
        balanceElement.innerText = `₹${newTotal.toFixed(2)}`;
    }

    // Record the transaction in the history
    addTransactionToHistory(transaction);
}

// Modify the addTransaction function to use handleTransactionSelection
function addTransaction(e) {
    e.preventDefault();
    const text = textElement.value.trim();
    const amount = amountElement.value.trim();
    const incomeExpense = incomeRadio.checked ? "income" : "expense";

    if (text === "" || amount === "") {
        alert('Please add text and amount');
        return;
    }

    const transaction = {
        id: generateID(),
        text,
        amount: parseFloat(amount) * (incomeExpense === "expense" ? -1 : 1),
    };

    transactions.push(transaction);
    handleTransactionSelection(transaction); // Update balance and history based on selection
    updateLocalStorage();
    textElement.value = "";
    amountElement.value = "";
}