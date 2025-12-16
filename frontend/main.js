import {app, BrowserWindow, globalShortcut, Menu} from 'electron';
import path from 'path';
import {fileURLToPath} from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
Menu.setApplicationMenu(null);

function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        },
    });

    win.loadFile(path.join(__dirname, 'dist', 'index.html'));
    win.webContents.openDevTools();
    registerShortcuts(win);
}

function registerShortcuts(win) {
    globalShortcut.register('CommandOrControl+1', () => {
        const currentZoom = win.webContents.getZoomFactor();
        win.webContents.setZoomFactor(currentZoom + 0.1);
    });
    globalShortcut.register('CommandOrControl+2', () => {
        const currentZoom = win.webContents.getZoomFactor();
        win.webContents.setZoomFactor(currentZoom - 0.1);
    });
    globalShortcut.register('CommandOrControl+0', () => {
        win.webContents.setZoomFactor(1.0); // 重置为默认缩放比例
    });
}

app.whenReady().then(() => {
    createWindow();
    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('will-quit', () => {
    globalShortcut.unregisterAll();
});
