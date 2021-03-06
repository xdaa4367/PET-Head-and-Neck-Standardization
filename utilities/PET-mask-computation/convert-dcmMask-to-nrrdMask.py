"""
This script converts RTStruct-dcm-files (RTStruct-files = masks) to RTStruct-nrrd-files using plastimatch.
https://www.plastimatch.org/
"""


import os
import numpy as np
import nrrd

# Path to directory with RT-Structure file and corresponding Dicom-files
path = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/Head-Neck-PET-CT/Separated_Centers_PET_RTStruct'

# Path to destination folder
dst_path = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/Head-Neck-PET-CT/Plastimatch_Output'

# Command for terminal -> plastimatch
convert = 'plastimatch convert --input {} --output-prefix {} --prefix-format "nrrd"  --modality "PT"'

for cohort in sorted(os.listdir(path)):
    print(cohort)

    # Create folder for each cohort
    os.makedirs(os.path.join(dst_path, cohort), exist_ok=True)

    for patient in sorted(os.listdir(os.path.join(path, cohort))):

        # Create folder for each patient
        os.makedirs(os.path.join(dst_path, cohort, patient), exist_ok=True)

        # Define input path
        input_path = os.path.join(path, cohort, patient)

        # Define output path
        output_path = os.path.join(dst_path, cohort, patient)

        # Call terminal for conversion using plastimatch
        print('Converting Dicom files in nrrd Structure files')
        os.system(convert.format(input_path, output_path))
