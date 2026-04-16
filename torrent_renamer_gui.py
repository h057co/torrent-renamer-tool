import os
import re
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading

# --- Core Logic Functions ---

def bdecode(data):
    def decode_item(index):
        char = data[index:index+1]
        if char == b'i':
            end = data.find(b'e', index)
            return int(data[index+1:end]), end + 1
        elif char == b'l':
            index += 1
            items = []
            while data[index:index+1] != b'e':
                item, index = decode_item(index)
                items.append(item)
            return items, index + 1
        elif char == b'd':
            index += 1
            items = {}
            while data[index:index+1] != b'e':
                key, index = decode_item(index)
                value, index = decode_item(index)
                if isinstance(key, bytes):
                    key = key.decode('utf-8', 'ignore')
                items[key] = value
            return items, index + 1
        elif char.isdigit():
            colon = data.find(b':', index)
            if colon == -1: return None, index
            length = int(data[index:colon])
            start = colon + 1
            end = start + length
            return data[start:end], end
        else:
            return None, index

    try:
        result, _ = decode_item(0)
        return result
    except:
        return None

def sanitize_filename(filename):
    filename = re.sub(r'[\\/:*?"<>|]', '_', filename)
    filename = filename.strip('. ')
    return filename

def extract_tracker_shortname(announce_bytes):
    if not announce_bytes:
        return "Unknown"
    try:
        url = announce_bytes.decode('utf-8', 'ignore').lower()
        match = re.search(r'://([^:/]+)', url)
        if match:
            domain = match.group(1)
            parts = domain.split('.')
            if len(parts) >= 2:
                if parts[0] in ('tracker', 'announce', 'bt', 'torrent', 'www'):
                    return parts[1].upper()
                return parts[0].upper()
            return domain.upper()
    except:
        pass
    return "Unknown"

# --- GUI Application Class ---

class TorrentRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Torrent Renamer Tool")
        self.root.geometry("700x500")
        self.root.minsize(600, 400)

        # Variables
        self.folder_path = tk.StringVar(value="")
        self.dry_run = tk.BooleanVar(value=True)

        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"))
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        header = ttk.Label(main_frame, text="Renombrador de Archivos Torrent", style="Header.TLabel")
        header.pack(pady=(0, 20))

        # Folder Selection
        folder_frame = ttk.Frame(main_frame)
        folder_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(folder_frame, text="Carpeta de Torrents:").pack(side=tk.LEFT)
        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_path)
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(folder_frame, text="Examinar...", command=self.browse_folder).pack(side=tk.RIGHT)

        # Options
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.X, pady=10)
        
        ttk.Checkbutton(options_frame, text="Modo Simulación (No renombra archivos)", variable=self.dry_run).pack(side=tk.LEFT)

        # Start Button
        self.start_btn = ttk.Button(main_frame, text="Iniciar Proceso", command=self.start_process)
        self.start_btn.pack(pady=10)

        # Log Area
        log_frame = ttk.Frame(main_frame)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(log_frame, text="Registro de Actividad:").pack(anchor=tk.W)
        self.log_text = tk.Text(log_frame, height=10, state=tk.DISABLED, bg="#f0f0f0")
        self.log_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def start_process(self):
        directory = self.folder_path.get()
        if not directory or not os.path.exists(directory):
            messagebox.showerror("Error", "Por favor, selecciona una carpeta válida.")
            return

        self.start_btn.config(state=tk.DISABLED)
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # Run in a thread to keep GUI responsive
        threading.Thread(target=self.run_renaming_logic, args=(directory, self.dry_run.get()), daemon=True).start()

    def run_renaming_logic(self, directory, dry_run):
        try:
            files = [f for f in os.listdir(directory) if f.lower().endswith('.torrent')]
            mode_str = "SIMULACIÓN" if dry_run else "EJECUCIÓN REAL"
            self.log(f"--- Iniciando {mode_str} ---")
            self.log(f"Procesando {len(files)} archivos en: {directory}\n")

            count = 0
            for filename in files:
                filepath = os.path.join(directory, filename)
                try:
                    with open(filepath, 'rb') as f:
                        data = f.read()
                    
                    metadata = bdecode(data)
                    if not metadata or 'info' not in metadata or 'name' not in metadata['info']:
                        continue
                    
                    tracker_url = metadata.get('announce')
                    tracker_name = extract_tracker_shortname(tracker_url)

                    original_name_bytes = metadata['info']['name']
                    try:
                        content_name = original_name_bytes.decode('utf-8')
                    except:
                        content_name = original_name_bytes.decode('latin-1', 'ignore')
                    
                    content_name = sanitize_filename(content_name)
                    new_filename = f"[{tracker_name}] {content_name}"
                    if not new_filename.lower().endswith('.torrent'):
                        new_filename += ".torrent"

                    if filename == new_filename:
                        continue

                    self.log(f"✓ {filename} -> {new_filename}")
                    
                    if not dry_run:
                        new_filepath = os.path.join(directory, new_filename)
                        if os.path.exists(new_filepath):
                            base, ext = os.path.splitext(new_filename)
                            counter = 1
                            while os.path.exists(os.path.join(directory, f"{base} ({counter}){ext}")):
                                counter += 1
                            new_filepath = os.path.join(directory, f"{base} ({counter}){ext}")
                        
                        os.rename(filepath, new_filepath)
                    count += 1
                except Exception as e:
                    self.log(f"✗ Error en {filename}: {str(e)}")

            self.log(f"\n--- Proceso finalizado ---")
            self.log(f"Archivos procesados: {count}")
            if not dry_run:
                messagebox.showinfo("Completado", f"Se han renombrado {count} archivos.")
            else:
                messagebox.showinfo("Simulación", f"Simulación completada. No se realizaron cambios físicos.")

        except Exception as e:
            self.log(f"Error crítico: {str(e)}")
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
        
        finally:
            self.start_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = TorrentRenamerApp(root)
    root.mainloop()
