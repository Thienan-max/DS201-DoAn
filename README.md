# Deep Learning for Data Science Project - Dataset Processing

This repository contains the data processing pipeline for our Deep Learning for Data Science course project. It includes scripts for downloading, cleaning, filtering, resizing, and validating the dataset.

## Scripts Overview

1. `download_and_clean.py`: Downloads the initial dataset and performs basic cleaning.
2. `filter_data.py`: Filters the dataset based on specific criteria.
3. `filter_columns.py`: Selects and cleans necessary columns from the metadata.
4. `resize_images.py`: Resizes images to the required resolution for deep learning models.
5. `sanity_check.py`: Performs final validation on the dataset (checking for corrupted images, cleaning HTML/junk characters, and verifying data synchronization).

## Dataset

The final processed dataset (consisting of `resized_images` and `final_metadata`) has been uploaded to Kaggle. The `data/` directory is excluded from this repository to avoid pushing large files to GitHub.

## Requirements

- Python 3.x
- PIL (Pillow)
- pandas
- requests (if applicable)

## Usage

Run the scripts in the numerical order specified above to replicate the dataset processing pipeline.
