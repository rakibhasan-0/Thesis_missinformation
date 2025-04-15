import json
import os
import glob

def gather_and_remove_transcript(input_folder, output_file):
    """
    Gathers all JSON files in 'input_folder', sets 'transcript' to an empty string
    in each, and saves them as a single JSON array in 'output_file'.
    """

    combined_data = []

    # Loop through all .json files in the folder
    for filename in glob.glob(os.path.join(input_folder, '*.json')):
        with open(filename, 'r', encoding='utf-8') as f:
            # Load the file
            data = json.load(f)
            
            # Make the transcript empty
            data["transcript"] = ""
            
            # Add this document to our combined list
            combined_data.append(data)

    # Write them all out to a single JSON array
    with open(output_file, 'w', encoding='utf-8') as out:
        json.dump(combined_data, out, indent=2, ensure_ascii=False)

    print(f"Done! Combined {len(combined_data)} documents into {output_file}")


if __name__ == "__main__":
    # Adjust the paths as needed:
    input_json_folder = r"C:\THESIS_SUM\finesure_summaries"
    output_json_file = r"C:\THESIS_SUM\sum_without_transcript.json"

    gather_and_remove_transcript(input_json_folder, output_json_file)
