import os
import sys
import imageio
import cv2  # Import cv2 for resizing
from glob import glob
from tqdm import tqdm
from typing import List
import pathlib # For creating dummy file

def convert_files(input_dir, output_dir, output_format, width=None, output_fps=10):  # Add width and output_fps
    """Converts video files from an input directory to a specified format in an output directory.

    Args:
        input_dir (str): Directory containing input video files (.mp4, .avi).
        output_dir (str): Directory where converted files will be saved.
        output_format (str): The desired output format (e.g., '.gif').
        width (int, optional): The desired width of the output GIF in pixels.
                               If provided, frames will be resized while maintaining
                               aspect ratio. Defaults to None (no resizing).
        output_fps (int, optional): The frame rate for the output GIF.
                                    Defaults to 10.
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # List all video files in the input directory
        video_files = glob(os.path.join(input_dir, '*.mp4')) + glob(os.path.join(input_dir, '*.avi'))

        for inputpath in video_files:
            # Generate output file path based on the input file path
            outputpath = os.path.join(output_dir, os.path.splitext(os.path.basename(inputpath))[0] + output_format)

            print(f"Converting {inputpath} to {outputpath}")

            with imageio.get_reader(inputpath) as reader:
                # fps = reader.get_meta_data()['fps'] # Remove old fps calculation
                total_frames = len(reader)

                with imageio.get_writer(outputpath, fps=output_fps) as writer:  # Use output_fps
                    for i, im in enumerate(tqdm(reader, total=total_frames)):
                        if width is not None:
                            aspect_ratio = im.shape[0] / im.shape[1]
                            height = int(width * aspect_ratio)
                            im = cv2.resize(im, (width, height))
                        writer.append_data(im)

            print(f"Conversion completed for {os.path.basename(inputpath)}")

    except FileNotFoundError as e:
        print(f"\nError: {str(e)}")
    except Exception as e:
        print(f"\nUnknown error: {str(e)}")

# Example usage:
# Create dummy directories and file for testing
dummy_input_dir = "dummy_input"
dummy_output_dir = "dummy_output"
os.makedirs(dummy_input_dir, exist_ok=True)
os.makedirs(dummy_output_dir, exist_ok=True)
pathlib.Path(os.path.join(dummy_input_dir, "test_video.mp4")).touch()

# Original usage (default fps, no resizing)
# input_directory = os.path.dirname(__file__)
# output_directory = os.path.join(input_directory, 'output')
# convert_files(input_directory, output_directory, '.gif')

# Example with resizing to 320px width and default 10 FPS
# convert_files(input_directory, output_directory, '.gif', width=320)

# Example with resizing to 240px width and 15 FPS
# convert_files(input_directory, output_directory, '.gif', width=240, output_fps=15)

# Dry run test call
print("Starting dry run test...")
convert_files(dummy_input_dir, dummy_output_dir, '.gif', width=100, output_fps=5)
print("Dry run test finished.")
