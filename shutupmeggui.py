import tkinter as tk
from tkinter import filedialog

def extract_files(megmid):
    with open(megmid, 'rb') as file:
        data = file.read()

    file_start_pattern1 = b'\xF2\x0D\xC9\x48\x61\x60\x60\x60\x63'
    file_start_pattern2 = b'\xF3\x0D\xC9\x48\x61\x60\x60\x60\x63'

    file_start_index = 0
    file_number = 1

    while file_start_index < len(data):
        start_offset1 = data.find(file_start_pattern1, file_start_index)
        start_offset2 = data.find(file_start_pattern2, file_start_index)

        if start_offset1 == -1 and start_offset2 == -1:
            break

        if start_offset1 == -1 or (start_offset2 != -1 and start_offset2 < start_offset1):
            start_offset = start_offset2
        else:
            start_offset = start_offset1

        next_start_offset1 = data.find(file_start_pattern1, start_offset + 1)
        next_start_offset2 = data.find(file_start_pattern2, start_offset + 1)

        next_start_offset = min(offset for offset in [next_start_offset1, next_start_offset2] if offset != -1)

        end_offset = next_start_offset if next_start_offset != -1 else len(data)

        file_content = data[start_offset:end_offset]
        with open(f"{file_number}.pop", 'wb') as output_file:
            output_file.write(file_content)

        file_start_index = end_offset
        file_number += 1

    print(f"{file_number - 1} files extracted successfully.")

def browse_file():
    file_path = filedialog.askopenfilename(title="Select File")
    entry_path.delete(0, tk.END)
    entry_path.insert(0, file_path)

def start_extraction():
    file_path = entry_path.get()
    extract_files(file_path)

# Create the main window
root = tk.Tk()
root.title("File Extraction GUI")

# Create and place widgets
label_path = tk.Label(root, text="Select File:")
label_path.grid(row=0, column=0, padx=10, pady=10)

entry_path = tk.Entry(root, width=50)
entry_path.grid(row=0, column=1, padx=10, pady=10)

button_browse = tk.Button(root, text="Browse", command=browse_file)
button_browse.grid(row=0, column=2, padx=10, pady=10)

button_extract = tk.Button(root, text="Extract Files", command=start_extraction)
button_extract.grid(row=1, column=1, pady=20)

# Run the main loop
root.mainloop()
