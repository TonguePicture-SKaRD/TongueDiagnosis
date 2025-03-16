import {app, BrowserWindow, globalShortcut, Menu} from 'electron';
import path from 'path';
import {fileURLToPath} from 'url';

// 解决 __dirname 在 ES 模块中不可用的问题
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
// 禁用菜单栏
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

    // 加载 Vue 打包后的 index.html 文件
    win.loadFile(path.join(__dirname, 'dist', 'index.html'));

    // 打开开发者工具（可选）
    // win.webContents.openDevTools();

    // 注册全局快捷键
    registerShortcuts(win);
}

// 注册放大和缩小的快捷键
function registerShortcuts(win) {
    // 放大快捷键：CmdOrCtrl + Plus
    globalShortcut.register('CommandOrControl+1', () => {
        const currentZoom = win.webContents.getZoomFactor();
        win.webContents.setZoomFactor(currentZoom + 0.1);
    });

    // 缩小快捷键：CmdOrCtrl + Minus
    globalShortcut.register('CommandOrControl+2', () => {
        const currentZoom = win.webContents.getZoomFactor();
        win.webContents.setZoomFactor(currentZoom - 0.1);
    });

    // 重置缩放快捷键：CmdOrCtrl + 0
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

// 在应用退出时注销所有快捷键
app.on('will-quit', () => {
    globalShortcut.unregisterAll();
});