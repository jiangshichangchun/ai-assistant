#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use serde::{Deserialize, Serialize};
use tauri::{Manager, SystemTray, SystemTrayEvent, SystemTrayMenu, SystemTrayMenuItem};

#[derive(Debug, Serialize, Deserialize)]
struct Message {
    content: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct ClipboardContent {
    text: String,
}

#[tauri::command]
async fn send_message(message: String) -> Result<String, String> {
    // 模拟AI回复
    Ok(format!("你刚才说：{}", message))
}

#[tauri::command]
async fn toggle_module(module_id: String, status: bool) -> Result<String, String> {
    // 模拟模块状态切换
    Ok(format!("模块 {} 已{}用", module_id, if status { "启" } else { "停" }))
}

#[tauri::command]
async fn get_clipboard_content() -> Result<ClipboardContent, String> {
    // 获取剪贴板内容
    let clipboard = arboard::Clipboard::new().map_err(|e| e.to_string())?;
    let text = clipboard.get_text().map_err(|e| e.to_string())?;
    Ok(ClipboardContent { text })
}

#[tauri::command]
async fn set_clipboard_content(text: String) -> Result<(), String> {
    // 设置剪贴板内容
    let clipboard = arboard::Clipboard::new().map_err(|e| e.to_string())?;
    clipboard.set_text(text).map_err(|e| e.to_string())?;
    Ok(())
}

fn main() {
    let system_tray_menu = SystemTrayMenu::new()
        .add_item(SystemTrayMenuItem::new("显示应用", "show"))
        .add_item(SystemTrayMenuItem::new("隐藏应用", "hide"))
        .add_item(SystemTrayMenuItem::new("退出", "quit"));

    let system_tray = SystemTray::new()
        .with_menu(system_tray_menu);

    tauri::Builder::default()
        .system_tray(system_tray)
        .on_system_tray_event(|app, event| match event {
            SystemTrayEvent::MenuItemClick { id, .. } => {
                match id.as_str() {
                    "show" => {
                        let window = app.get_window("main").unwrap();
                        window.show().unwrap();
                    }
                    "hide" => {
                        let window = app.get_window("main").unwrap();
                        window.hide().unwrap();
                    }
                    "quit" => {
                        app.exit(0);
                    }
                    _ => {}
                }
            }
            _ => {}
        })
        .invoke_handler(tauri::generate_handler![
            send_message, 
            toggle_module,
            get_clipboard_content,
            set_clipboard_content
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}