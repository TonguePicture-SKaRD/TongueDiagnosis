import { app, BrowserWindow } from 'electron';
import path from 'path';

function createWindow() {
    const win = new BrowserWindow({
        width: 1920,
        height: 1080,
        webPreferences: {
            nodeIntegration: true
        }
    });

    win.loadURL('http://localhost:5173/home'); // 这里可以改成你的本地页面
}

app.whenReady().then(() => {
    createWindow();
});
