import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfMerger
from PIL import Image
from reportlab.pdfgen import canvas

# Function to merge PDF files
def merge_pdf(files, output_file):
    merger = PdfMerger()
    for file in files:
        merger.append(file)
    merger.write(output_file)
    merger.close()

# Function to convert images to PDF maintaining the original form
def convert_and_merge_images(images, output_file):
    first_img = Image.open(images[0])
    full_width, full_height = first_img.size
    first_img.close()

    pdf_canvas = canvas.Canvas(output_file, pagesize=(full_width, full_height))
    
    for img_path in images:
        img = Image.open(img_path)
        width, height = img.size

        # Adjust the PDF canvas size to match the original image size
        pdf_canvas.setPageSize((width, height))

        pdf_canvas.drawImage(img_path, 0, 0, width=width, height=height)
        pdf_canvas.showPage()
        img.close()

    pdf_canvas.save()

# Function to handle file selection and output location
def browse_files(type):
    filetypes = ()
    if type == "PDF":
        filetypes = (("PDF files", "*.pdf"), ("All files", "*.*"))
    elif type == "Image":
        filetypes = (("Image files", "*.jpg *.png *.gif *.bmp"), ("All files", "*.*"))

    files = filedialog.askopenfilenames(title="Select Files", filetypes=filetypes)
    
    if len(files) > 0:
        output_file = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                   filetypes=(("PDF files", "*.pdf"), ("All files", "*.*")), 
                                                   title="Save As")
        if output_file:
            if type == "PDF":
                # If the selected type is PDF, merge the selected PDF files
                merge_pdf(files, output_file)
            elif type == "Image":
                # If the selected type is Image, convert and merge the selected images to PDF
                convert_and_merge_images(files, output_file)


# Function to exit the application
def exit_app():
    root.destroy()

# GUI configuration
root = tk.Tk()
root.title("Document Merger")
root.geometry("300x150")  # Change the window size
root.configure(bg="lightgray")  # Change the window background color

type_label = tk.Label(root, text="Select Document Type:", bg="lightgray")  # Change the background color of the label
type_label.pack(pady=10)  # Add vertical space between the label and the buttons

# Change button shape, color, center them horizontally, and set text in bold
button_font = ("Arial", 10, "bold")
pdf_button = tk.Button(root, text="Merge PDF", command=lambda: browse_files("PDF"), bg="blue", fg="white", font=button_font, relief="raised")
pdf_button.pack(side='left', padx=10)  # Align the button to the left and add horizontal space between the buttons

convert_button = tk.Button(root, text="Convert to PDF", command=lambda: browse_files("Image"), bg="green", fg="white", font=button_font, relief="raised")
convert_button.pack(side='left', padx=10)  # Align the button to the left and add horizontal space between the buttons

exit_button = tk.Button(root, text="Exit", command=exit_app, bg="red", fg="white", font=button_font, relief="raised")
exit_button.pack(side='left', padx=10)  # Align the button to the left and add horizontal space between the buttons

# Comment indicating the creator of the program
comment_label = tk.Label(root, text="Created by: Cesar Carrion A.", bg="lightgray", font=("Arial", 8,"bold"))
comment_label.place(relx=0.5, rely=1.0, anchor="s")  # Position the comment at the bottom, center horizontally

root.mainloop()