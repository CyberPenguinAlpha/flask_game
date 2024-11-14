const { app, BrowserWindow } = require('electron');
const path = require('path');

let win;

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

function saveSessionDataToDesktop(firstName, lastInitial, gradeLevel, loginTimestamp, finishTimestamp)
{
    const desktopPath = app.getPath('desktop'); 
    const csvPath = path.join(desktopPath, 'user_sessions.csv')

    const data = '${firstName},${lastname},${gradeLevel},${loginTimestamp},${finishTimestamp},Completed Game\n';

    fs.appendFile(csvPath, data, (err) => 
        {
            if (err) 
                {console.error('Error writing to CSV file:', err);}
            else 
                {console.log('Session data saved successfully!')}
        }
    );
}

//saveSessionDataToDesktop('John', 'D', '7', '2024-11-07T10:30:00', '2024-11-07T11:00:00');

app.whenReady().then(() => {
    createWindow();

    app.on('activate', () => {
        if(BrowserWindow,getAllWindows().length === 0) {createWindow();}
    });
});

app.on('window-all-closed', ()=> {
    if (process.platform !== 'darwin') {app.quit();}
});
