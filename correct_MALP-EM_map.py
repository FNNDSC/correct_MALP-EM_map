#!/usr/bin/env python
import argparse
import os
import sys
import nibabel as nib
import numpy as np

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Corrects a MALP-EM label map by adding a CSF label on unlabelled voxels and on the cerebellar cortex.',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--nifti-t1w', dest='nifti_t1w_file', required=True, help='Path to Nifti input file of MALP-EM labelling.')
    parser.add_argument('--nifti-malpem-input', dest='nifti_malpem_input_file', required=True, help='Path to Nifti input file of MALP-EM labelling.')
    parser.add_argument('--nifti-mask', dest='nifti_mask_file', required=True, help='Path to Nifti input file of the brain mask.')
    parser.add_argument('--nifti-malpem-output', dest='nifti_output_malpem_file', required=False, default=None, help='Path to Nifti output file of corrected MALP-EM labelling.')
    args = parser.parse_args()

    csf_label = 18
    cerebellar_labels = [10, 11, 12, 13, 36, 37, 38]

    nifti_t1w_file = args.nifti_t1w_file
    nifti_malpem_input_file = args.nifti_malpem_input_file
    nifti_mask_file = args.nifti_mask_file
    nifti_output_malpem_file = args.nifti_output_malpem_file

    nii_t1w = nib.load(nifti_t1w_file)
    nii_malpem = nib.load(nifti_malpem_input_file)
    nii_mask = nib.load(nifti_mask_file)

    t1w_data = nii_t1w.get_data().flatten()
    malpem_data = nii_malpem.get_data().flatten()
    mask_data = nii_mask.get_data().flatten()

    is_fourth_ventricle_voxel = (malpem_data == 2)
    threshold = np.percentile(t1w_data[is_fourth_ventricle_voxel], 90)

    is_foreground_voxel = (mask_data == 1)
    is_unlabeled_voxel = (malpem_data == 0)
    is_low_t1w = (t1w_data <= threshold)
    is_cerebellar_voxel = np.array([item in cerebellar_labels for item in malpem_data])
    is_incorrect_cerebellar_label_voxel = (is_low_t1w & is_cerebellar_voxel)
    is_csf_voxel = is_foreground_voxel & (is_incorrect_cerebellar_label_voxel | is_unlabeled_voxel)

    malpem_data[is_csf_voxel] = csf_label

    nii_out = nib.nifti1.Nifti1Image(malpem_data.reshape(nii_malpem.get_data().shape), None, header=nii_malpem.header)
    nib.save(nii_out, nifti_output_malpem_file)
