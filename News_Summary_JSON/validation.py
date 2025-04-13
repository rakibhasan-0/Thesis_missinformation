import json
import glob
import os

def convert_item(old_data, model_name="gpt-4"):
    """
    Convert a single article dict to FineSurE format:
      doc_id, model, transcript, sentences
    """
    doc_id = old_data["id"]  # e.g. article_001
    transcript = old_data["main_text"]  # rename main_text -> transcript

    # If you want multiple sentence lines, do a naive split:
    summary_text = old_data["summary"]
    summary_sentences = []
    for s in summary_text.split('.'):
        s = s.strip()
        if s:
            summary_sentences.append(s + ".")

    # Build FineSurE-style record
    finesure_record = {
        "doc_id": doc_id,
        "model": model_name,      # e.g., "gpt-4" or "my_summarizer"
        "transcript": transcript,
        "sentences": summary_sentences
    }
    return finesure_record

def main(input_folder, output_file, model_name="gpt-4"):
    """
    1) Reads all .json files in 'input_folder'.
    2) Converts each to FineSurE format.
    3) Writes each as a separate line in 'output_file' (JSONL).
    """
    # Gather all JSON files from the folder
    file_paths = sorted(glob.glob(os.path.join(input_folder, "*.json")))

    with open(output_file, "w", encoding="utf-8") as out:
        for fp in file_paths:
            with open(fp, "r", encoding="utf-8") as f:
                # Load the old format: { id, headline, main_text, summary }
                old_data = json.load(f)
            
            # Convert to FineSurE record
            new_record = convert_item(old_data, model_name=model_name)

            # Dump as a line in the .jsonl
            out.write(json.dumps(new_record, ensure_ascii=False) + "\n")

    print(f"Done! Wrote {len(file_paths)} lines to {output_file}.")

if __name__ == "__main__":
    # Example usage:
    # python convert_to_finesure.py
    # This code below just calls 'main' with some defaults. 
    # In a real scenario, you might parse sys.argv or environment variables.
    input_folder = r"C:\THESIS_SUM\News_Summary_JSON"           # folder containing your 150 JSON files
    output_file = "finesure_input.jsonl"      # single .jsonl output
    model_name = "gpt-4"                      # label the system that produced the summary

    main(input_folder, output_file, model_name)
