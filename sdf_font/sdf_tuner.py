#!/usr/bin/env python3
"""
SDF Font Tuner - Real-time visual parameter adjustment tool
Lets you preview and adjust SDF font rendering parameters with sliders
"""

import sys
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np

class SDFTuner:
    def __init__(self, sdf_path):
        self.root = tk.Tk()
        self.root.title("SDF Font Tuner - Real-time Preview")
        self.root.geometry("1200x800")
        
        # Load SDF texture
        self.sdf_img = Image.open(sdf_path).convert('RGBA')
        self.sdf_array = np.array(self.sdf_img).astype(float) / 255.0
        
        # Parameters (matching FFNx defaults)
        self.params = {
            'pixel_range': tk.DoubleVar(value=4.0),
            'thickness': tk.DoubleVar(value=0.5),
            'shadow_offset': tk.DoubleVar(value=1.0),
            'shadow_opacity': tk.DoubleVar(value=0.5),
        }
        
        # Setup UI
        self._setup_ui()
        
        # Initial render
        self.update_preview()
    
    def _setup_ui(self):
        """Create the UI layout"""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Preview area (left side)
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="10")
        preview_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.preview_label = ttk.Label(preview_frame)
        self.preview_label.pack()
        
        # Controls area (right side)
        controls_frame = ttk.LabelFrame(main_frame, text="Parameters", padding="10")
        controls_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Pixel Range slider
        self._add_slider(controls_frame, 0, "Pixel Range (Edge Smoothness)",
                        self.params['pixel_range'], 1.0, 10.0, 0.1,
                        "Distance field spread - higher = smoother edges")
        
        # Thickness slider
        self._add_slider(controls_frame, 1, "Thickness (Boldness)",
                        self.params['thickness'], 0.2, 1.0, 0.05,
                        "Glyph weight - 0.5 = normal, higher = bolder")
        
        # Shadow offset slider
        self._add_slider(controls_frame, 2, "Shadow Offset (pixels)",
                        self.params['shadow_offset'], 0.0, 5.0, 0.5,
                        "Shadow distance - 0 = no shadow")
        
        # Shadow opacity slider
        self._add_slider(controls_frame, 3, "Shadow Opacity",
                        self.params['shadow_opacity'], 0.0, 1.0, 0.05,
                        "Shadow darkness - 0 = invisible, 1 = opaque")
        
        # Export button
        export_btn = ttk.Button(controls_frame, text="Copy to FFNx.toml", 
                               command=self.export_config)
        export_btn.grid(row=4, column=0, columnspan=3, pady=20, sticky=(tk.W, tk.E))
        
        # Config display
        self.config_text = tk.Text(controls_frame, height=8, width=40)
        self.config_text.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # Make resizable
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=1)
    
    def _add_slider(self, parent, row, label, variable, min_val, max_val, resolution, tooltip):
        """Add a labeled slider"""
        # Label
        lbl = ttk.Label(parent, text=label)
        lbl.grid(row=row*2, column=0, sticky=tk.W, pady=(10, 0))
        
        # Tooltip
        tip = ttk.Label(parent, text=tooltip, font=('Arial', 8), foreground='gray')
        tip.grid(row=row*2, column=0, sticky=tk.W, pady=(25, 0))
        
        # Value display
        value_lbl = ttk.Label(parent, text=f"{variable.get():.2f}")
        value_lbl.grid(row=row*2, column=1, sticky=tk.E, pady=(10, 0))
        
        # Slider
        slider = ttk.Scale(parent, from_=min_val, to=max_val, orient=tk.HORIZONTAL,
                          variable=variable, command=lambda v: self._on_slider_change(v, value_lbl))
        slider.grid(row=row*2+1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Update on change
        variable.trace_add('write', lambda *args: self.update_preview())
    
    def _on_slider_change(self, value, label):
        """Update value label when slider moves"""
        label.config(text=f"{float(value):.2f}")
    
    def median(self, r, g, b):
        """Compute median of RGB (for SDF)"""
        return np.maximum(np.minimum(r, g), np.minimum(np.maximum(r, g), b))
    
    def update_preview(self):
        """Render preview with current parameters"""
        # Get parameters
        px_range = self.params['pixel_range'].get()
        thickness = self.params['thickness'].get()
        shadow_off = self.params['shadow_offset'].get()
        shadow_opa = self.params['shadow_opacity'].get()
        
        # Extract RGB channels (SDF data)
        r, g, b, a = self.sdf_array[:,:,0], self.sdf_array[:,:,1], self.sdf_array[:,:,2], self.sdf_array[:,:,3]
        
        # Compute signed distance (main glyph)
        sd = self.median(r, g, b)
        screen_px_dist = px_range * (sd - 0.5)
        opacity = np.clip(screen_px_dist + thickness, 0.0, 1.0)
        
        # Compute shadow (shifted)
        shadow_pixels = int(shadow_off)
        if shadow_pixels > 0:
            shadow_sd = np.roll(np.roll(sd, shadow_pixels, axis=0), shadow_pixels, axis=1)
            shadow_dist = px_range * (shadow_sd - 0.5)
            shadow_value = np.clip(shadow_dist + 0.5, 0.0, 1.0)
        else:
            shadow_value = np.zeros_like(sd)
        
        # Composite: white text with black shadow
        white = np.ones_like(opacity)
        black = np.zeros_like(opacity)
        
        # Mix shadow and text
        final_r = white * opacity + black * (1 - opacity) * shadow_value * shadow_opa
        final_g = white * opacity + black * (1 - opacity) * shadow_value * shadow_opa
        final_b = white * opacity + black * (1 - opacity) * shadow_value * shadow_opa
        final_a = np.maximum(opacity, shadow_value * shadow_opa)
        
        # Clamp
        final_r = np.clip(final_r, 0, 1)
        final_g = np.clip(final_g, 0, 1)
        final_b = np.clip(final_b, 0, 1)
        final_a = np.clip(final_a, 0, 1)
        
        # Convert to image
        output = np.stack([final_r, final_g, final_b, final_a], axis=2)
        output_uint8 = (output * 255).astype(np.uint8)
        
        # Create preview image (scale up for visibility)
        preview_img = Image.fromarray(output_uint8, mode='RGBA')
        
        # Crop to show just a few characters
        preview_img = preview_img.crop((0, 0, 512, 256))
        
        # Scale up 2x for better visibility
        preview_img = preview_img.resize((1024, 512), Image.NEAREST)
        
        # Add checkerboard background to show transparency
        bg = self._create_checkerboard(1024, 512)
        bg.paste(preview_img, (0, 0), preview_img)
        
        # Display
        photo = ImageTk.PhotoImage(bg)
        self.preview_label.config(image=photo)
        self.preview_label.image = photo  # Keep reference
        
        # Update config text
        self.update_config_display()
    
    def _create_checkerboard(self, width, height, square_size=20):
        """Create a checkerboard background"""
        img = Image.new('RGB', (width, height), 'white')
        pixels = img.load()
        
        for i in range(width):
            for j in range(height):
                if ((i // square_size) + (j // square_size)) % 2:
                    pixels[i, j] = (200, 200, 200)
        
        return img
    
    def update_config_display(self):
        """Update the config text display"""
        config = f"""# Copy these to FFNx.toml:

sdf_pixel_range = {self.params['pixel_range'].get():.1f}
sdf_thickness = {self.params['thickness'].get():.2f}
sdf_shadow_offset = {self.params['shadow_offset'].get():.1f}
sdf_shadow_opacity = {self.params['shadow_opacity'].get():.2f}
"""
        self.config_text.delete('1.0', tk.END)
        self.config_text.insert('1.0', config)
    
    def export_config(self):
        """Copy config to clipboard"""
        config = self.config_text.get('1.0', tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(config)
        
        # Show confirmation
        btn = self.root.nametowidget('.!frame.!labelframe2.!button')
        original_text = btn.cget('text')
        btn.config(text="✓ Copied to clipboard!")
        self.root.after(2000, lambda: btn.config(text=original_text))
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sdf_tuner.py <path_to_sdf.png>")
        print("Example: python sdf_tuner.py jafont_1_00_sdf.png")
        sys.exit(1)
    
    app = SDFTuner(sys.argv[1])
    app.run()
