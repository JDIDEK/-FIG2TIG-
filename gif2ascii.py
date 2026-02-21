import os
import sys
import time
import json
import argparse
from PIL import Image

# Enable ANSI escape codes on Windows
if os.name == 'nt':
    os.system("")

# ASCII character palette (from empty/dark to dense/light)
ASCII_CHARS = [" ", ".", ",", ":", ";", "+", "*", "?", "%", "#", "@"]

# Standard RGB color mapping for solid color modes
COLORS = {
    "red": (255, 50, 50),
    "green": (50, 255, 50),
    "blue": (50, 150, 255),
    "yellow": (255, 255, 50),
    "cyan": (50, 255, 255),
    "magenta": (255, 50, 255)
}

def process_frame(image, width=80, color_mode=None, threshold=30, is_html=False):
    """
    Converts a single PIL Image frame to an ASCII string.
    Handles resizing, transparency, thresholding, and color application.
    """
    img_width, img_height = image.size
    
    # Adjust height to account for terminal font aspect ratio (~0.55)
    height = int((img_height / img_width) * width * 0.55)
    img = image.resize((width, height)).convert("RGBA")
    pixels = img.getdata()
    
    lines = []
    current_line = []
    
    for i, (r, g, b, a) in enumerate(pixels):
        # Treat transparent pixels or dark pixels (below threshold) as empty space
        if a < 128 or (r < threshold and g < threshold and b < threshold):
            char = " "
        else:
            # Calculate perceived luminance to pick the right ASCII character
            luminance = int(0.299 * r + 0.587 * g + 0.114 * b)
            char_idx = min(int((luminance / 255) * len(ASCII_CHARS)), len(ASCII_CHARS) - 1)
            char = ASCII_CHARS[char_idx]
            
            # Apply original pixel colors if requested
            if color_mode == "original":
                if is_html:
                    char = f"<span style='color: rgb({r},{g},{b})'>{char}</span>"
                else:
                    char = f"\033[38;2;{r};{g};{b}m{char}\033[0m"
                    
        current_line.append(char)
        
        # End of the current image row
        if (i + 1) % width == 0:
            lines.append("".join(current_line))
            current_line = []
            
    # Join lines based on the target format
    line_separator = "<br>\n" if is_html else "\n"
    frame_str = line_separator.join(lines)
    
    # Apply a solid color to the entire frame if a specific color was chosen
    if color_mode in COLORS:
        r, g, b = COLORS[color_mode]
        if is_html:
            frame_str = f"<div style='color: rgb({r},{g},{b});'>\n{frame_str}\n</div>"
        else:
            frame_str = f"\033[38;2;{r};{g};{b}m{frame_str}\033[0m"
            
    return frame_str

def extract_frames(gif_path, width, color_mode, threshold, is_html=False):
    """
    Iterates through a GIF file and extracts all frames as ASCII strings.
    """
    try:
        img = Image.open(gif_path)
    except IOError:
        sys.exit(f"Error: Cannot open or read the file '{gif_path}'.")

    frames = []
    try:
        while True:
            ascii_frame = process_frame(img, width, color_mode, threshold, is_html)
            frames.append(ascii_frame)
            img.seek(img.tell() + 1)
    except EOFError:
        pass # Reached the end of the GIF
        
    return frames

def play_in_terminal(frames, fps):
    """
    Loops the ASCII frames in the terminal window.
    """
    clear_cmd = 'cls' if os.name == 'nt' else 'clear'
    delay = 1.0 / fps
    
    print("Starting animation... Press Ctrl+C to stop.")
    time.sleep(1)
    
    try:
        while True:
            for frame in frames:
                os.system(clear_cmd)
                sys.stdout.write(frame + "\n")
                sys.stdout.flush()
                time.sleep(delay)
    except KeyboardInterrupt:
        print("\nAnimation stopped by user.")

def export_single_txt(frames, output_path):
    """
    Writes all frames sequentially into a single text file.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        for i, frame in enumerate(frames):
            f.write(f"--- FRAME {i+1} ---\n")
            f.write(frame + "\n\n")
    print(f"Exported successfully to: {output_path}")

def export_directory(frames, output_dir):
    """
    Writes each frame into its own text file inside a specified directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    for i, frame in enumerate(frames):
        file_path = os.path.join(output_dir, f"frame_{i+1:03d}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(frame + "\n")
    print(f"Exported {len(frames)} frames to directory: {output_dir}/")

def export_html(frames, output_path, fps):
    """
    Generates a standalone HTML file containing a JavaScript loop to animate the frames.
    """
    delay_ms = int(1000 / fps)
    frames_json = json.dumps(frames)
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ASCII Art Animation</title>
    <style>
        body {{ background-color: #000; color: #fff; text-align: center; padding-top: 50px; }}
        #ascii-container {{
            font-family: monospace;
            white-space: pre;
            line-height: 10px;
            font-size: 10px;
            display: inline-block;
            text-align: left;
        }}
    </style>
</head>
<body>
    <div id="ascii-container"></div>
    <script>
        const frames = {frames_json};
        let currentFrame = 0;
        const container = document.getElementById('ascii-container');
        
        setInterval(() => {{
            container.innerHTML = frames[currentFrame];
            currentFrame = (currentFrame + 1) % frames.length;
        }}, {delay_ms});
    </script>
</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"HTML export successful: {output_path}")

def print_animated_guide():
    """
    Prints the welcome guide with a colorful, line-by-line animation effect.
    """
    # List of tuples: (ANSI color code, text line)
    lines = [
        ("\033[96m", "=================================================="), # Light Cyan
        ("\033[93m", "          🎨 GIF to ASCII Art Converter 🎨"),       # Light Yellow
        ("\033[96m", "=================================================="),
        ("", ""),
        ("\033[91m", "Oops! You need to provide a GIF file to convert."),  # Light Red
        ("", ""),
        ("\033[92m", "👉 BASIC USAGE:"),                                    # Light Green
        ("\033[0m",  "   python gif2ascii.py animation.gif"),             # Reset (Default terminal color)
        ("", ""),
        ("\033[95m", "🌟 COOL EXAMPLES:"),                                  # Light Magenta
        ("\033[90m", "   # Play in the terminal with Matrix-style green text:"), # Dark Gray
        ("\033[0m",  "   python gif2ascii.py animation.gif -c green"),
        ("", ""),
        ("\033[90m", "   # Play in the terminal keeping original GIF colors:"),
        ("\033[0m",  "   python gif2ascii.py animation.gif -c original -w 100"),
        ("", ""),
        ("\033[90m", "   # Export as a colorful animated webpage:"),
        ("\033[0m",  "   python gif2ascii.py animation.gif -c original --export-html index.html"),
        ("", ""),
        ("\033[90m", "   # Extract every single frame into a directory:"),
        ("\033[0m",  "   python gif2ascii.py animation.gif --export-dir my_frames"),
        ("", ""),
        ("\033[94m", "For a complete list of options, use the help flag:"), # Light Blue
        ("\033[0m",  "   python gif2ascii.py --help"),
        ("\033[96m", "=================================================="),
        ("\033[0m",  "") # Final reset to ensure terminal goes back to normal
    ]

    for color_code, text in lines:
        # Apply color if specified, print the text, and flush to terminal immediately
        sys.stdout.write(f"{color_code}{text}\n")
        sys.stdout.flush()
        # Small delay to create the animation effect
        time.sleep(0.04)

def main():
    # If the user runs the script without any arguments, show a friendly guide
    if len(sys.argv) == 1:
        print_animated_guide()
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Convert animated GIFs to ASCII Art.")
    parser.add_argument("input", help="Path to the source GIF file.")
    parser.add_argument("-w", "--width", type=int, default=80, help="Output width in characters (default: 80).")
    parser.add_argument("-f", "--fps", type=int, default=15, help="Playback speed in frames per second (default: 15).")
    parser.add_argument("-t", "--threshold", type=int, default=30, help="Darkness threshold to treat as background (default: 30).")
    parser.add_argument("-c", "--color", type=str, choices=["original"] + list(COLORS.keys()), help="Text color mode (e.g., green, red, original).")
    
    # Output options
    parser.add_argument("--export-txt", type=str, metavar="FILE", help="Export all frames into a single text file.")
    parser.add_argument("--export-dir", type=str, metavar="DIR", help="Export each frame as a separate text file in a directory.")
    parser.add_argument("--export-html", type=str, metavar="FILE", help="Generate an animated HTML page.")
    
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        sys.exit(f"Error: The file '{args.input}' does not exist.")

    print(f"Processing '{args.input}'...")
    
    is_html = bool(args.export_html)
    frames = extract_frames(args.input, args.width, args.color, args.threshold, is_html)
    
    if not frames:
        sys.exit("No frames could be extracted.")

    # Route to the requested output method
    if args.export_html:
        export_html(frames, args.export_html, args.fps)
    elif args.export_txt:
        export_single_txt(frames, args.export_txt)
    elif args.export_dir:
        export_directory(frames, args.export_dir)
    else:
        play_in_terminal(frames, args.fps)

if __name__ == "__main__":
    main()