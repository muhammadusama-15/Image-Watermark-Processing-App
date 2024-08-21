#Importing relevant packages/libraries
import customtkinter as ctk
from customtkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont


#Creating a global image name---will be used to save the end file
image_name = ""


#Defining a function to create a starting frame widgets
def create_starting_widgets():
    #Deleting old widgets, if any
    for widget in frame.winfo_children():
        widget.destroy()
    #Creating Labels and Buttons
    welcome_label = ctk.CTkLabel(master=frame,text="Welcome to the 'Image Watermark Processing' application.",font=("Calibri",20,"bold"))
    welcome_label.grid(row=0, column=0,columnspan=2)

    paragraph_label = ctk.CTkLabel(master=frame, text="Let others know your images/work by adding your watermark in just few steps.")
    paragraph_label.grid(row=1,column=0,columnspan=2,pady=20)

    browse_button = ctk.CTkButton(master=frame,text="Browse Image",command=browse_image)
    browse_button.grid(row=2,column=0,columnspan=2)


#Defining a function to browse images on button press
def browse_image():
    filetypes = [("Image files", "*.png;*.jpg;*.jpeg")]
    path = filedialog.askopenfilename(filetypes=filetypes)

    #if image is selected
    if len(path):
        global image_name
        image_name = path.split("/")[-1]
        image = Image.open(path)
        watermark_image = image.copy()
        path_label = ctk.CTkLabel(master=frame, text=f"Image Selected: {path}", font=("Arial",14,"bold"), text_color="red")
        path_label.grid(row=2, column=0, columnspan=2,padx=10)

        add_text_watermark_button = ctk.CTkButton(master=frame,text="Add Text Watermark",command=lambda:text_watermark(watermark_image))
        add_text_watermark_button.grid(row=3,column=0,pady=5)

        add_picture_watermark_button = ctk.CTkButton(master=frame,text="Add Picture Watermark",command=lambda:picture_watermark(watermark_image))
        add_picture_watermark_button.grid(row=3,column=1,pady=5)

        home_button = ctk.CTkButton(master=frame,text="Home",command=create_starting_widgets)
        home_button.grid(row=4,column=0,columnspan=2)


#Defining functions to add a text watermark---For adding your 'Brand Name'
def text_watermark(watermark_image):
    #Destroying all widgets in a frame
    for widget in frame.winfo_children():
        widget.destroy()
    #Creating new widgets
    text_entry = ctk.CTkEntry(master=frame, placeholder_text="What do you want to add as a watermark?",width=400)
    text_entry.focus()
    text_entry.grid(row=0,column=0,columnspan=2,pady=10,)
    submit_button = ctk.CTkButton(master=frame, text="Submit", command=lambda:add_text_watermark())
    submit_button.grid(row=1, column=0)
    home_button = ctk.CTkButton(master=frame,text="Home",command=create_starting_widgets)
    home_button.grid(row=1,column=1)

    def add_text_watermark():
        text = text_entry.get()
        if text != "":
            draw = ImageDraw.Draw(watermark_image)
            
            w, h = watermark_image.size #width and height of image
            x, y = int(w / 8), int(h / 8) #location to put the watermark
            if x > y:
                font_size = y
            elif y > x:
                font_size = x
            else:
                font_size = x
            
            #font typy and font size
            font = ImageFont.truetype("arial.ttf", int(font_size/5))
            
            # add Watermark
            # (0,0,0)-black color text
            draw.text((x, y), text=text, fill=(0, 0, 0), font=font, anchor='ms')
            watermark_image.show()

            if messagebox.askyesno(title="Save Image",message="Do you want to save this image."):
                watermark_image.save(f'Water Marked Images/{image_name}' )
                messagebox.showinfo(title="Image Saved", message="Image has been saved successfully in 'Water Marked Images'.")
            else:
                messagebox.showinfo(title="Image Not Saved", message="Image has not been saved.")

        else:
            messagebox.showinfo(title="Watermark text missing", message="Kindly enter the watermart text in the box.")


#Defining functions to add a picture watermark---For adding your 'Brand Logo'
def picture_watermark(watermark_image):
    filetypes = [("Image files", "*.png;*.jpg;*.jpeg")]
    logo_path = filedialog.askopenfilename(filetypes=filetypes)
    logo = Image.open(logo_path)
    logo_transparent = remove_background(logo=logo)
    
    w, h = watermark_image.size #width and height of image
    x, y = int(w / 10), int(h / 10) #location to put the watermark

    #Cropping the logo
    logo_transparent.thumbnail((h/10,h/10))
    watermark_image.paste(logo_transparent,(x,y))
    watermark_image.show()
    if messagebox.askyesno(title="Save Image",message="Do you want to save this image."):
        watermark_image.save(f'Water Marked Images/{image_name}' )
        messagebox.showinfo(title="Image Saved", message="Image has been saved successfully in 'Water Marked Images'.")
    else:
        messagebox.showinfo(title="Image Not Saved", message="Image has not been saved.")


#Defining a function to remove black background from images---Getting rid of transparent parts of the logo
def remove_background(logo):
    logo_transparent = logo.convert("RGBA")
    data = logo_transparent.getdata() 
    new_data = [] 
    for item in data: 
        if item[0] == 0 and item[1] == 0 and item[2] == 0:  # finding black colour by its RGB value 
            # storing a transparent value when we find a black colour 
            new_data.append((255, 255, 255, 0)) 
        else: 
            new_data.append(item)  # other colours remain unchanged 
    logo_transparent.putdata(new_data)
    return logo_transparent


#Creating a window for GUI Application
window = ctk.CTk()
window.title("Image Watermark Application")
window.minsize(height=500, width=500)


#Creating a frame
frame = ctk.CTkFrame(master=window, width=400, height=400)
frame.pack(padx=20, pady=20)
create_starting_widgets()


#Creating mainloop to run the application
window.mainloop()

