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
            nodeIntegration: true,
            contextIsolation: true
        }
    })
    win.loadURL('https://flask-game-5wzz.onrender.com');
    //win.webContents.openDevTools();
    win.on('closed', ()=>{win = null;});
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
