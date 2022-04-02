
"""
Example of how to use AutoMATiC Net
See specific comments above each function
"""


import AutoMATiCA

dicom_directory = "PATH TO DIRECTORY CONTAINING CT SCANS"
tensorflow_models_directory = "PATH TO DIRECTORY CONTAINING TENSORFLOW MODELS"
image_saving_directory = "PATH TO DIRECTORY TO SAVE IMAGES"
results_saving_directory = "PATH TO DIRECTORY TO SAVE RESULTS"



##use automated_CT_analysis.generate_CT_filepaths to create a list of CT file paths for analysis
##input parameter should be the directory containing the CT scans
##CT scans can have a .dcm file extension or no file extension
CT_filepaths = AutoMATiCA.generate_CT_filepaths(dicom_directory)
#
#this loads the neural networks for analysis
#input parameter should be the directory containing the models
#do not rename models, unless they are also updated in the source code
muscle_model, IMAT_model, VAT_model, SAT_model = AutoMATiCA.load_models(tensorflow_models_directory)

#performing the analysis and extracting CT parameters (i.e. voltage, patient ID, etc.)
#CT filepaths and 4 neural network models are used as input parameters
#HU ranges for prediction refine can be narrowed (i.e. muscle from -29 to 150 TO 30 to 150) but cannot be widened (i.e. -29 to 150 TO -50 to 200)
#Batch size indicates # of scans to be analyzed in parallel. For CPU analysis, set to 1 as it does not change speed of analysis. For GPU, increase batch size to increase speed, but will become memory limited at somepoint
CT_HU, CT_fat_HU, CT_lean_HU, CT_VAT_HU, pred_muscle, pred_IMAT, pred_VAT, pred_SAT, CT_pixel_spacing, CT_image_dimensions, CT_voltage, CT_current, CT_date, CT_slice_thickness, Patient_id, Patient_age, Patient_sex, CT_filepaths, removed_scans = AutoMATiCA.segmentation_prediction(CT_filepaths, muscle_model, IMAT_model, VAT_model, SAT_model, muscle_range = (-29, 150), VAT_range = (-150, -50), IMAT_SAT_range = (-190, -30), batch_size=1)

#combine the 4 predicted segmentation maps into one
#input is filtered CT scans and predicted segmentation maps
combined_map = AutoMATiCA.combine_segmentation_predictions(CT_fat_HU, CT_lean_HU, CT_VAT_HU, pred_VAT, pred_SAT, pred_IMAT, pred_muscle)

#this displays and saves the segmentation images
#input is raw CT scans, combined maps (overlayed on raw CT scan), patient id, and dir for saving images
#if there are a large number of scans being analzyed at once, displaying the output should be avoided
AutoMATiCA.display_segmentation(CT_HU, combined_map, Patient_id)
AutoMATiCA.save_segmentation_image(CT_HU, combined_map, Patient_id, save_directory = image_saving_directory)

#used for calcualting CSA and average HU for each tissue
#requires combined maps, CT pixel spacing and dimensions for calculations
muscle_CSA, IMAT_CSA, VAT_CSA, SAT_CSA = AutoMATiCA.CSA_analysis(combined_map, CT_pixel_spacing, CT_image_dimensions)
muscle_HU, IMAT_HU, VAT_HU, SAT_HU = AutoMATiCA.HU_analysis(combined_map, CT_HU)

#exports results into an excel file
#will need to update the directory for saving
AutoMATiCA.save_results_to_excel(Patient_id, Patient_age, Patient_sex, muscle_CSA, IMAT_CSA, VAT_CSA, SAT_CSA, muscle_HU, IMAT_HU, VAT_HU, SAT_HU, CT_pixel_spacing, CT_image_dimensions, CT_voltage, CT_current, CT_date, CT_slice_thickness, CT_filepaths, results_saving_directory, removed_scans)
