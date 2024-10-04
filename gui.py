import customtkinter as ctk
import numpy as np
import pyaudio
import threading
import time

# Set up the main window with CTk
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class AudioVisualizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Audio Visualizer")
        self.geometry("800x600")

        # Create a canvas for the visualizer
        self.canvas = ctk.CTkCanvas(self, bg=self.cget("bg"), width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Create buttons for control
        self.start_button = ctk.CTkButton(self, text="Start Visualizer", command=self.start_visualizer)
        self.start_button.pack(pady=10)

        self.stop_button = ctk.CTkButton(self, text="Stop Visualizer", command=self.stop_visualizer)
        self.stop_button.pack(pady=10)

        self.running = False
        self.audio_thread = None

    def start_visualizer(self):
        if not self.running:
            self.running = True
            self.audio_thread = threading.Thread(target=self.update_visualizer)
            self.audio_thread.start()

    def stop_visualizer(self):
        self.running = False
        if self.audio_thread:
            self.audio_thread.join()

    def update_visualizer(self):
        # Set up audio stream with PyAudio
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

        while self.running:
            # Read audio data from the stream
            data = np.frombuffer(stream.read(1024), dtype=np.int16)

            # Clear the canvas for new drawing
            self.canvas.delete("all")

            # Draw the waveform on the canvas
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            x_scale = width / len(data)
            y_scale = height / 32768  # Scale factor for visualizing

            # Create points for the waveform
            points = []
            for i, value in enumerate(data):
                x = i * x_scale
                y = height / 2 - value * y_scale  # Center the waveform vertically
                points.append(x)
                points.append(y)

            # Draw the waveform
            self.canvas.create_line(points, fill="cyan", smooth=True)

            time.sleep(0.05)  # Refresh rate

        stream.stop_stream()
        stream.close()
        p.terminate()

# Run the app
if __name__ == "__main__":
    app = AudioVisualizerApp()
    app.mainloop()
