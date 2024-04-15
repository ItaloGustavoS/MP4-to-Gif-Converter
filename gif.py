import imageio
from glob import glob
from tqdm import tqdm
from typing import List

def convert_files(input_dir, output_dir, output_format):
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
                fps = reader.get_meta_data()['fps']
                total_frames = len(reader)

                with imageio.get_writer(outputpath, fps=fps) as writer:
                    for i, im in enumerate(tqdm(reader, total=total_frames)):
                        writer.append_data(im)

            print(f"Conversion completed for {os.path.basename(inputpath)}")

    except FileNotFoundError as e:
        print(f"\nError: {str(e)}")
    except Exception as e:
        print(f"\nUnknown error: {str(e)}")

# Example usage:
input_directory = os.path.dirname(__file__)
output_directory = os.path.join(input_directory, 'output')
convert_files(input_directory, output_directory, '.gif')
