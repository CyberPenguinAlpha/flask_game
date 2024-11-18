const fs = require('fs');
const path = require('path');

let win;
const { app, BrowserWindow } = require('electron');

function createWindow()
{
    win=new BrowserWindow
    ({
        width:800,
        height:600,
        webPreferences:
        {
            nodeIntegration: false,
            contextIsolation: true
        }
    })
    win.loadURL('https://flask-game-5wzz.onrender.com');
    //win.webContents.openDevTools();
    win.on('closed', ()=>{win = null;});
}

// Inject JavaScript code after the window is loaded
    mainWindow.webContents.on('did-finish-load', () => {
        const script = `
        // Event listener for login submission
        document.getElementById('loginButton').addEventListener('click', function() {
            let firstName = document.getElementById('first_Name').value;
            let lastInitial = document.getElementById('last_Initial').value;
            let gradeLevel = document.getElementById('grade_Level').value;
            let loginTimestamp = new Date().toISOString();
        
            // Generate Session ID
            sessionID = generateSessionID(firstName, lastInitial, gradeLevel, loginTimestamp);
            
            // Log login details in T1.csv
            logLoginData(sessionID, firstName, lastInitial, gradeLevel, loginTimestamp);
        
            // Start the interaction
            handleInteraction();
        });
        `;

        mainWindow.webContents.executeJavaScript(script);
        }    
// Generate session ID
function generateSessionID(firstName, lastInitial, gradeLevel, timestamp) {
    return `${firstName.charAt(0)}${lastInitial}${gradeLevel}${timestamp}`;
}

// Log login data to T1.csv
function logLoginData(sessionID, firstName, lastInitial, gradeLevel, loginTimestamp) {
    const loginData = `${sessionID},${firstName},${lastInitial},${gradeLevel},${loginTimestamp}\n`;
    const loginFilePath = path.join(__dirname, 'T1.csv');
    
    // Append the login data to T1.csv
    fs.appendFileSync(loginFilePath, loginData);
}

// Handle student interaction with Gemini
function handleInteraction() {
    document.getElementById('submitButton').addEventListener('click', function() {
        studentSolution = document.getElementById('studentSolution').value;
        const startTime = new Date().toISOString();

        // Simulating the evaluation result (replace this with actual evaluation logic)
        const evaluationResult = simulateEvaluation(studentSolution);

        // Log the interaction in T2.csv
        const endTime = new Date().toISOString();
        const status = evaluationResult.status;
        const aiResponse = evaluationResult.aiResponse;

        logInteractionData(sessionID, studentSolution, aiResponse, startTime, endTime, status);

        // Show the appropriate message based on the status
        if (status === 'success') {
            showMessage('success', 'Correct! You’ve solved the challenge.');
        } else if (status === 'partial') {
            showMessage('partial', 'Partially correct! Try again.');
        } else {
            currentAttempt++;
            if (currentAttempt > 3) {
                showMessage('error', 'Maximum attempts reached! Please review the challenge and try again later.');
            } else {
                showMessage('error', 'Incorrect solution. Please try again.');
            }
        }
    });
}

// Log interaction data to T2.csv
function logInteractionData(sessionID, studentSolution, aiResponse, startTime, endTime, status) {
    const interactionData = `${startTime},${endTime},${studentSolution},${aiResponse},${status},${sessionID}\n`;
    const interactionFilePath = path.join(__dirname, 'T2.csv');
    
    // Append the interaction data to T2.csv
    fs.appendFileSync(interactionFilePath, interactionData);
}

// Show message to user
function showMessage(type, message) {
    const messageBox = document.getElementById('messageBox');
    messageBox.textContent = message;

    // Change message box style based on the type
    if (type === 'success') {
        messageBox.style.color = 'green';
    } else if (type === 'partial') {
        messageBox.style.color = 'orange';
    } else {
        messageBox.style.color = 'red';
    }
    messageBox.style.display = 'block';
}

app.whenReady().then(() => {
    createWindow();

    app.on('activate', () => {
        if(BrowserWindow,getAllWindows().length === 0) {createWindow();}
    });
});

app.on('window-all-closed', ()=> {
    if (process.platform !== 'darwin') {app.quit();}
});
