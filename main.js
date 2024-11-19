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

    // Inject JavaScript code after the window is loaded
    win.webContents.on('did-finish-load', () => {
        const script = `
        // Event listener for login submission
        document.getElementById('loginButton').addEventListener('click', function() {
            event.preventDefault();
            
            let firstName = document.getElementById('first_name').value; 
            let lastInitial = document.getElementById('last_initial').value; 
            let gradeLevel = document.getElementById('grade_level').value; 
            let loginTimestamp = new Date().toISOString();
            sessionID = generateSessionID(firstName, lastInitial, gradeLevel, loginTimestamp);
            logLoginData(sessionID, firstName, lastInitial, gradeLevel, loginTimestamp);

            document.querySelector('form').submit();
        });
        `;

        win.webContents.executeJavaScript(script);
        }); 
    
    win.on('closed', ()=>{win = null;});
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
