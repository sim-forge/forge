#![cfg_attr(
  all(not(debug_assertions), target_os = "windows"),
  windows_subsystem = "windows"
)]

use std::sync::Mutex;
use tauri::{State, Window};

struct AppState {
  counter: Mutex<i32>,
}

#[tauri::command]
fn increment_counter(state: State<AppState>) -> i32 {
  let mut counter = state.counter.lock().unwrap();
  *counter += 1;
  *counter
}

#[tauri::command]
fn get_counter(state: State<AppState>) -> i32 {
  *state.counter.lock().unwrap()
}

fn main() {
  let app_state = AppState {
    counter: Mutex::new(0),
  };

  tauri::Builder::default()
    .manage(app_state)
    .invoke_handler(tauri::generate_handler![
      increment_counter,
      get_counter
    ])
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}