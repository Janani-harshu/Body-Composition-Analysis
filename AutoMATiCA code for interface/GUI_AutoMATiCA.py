"""
Copyright

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files 
(the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, 
publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import AutoMATiCA_source_GUI
from PIL import Image, ImageTk

global muscle_HU_range
muscle_HU_range = (-29, 150)
global IMAT_SAT_HU_range
IMAT_SAT_HU_range = (-190, -30)
global VAT_HU_range
VAT_HU_range = (-150, -50)

##These functions are called to select directories for pulling CT scans, saving analyzed scans, and saving results files
def get_CT_directory():
    global folder_path_CT
    filename_CT = filedialog.askdirectory()
    folder_path_CT.set(filename_CT)

def get_image_save_directory():
    global folder_path_image
    filename_save = filedialog.askdirectory()
    folder_path_image.set(filename_save)
    
def get_results_directory():
    global folder_path_results
    filename_results = filedialog.askdirectory()
    folder_path_results.set(filename_results)


##Used to scroll left and right through the analyzed images
def left(CT_display, RGB_img, overlay, CT_label, overlay_label, Patient_id,string_id,patient_id_label):
    global curr_index
    curr_index-=1
    if curr_index<-CT_display.shape[0]+1:
        curr_index=0
    
    CT_img = ImageTk.PhotoImage(Image.fromarray(CT_display[curr_index]))
    overlay_img = ImageTk.PhotoImage(Image.fromarray(overlay[curr_index]))
    
    CT_label.configure(image = CT_img)
    CT_label.image = CT_img  
    
    overlay_label.configure(image = overlay_img)
    overlay_label.image = overlay_img  
    
    string_id.set('Patient ID: ' + Patient_id[curr_index])
    
    
def right(CT_display, RGB_img, overlay, CT_label, overlay_label, Patient_id, string_id,patient_id_label):
    global curr_index
    curr_index+=1
    if curr_index>CT_display.shape[0]-1:
        curr_index=0
    
    CT_img = ImageTk.PhotoImage(Image.fromarray(CT_display[curr_index]))
    overlay_img = ImageTk.PhotoImage(Image.fromarray(overlay[curr_index]))
    
    CT_label.configure(image = CT_img)
    CT_label.image = CT_img

    overlay_label.configure(image = overlay_img)
    overlay_label.image = overlay_img  
    
    string_id.set('Patient ID: ' + Patient_id[curr_index])


#used for updating muscle, IMAT, VAT, and SAT HU ranges (see set_HU_range)
def return_HU_range():
    global muscle_HU_range
    muscle_HU_range = (int(muscle_low.get()), int(muscle_high.get()))
    global IMAT_SAT_HU_range
    IMAT_SAT_HU_range = (int(IMAT_low.get()), int(IMAT_high.get()))
    global VAT_HU_range
    VAT_HU_range = (int(VAT_low.get()), int(VAT_high.get()))

    window.destroy()
    
##creates a new window to update HU ranges
def set_HU_range():
    global window
    window = Toplevel(root)
    window.iconbitmap('C:\\Users\\Harshini\\Desktop\\BCA\\BCA_implementation\\AutoMATiCA code for interface\\image\\Logo.ico')
    
    Label(window, text="Muscle HU lower boundary").grid(row=0, column=0, sticky=(N,S,E,W), columnspan=1, rowspan=1)
    global muscle_low
    muscle_low = Entry(window)
    muscle_low.insert(0, -29)
    muscle_low.grid(row=0, column=1, sticky=(N,S,E,W), columnspan=1, rowspan=1)
    
    Label(window, text="Muscle HU upper boundary").grid(row=0, column=2, sticky=(N,S,E,W), columnspan=1, rowspan=1)
    global muscle_high
    muscle_high = Entry(window)
    muscle_high.insert(0, 150)
    muscle_high.grid(row=0, column=3, sticky=(N,S,E,W), columnspan=1, rowspan=1)
    
    Label(window, text="IMAT and SAT HU lower boundary").grid(row=1, column=0, sticky=(N,S,E,W), columnspan=1, rowspan=1)
    global IMAT_low
    IMAT_low = Entry(window)
    IMAT_low.insert(0, -190)
    IMAT_low.grid(row=1, column=1, sticky=(N,S,E,W), columnspan=1, rowspan=1)
    
    Label(window, text="IMAT and SAT HU upper boundary").grid(row=1, column=2, sticky=(N,S,E,W), columnspan=1, rowspan=1)
    global IMAT_high
    IMAT_high = Entry(window)
    IMAT_high.insert(0, -30)
    IMAT_high.grid(row=1, column=3, sticky=(N,S,E,W), columnspan=1, rowspan=1)
    
    Label(window, text="VAT HU lower boundary").grid(row=2, column=0, sticky=(N,S,E,W), columnspan=1, rowspan=1)
    global VAT_low
    VAT_low = Entry(window)
    VAT_low.insert(0, -150)
    VAT_low.grid(row=2, column=1, sticky=(N,S,E,W), columnspan=1, rowspan=1)
    
    Label(window, text="VAT HU upper boundary").grid(row=2, column=2, sticky=(N,S,E,W), columnspan=1, rowspan=1)
    global VAT_high
    VAT_high = Entry(window)
    VAT_high.insert(0, -50)
    VAT_high.grid(row=2, column=3, sticky=(N,S,E,W), columnspan=1, rowspan=1)
    
    window.grid_rowconfigure(4, minsize=30)
    
    okay_button = ttk.Button(window, text = 'Confirm', command= return_HU_range)
    okay_button.grid(row=5, column=1, sticky=(N,S,E,W), columnspan=2, rowspan=1)
    
##performs segmentation 
def run(DisplayVar, ImageVar, ResultsVar, folder_path_CT, folder_path_image, folder_path_results):
    
    dicom_l3_filepath = AutoMATiCA_source_GUI.generate_CT_filepaths(folder_path_CT.get())

    CT_HU, CT_fat_HU, CT_lean_HU, CT_VAT_HU, pred_muscle, pred_IMAT, pred_VAT, pred_SAT, CT_pixel_spacing, CT_image_dimensions, CT_voltage, CT_current, CT_date, CT_slice_thickness, Patient_id, Patient_age, Patient_sex, dicom_l3_filepath, removed_scans = AutoMATiCA_source_GUI.segmentation_prediction(dicom_l3_filepath, muscle_model, IMAT_model, VAT_model, SAT_model, muscle_HU_range, VAT_HU_range, IMAT_SAT_HU_range, batch_size = 1)
    combined_map = AutoMATiCA_source_GUI.combine_segmentation_predictions(CT_fat_HU, CT_lean_HU, CT_VAT_HU, pred_VAT, pred_SAT, pred_IMAT, pred_muscle)
     
    if ImageVar.get() == 1:
        AutoMATiCA_source_GUI.save_segmentation_image(CT_HU, combined_map, Patient_id, save_directory = folder_path_image.get())

    muscle_CSA, IMAT_CSA, VAT_CSA, SAT_CSA = AutoMATiCA_source_GUI.CSA_analysis(combined_map, CT_pixel_spacing, CT_image_dimensions)
    muscle_HU, IMAT_HU, VAT_HU, SAT_HU = AutoMATiCA_source_GUI.HU_analysis(combined_map, CT_HU)
    
    if ResultsVar.get() ==1:
        AutoMATiCA_source_GUI.save_results_to_excel(Patient_id, Patient_age, Patient_sex, muscle_CSA, IMAT_CSA, VAT_CSA, SAT_CSA, muscle_HU, IMAT_HU, VAT_HU, SAT_HU, CT_pixel_spacing, CT_image_dimensions, CT_voltage, CT_current, CT_date, CT_slice_thickness, dicom_l3_filepath, folder_path_results.get(), removed_scans)

    print('analysis completed')
    
    if DisplayVar.get() == 1:

        overlay, RGB_img, CT_display = AutoMATiCA_source_GUI.display_segmentation(CT_HU, combined_map, Patient_id)

        popup = Toplevel(root)
        popup.iconbitmap('C:\\Users\\Harshini\\Desktop\\BCA\\BCA_implementation\\AutoMATiCA code for interface\\image\\Logo.ico')
        
        pop_frame = ttk.Frame(popup, borderwidth=5, relief="sunken", width=300, height=150)
        pop_frame.grid(row=1, column=0, sticky=(N,S,E,W), columnspan=1, rowspan=1)
        
        CT_img = ImageTk.PhotoImage(Image.fromarray(CT_display[curr_index]))
        overlay_img = ImageTk.PhotoImage(Image.fromarray(overlay[curr_index]))
        
        CT_label = ttk.Label(pop_frame)
        CT_label['image'] = CT_img
        CT_label.grid(row=0, column=0, sticky=(N,S,E,W), columnspan=1, rowspan=1)

        overlay_label = ttk.Label(pop_frame)
        overlay_label['image'] = overlay_img
        overlay_label.grid(row=0, column=2, sticky=(N,S,E,W), columnspan=1, rowspan=1)
        
        popup.columnconfigure(0, weight=1)
        popup.rowconfigure(0, weight=1)
   
        string_id = StringVar()
        patient_id_label = ttk.Label(popup, textvariable=string_id)
        patient_id_label.grid(row=0, column =0, sticky=(N,S,E,W), columnspan=2, rowspan=1)
        
        arrow_bar= Label(popup, text="press left and right arrow keys to scroll through scans", bd=1, relief=SUNKEN, anchor=W)
        arrow_bar.grid(row=2, column=0, sticky=(N,S,E,W))
        
        popup.bind('<Left>', lambda x: left(CT_display, RGB_img, overlay, CT_label, overlay_label, Patient_id, string_id, patient_id_label))
        popup.bind('<Right>', lambda x: right(CT_display, RGB_img, overlay, CT_label, overlay_label, Patient_id, string_id, patient_id_label))
        

root = Tk()
root.title('Automated BCA')

curr_index = 0

menu = Menu(root) 
root.config(menu=menu)

DisplayVar = IntVar()
ImageVar = IntVar()
ResultsVar = IntVar()
folder_path_CT = StringVar()
folder_path_image = StringVar()
folder_path_results = StringVar()

#create toolbar
toolbar = ttk.Frame(root, borderwidth=5, relief="sunken", width=200, height=100)
CTButton = ttk.Button(toolbar, text="1) Load CT scans for analysis", command = get_CT_directory)
CTButton.grid(row=0, column=0, sticky=(N,S,E,W), columnspan=1, rowspan=1)
ImageButton= ttk.Button(toolbar, text="2) Location for saving images", command=get_image_save_directory)
ImageButton.grid(row=0, column=1, sticky=(N,S,E,W), columnspan=1, rowspan=1)
ResultsButton= ttk.Button(toolbar, text="3) Location for saving results", command=get_results_directory)
ResultsButton.grid(row=0, column=2, sticky=(N,S,E,W), columnspan=1, rowspan=1)

DisplaySegBox = ttk.Checkbutton(toolbar, text='Display segmentation',  variable = DisplayVar)
DisplaySegBox.grid(row=2, column=0)
SaveDisplayBox = ttk.Checkbutton(toolbar, text='Save images', variable = ImageVar)
SaveDisplayBox.grid(row=2, column=1)
SaveResultsBox = ttk.Checkbutton(toolbar, text='Save results of segmentation', variable = ResultsVar)
SaveResultsBox.grid(row=2, column=2)
toolbar.grid(rows=1, column=0, sticky=(N,S,E,W), columnspan=1, rowspan=1)

RunButton = ttk.Button(toolbar, text = 'Perform segmentation', command= lambda: run(DisplayVar, ImageVar, ResultsVar, folder_path_CT, folder_path_image, folder_path_results))
RunButton.grid(row=4, column=1, sticky=(N,S,E,W), columnspan=1, rowspan=1)

#Create status bar
usage = Label(root, text='How to use:',bd=1, relief=SUNKEN, anchor=W)
usage.grid(row=1, column=0, sticky=(N,S,E,W))
statusbar= Label(root, text="1) Select CT scan location, 2) Select location for saving images, 3) Select location for saving results", bd=1, relief=SUNKEN, anchor=W)
statusbar.grid(row=2, column=0, sticky=(N,S,E,W))
statusbar1= Label(root, text="4) Check operations to be performed, 5) When ready, click 'Perform segmentation'", bd=1, relief=SUNKEN, anchor=W)
statusbar1.grid(row=3, column=0, sticky=(N,S,E,W))
statusbar2= Label(root, text="6) Optional: Adjust HU threshold ranges for customized CSA analysis", bd=1, relief=SUNKEN, anchor=W)
statusbar2.grid(row=4, column=0, sticky=(N,S,E,W))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
toolbar.columnconfigure(0, weight=1)
toolbar.columnconfigure(1, weight=1)
toolbar.columnconfigure(2, weight=1)

HU_adjustment_button = ttk.Button(toolbar, text="Optional: Adjust HU ranges", command = set_HU_range)
HU_adjustment_button.grid(row=3, column=1, sticky=(N,S,E,W), columnspan=1, rowspan=1)

muscle_model, IMAT_model, VAT_model, SAT_model = AutoMATiCA_source_GUI.load_models('..//Tensorflow Models')

root.iconbitmap('C:\\Users\\Harshini\\Desktop\\BCA\\BCA_implementation\\AutoMATiCA code for interface\\image\\Logo.ico')

root.mainloop()
