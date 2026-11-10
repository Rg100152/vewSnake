"""vewSnake GUI - Tkinter frontend for the vewSnake image engine.

Developer: Raj Gautam
Usage: python3 -m vewsnake.gui  (or `vewsnake-gui` after pip install)
"""

import io
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import requests
from PIL import Image, ImageTk

from .constants import AUTHOR, BANNER, REQUEST_TIMEOUT, USER_AGENT, VERSION, resolve_endpoint

# Set this to your own server (or export VEWSNAKE_API) to use a custom endpoint:
CUSTOM_API_ENDPOINT: str | None = None


class VewSnakeGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(f"vewSnake GUI v{VERSION} — Image Generator")
        self.root.geometry("650x720")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(
            "TProgressbar", thickness=8, troughcolor="#313244", background="#cba6f7"
        )
        self.setup_ui()

    def setup_ui(self) -> None:
        header = tk.Label(
            self.root, text="vewSnake AI Engine", font=("Courier", 20, "bold"),
            fg="#cba6f7", bg="#1e1e2e",
        )
        header.pack(pady=15)

        developer_tag = tk.Label(
            self.root,
            text=f"Free key-less API profile | Dev: {AUTHOR} | v{VERSION}",
            font=("Helvetica", 9, "italic"), fg="#a6adc8", bg="#1e1e2e",
        )
        developer_tag.pack(pady=2)

        input_frame = tk.Frame(self.root, bg="#1e1e2e")
        input_frame.pack(fill="x", padx=30, pady=10)

        prompt_label = tk.Label(
            input_frame, text="Enter Vector Instruction (Prompt):",
            font=("Helvetica", 11, "bold"), fg="#cdd6f4", bg="#1e1e2e",
        )
        prompt_label.pack(anchor="w", pady=5)

        self.prompt_entry = tk.Text(
            input_frame, height=4, bg="#313244", fg="#cdd6f4",
            insertbackground="white", font=("Helvetica", 11), bd=0,
            highlightthickness=1, highlightbackground="#45475a",
            highlightcolor="#cba6f7",
        )
        self.prompt_entry.pack(fill="x", pady=5)
        self.prompt_entry.insert(
            "1.0",
            "A green snake coding on an old laptop, matrix digital rain "
            "background, highly detailed cyberpunk style",
        )

        self.btn_generate = tk.Button(
            self.root, text="GENERATE IMAGE", font=("Helvetica", 11, "bold"),
            bg="#a6e3a1", fg="#11111b", activebackground="#b4befe",
            activeforeground="#11111b", bd=0, cursor="hand2",
            command=self.start_generation_thread,
        )
        self.btn_generate.pack(fill="x", padx=30, pady=15)

        self.progress = ttk.Progressbar(
            self.root, orient="horizontal", mode="indeterminate", style="TProgressbar"
        )
        self.status_label = tk.Label(
            self.root, text="System Idle | Free API Node Connected",
            font=("Helvetica", 10), fg="#a6adc8", bg="#1e1e2e",
        )
        self.status_label.pack(pady=2)

        preview_label = tk.Label(
            self.root, text="Render Output Preview:", font=("Helvetica", 10, "bold"),
            fg="#a6adc8", bg="#1e1e2e",
        )
        preview_label.pack(anchor="w", padx=30, pady=5)

        self.preview_frame = tk.Frame(
            self.root, width=590, height=380, bg="#313244",
            highlightthickness=1, highlightbackground="#45475a",
        )
        self.preview_frame.pack_propagate(False)
        self.preview_frame.pack(padx=30, pady=5)

        self.image_display = tk.Label(self.preview_frame, bg="#313244")
        self.image_display.pack(expand=True, fill="both")
        self.raw_image_data: bytes | None = None

    def log_status(self, text: str, color: str = "#a6adc8") -> None:
        self.status_label.config(text=text, fg=color)

    def start_generation_thread(self) -> None:
        prompt = self.prompt_entry.get("1.0", "end-1c").strip()
        if not prompt:
            messagebox.showwarning("Execution Halted", "Prompt text field cannot be empty.")
            return

        self.btn_generate.config(state="disabled", bg="#45475a")
        self.progress.pack(fill="x", padx=30, pady=5)
        self.progress.start(10)
        self.log_status("[CONNECTING] Handshaking with inference API...", "#f9e2af")
        threading.Thread(target=self.execute_inference, args=(prompt,), daemon=True).start()

    def execute_inference(self, prompt: str) -> None:
        try:
            url, is_custom = resolve_endpoint(CUSTOM_API_ENDPOINT, prompt, 1024, 1024)
            if is_custom:
                response = requests.post(
                    url, json={"prompt": prompt}, timeout=REQUEST_TIMEOUT,
                    headers={"User-Agent": USER_AGENT},
                )
            else:
                response = requests.get(
                    url, timeout=REQUEST_TIMEOUT, headers={"User-Agent": USER_AGENT}
                )

            if response.status_code == 200:
                self.log_status("[SUCCESS] Processing completed. Rendering graphics asset...", "#a6e3a1")
                self.raw_image_data = response.content
                self.root.after(0, self.display_render_preview)
            else:
                msg = f"Server responded with fault code: {response.status_code}"
                self.root.after(0, lambda: messagebox.showerror("API Error", msg))
                self.root.after(0, self.reset_ui_state)

        except Exception as system_fault:  # noqa: BLE001 - GUI boundary handler
            self.root.after(
                0, lambda: messagebox.showerror("API Offline", f"Connection fault:\n{system_fault}")
            )
            self.root.after(0, self.reset_ui_state)

    def display_render_preview(self) -> None:
        try:
            img = Image.open(io.BytesIO(self.raw_image_data))
            img.thumbnail((570, 360), Image.Resampling.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(img)
            self.image_display.config(image=self.tk_image)
            self.log_status("Image generated successfully!", "#a6e3a1")
            self.save_compiled_asset()
        except Exception as compilation_error:  # noqa: BLE001 - GUI boundary handler
            messagebox.showerror("Graphics Compilation Error", str(compilation_error))
        self.reset_ui_state()

    def save_compiled_asset(self) -> None:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Format", "*.png")],
            title="Save vewSnake Image",
        )
        if file_path:
            with open(file_path, "wb") as storage_file:
                storage_file.write(self.raw_image_data)
            messagebox.showinfo("Export Successful", f"Saved at:\n{file_path}")

    def reset_ui_state(self) -> None:
        self.progress.stop()
        self.progress.pack_forget()
        self.btn_generate.config(state="normal", bg="#a6e3a1")


def main() -> None:
    app_window = tk.Tk()
    VewSnakeGUI(app_window)
    app_window.mainloop()


if __name__ == "__main__":
    main()
