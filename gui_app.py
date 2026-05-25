import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
from pathlib import Path
import os
import sys

from watermark_remover import WatermarkRemover, is_watermark_removal_available
from metadata_handler import has_ai_metadata, get_ai_metadata_summary

class WatermarkGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Watermark & Metadata Remover")
        self.geometry("900x600")
        
        self.input_dir = None
        self.detected_images = []  # List of dicts {path, type_summary}

        # UI Setup
        top_frame = tk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        self.btn_select = tk.Button(top_frame, text="1. Select Folder to Scan", command=self.select_folder)
        self.btn_select.pack(side=tk.LEFT, padx=5)
        
        self.lbl_status = tk.Label(top_frame, text="Ready.")
        self.lbl_status.pack(side=tk.LEFT, padx=15)
        
        # Table
        columns = ("path", "has_ai", "type")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.heading("path", text="Image File")
        self.tree.heading("has_ai", text="Has AI/Watermark")
        self.tree.heading("type", text="Metadata Type / Details")
        
        self.tree.column("path", width=300, minwidth=150, stretch=tk.YES)
        self.tree.column("has_ai", width=130, minwidth=100, stretch=tk.NO, anchor=tk.CENTER)
        self.tree.column("type", width=400, minwidth=200, stretch=tk.YES)
        
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Bottom controls
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        # Scan Progress
        scan_frame = tk.Frame(bottom_frame)
        scan_frame.pack(side=tk.TOP, fill=tk.X, pady=2)
        tk.Label(scan_frame, text="Scan Progress:", width=20, anchor="w").pack(side=tk.LEFT)
        self.scan_progress = ttk.Progressbar(scan_frame, orient=tk.HORIZONTAL, mode='determinate')
        self.scan_progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Removal Progress
        removal_frame = tk.Frame(bottom_frame)
        removal_frame.pack(side=tk.TOP, fill=tk.X, pady=2)
        tk.Label(removal_frame, text="Overall Removal Progress:", width=20, anchor="w").pack(side=tk.LEFT)
        self.removal_progress = ttk.Progressbar(removal_frame, orient=tk.HORIZONTAL, mode='determinate')
        self.removal_progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # File Progress
        file_frame = tk.Frame(bottom_frame)
        file_frame.pack(side=tk.TOP, fill=tk.X, pady=2)
        tk.Label(file_frame, text="Current File Activity:", width=20, anchor="w").pack(side=tk.LEFT)
        self.file_progress = ttk.Progressbar(file_frame, orient=tk.HORIZONTAL, mode='indeterminate')
        self.file_progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Buttons
        btn_frame = tk.Frame(bottom_frame)
        btn_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        self.btn_remove = tk.Button(btn_frame, text="2. Remove Watermarks from Detected Images", state=tk.DISABLED, command=self.remove_watermarks)
        self.btn_remove.pack(side=tk.RIGHT, padx=5)

    def select_folder(self):
        folder = filedialog.askdirectory(title="Select Folder to Scan")
        if folder:
            self.input_dir = Path(folder)
            self.lbl_status.config(text=f"Scanning {self.input_dir}...")
            self.tree.delete(*self.tree.get_children())
            self.detected_images.clear()
            self.btn_remove.config(state=tk.DISABLED)
            
            # Run scan in background thread
            threading.Thread(target=self.scan_folder, daemon=True).start()

    def scan_folder(self):
        extensions = {'.png', '.jpg', '.jpeg'}
        files_to_check = []
        for root, _, files in os.walk(self.input_dir):
            for file in files:
                if Path(file).suffix.lower() in extensions:
                    files_to_check.append(Path(root) / file)
                    
        total = len(files_to_check)
        count_ai = 0
        
        self.scan_progress["maximum"] = total if total > 0 else 1
        self.scan_progress["value"] = 0
        self.removal_progress["value"] = 0
        
        for i, file_path in enumerate(files_to_check):
            # Check for AI metadata / Watermarks
            try:
                has_ai = has_ai_metadata(file_path)
                if has_ai:
                    count_ai += 1
                    summary = get_ai_metadata_summary(file_path).replace('\n', ' | ')
                    item_id = self.tree.insert("", tk.END, values=(
                        str(file_path.relative_to(self.input_dir) if self.input_dir in file_path.parents else file_path),
                        "Yes",
                        summary
                    ))
                    self.detected_images.append({
                        "path": file_path,
                        "summary": summary,
                        "item_id": item_id
                    })
            except Exception as e:
                pass # Skip files that can't be read properly
                
            self.scan_progress["value"] = i + 1
            self.update_idletasks()
            
        self.after(0, lambda c=count_ai: self._finish_scan(c))

    def _finish_scan(self, count_ai):
        if count_ai > 0:
            self.lbl_status.config(text=f"Scan complete. Found {count_ai} images with AI metadata/watermarks.")
            self.btn_remove.config(state=tk.NORMAL)
        else:
            self.lbl_status.config(text="Scan complete. No watermarks found.")
            messagebox.showinfo(
                "Scan Complete", 
                "Great news! No images with invisible watermarks or AI metadata were found in this folder."
            )

    def remove_watermarks(self):
        if not self.detected_images:
            return
            
        if not is_watermark_removal_available():
            messagebox.showerror("Error", "Watermark removal is not available. Please ensure diffusers/torch are installed.")
            return

        confirm = messagebox.askyesno(
            "Confirm Removal", 
            f"Are you sure you want to remove invisible watermarks and metadata from {len(self.detected_images)} images?\n\nThis will overwrite the original files with cleaned versions."
        )
        
        if confirm:
            self.btn_select.config(state=tk.DISABLED)
            self.btn_remove.config(state=tk.DISABLED)
            self.lbl_status.config(text="Initializing model (this may take a moment)...")
            
            # Run removal in background
            threading.Thread(target=self.process_removal, daemon=True).start()

    def process_removal(self):
        try:
            # Initialize remover (loads model to CPU/GPU) with verbose callback
            def update_verbose_text(msg):
                self.after(0, lambda m=msg: self.lbl_status.config(text=m))
                
            remover = WatermarkRemover(
                model_id="Lykon/dreamshaper-8", 
                device="auto",
                progress_callback=update_verbose_text
            )
            
            self.removal_progress["maximum"] = len(self.detected_images)
            self.removal_progress["value"] = 0
            
            for i, img_info in enumerate(self.detected_images):
                img_path = img_info["path"]
                item_id = img_info.get("item_id")
                
                # Safe GUI update for status
                self.after(0, lambda n=img_path.name, idx=i: self._start_file_progress(n, idx))
                
                # Process and overwrite
                remover.remove_watermark(
                    image_path=img_path,
                    output_path=img_path, # overwrite
                    strength=0.04,
                    num_inference_steps=50
                )
                
                # Safe GUI update for tree and progress
                self.after(0, lambda idx=i, iid=item_id: self._update_item_cleaned(idx, iid))
                
            self.after(0, self._finish_success)
            
        except Exception as e:
            err = str(e)
            self.after(0, lambda: self._finish_error(err))

    def _start_file_progress(self, name, idx):
        self.lbl_status.config(text=f"Starting: {name} ({idx+1}/{len(self.detected_images)})...")
        self.file_progress.start(15)

    def _update_item_cleaned(self, idx, iid):
        self.removal_progress["value"] = idx + 1
        self.file_progress.stop()
        vals = self.tree.item(iid, "values")
        if vals:
            self.tree.item(iid, values=(vals[0], "Cleaned", "Metadata stripped"))
            self.update_idletasks()

    def _finish_success(self):
        self.file_progress.stop()
        self.lbl_status.config(text="Cleaning complete! All detected watermarks and metadata have been removed.")
        self.btn_select.config(state=tk.NORMAL)
        messagebox.showinfo("Success", "Watermark and AI metadata removal completed successfully!")
        self.detected_images.clear()

    def _finish_error(self, err_msg):
        self.file_progress.stop()
        self.lbl_status.config(text="An error occurred.")
        self.btn_select.config(state=tk.NORMAL)
        self.btn_remove.config(state=tk.NORMAL)
        messagebox.showerror("Error", f"An error occurred during removal:\n{err_msg}")

if __name__ == "__main__":
    app = WatermarkGUI()
    app.mainloop()
