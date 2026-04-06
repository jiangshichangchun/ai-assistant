#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
struct Message {
    content: String,
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

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![send_message, toggle_module])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}