import json
import glob
import os
import csv
import re

def extract_numeric_id(doc_id_str):
    """
    Extract trailing digits from a doc ID string (e.g., 'article_001' -> 1).
    If no digits are found, return 9999999 so the file sorts last.
    """
    match = re.search(r'(\d+)$', doc_id_str)
    if match:
        return int(match.group(1))
    return 9999999

def calculate_faithfulness_score(json_file_path):
    """
    Reads a JSON file containing sentence fact-check results.
    Returns a tuple (doc_id, faithfulness_percent), where:
      - doc_id is derived from the file name.
      - faithfulness_percent is the percentage of sentences
        marked "no error."
    """
    file_name = os.path.basename(json_file_path)
    doc_id = os.path.splitext(file_name)[0]

    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    total_sentences = len(data)
    no_error_count = sum(
        1 for item in data if item.get("category", "").lower() == "no error"
    )

    # Avoid divide-by-zero if file is empty
    if total_sentences == 0:
        faithfulness_percent = 0.0
    else:
        faithfulness_percent = (no_error_count / total_sentences) * 100

    return doc_id, faithfulness_percent

def main():
    input_folder = r"C:\THESIS_SUM\fineSure_faith_res"
    output_csv = r"C:\THESIS_SUM\final_faithfulness.csv"

    json_files = glob.glob(os.path.join(input_folder, "*.json"))
    if not json_files:
        print(f"No JSON files found in: {input_folder}")
        return

    results = []
    for json_path in json_files:
        doc_id, faithfulness_score = calculate_faithfulness_score(json_path)
        results.append((doc_id, faithfulness_score))

    # Sort the results by numeric ID extracted from the doc_id
    results.sort(key=lambda x: extract_numeric_id(x[0]))

    # Compute the overall average faithfulness
    if results:
        overall_faithfulness = sum(score for _, score in results) / len(results)
    else:
        overall_faithfulness = 0.0

    # Write all results to CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["doc_id", "faithfulness_percent"])

        for doc_id, score in results:
            writer.writerow([doc_id, f"{score:.2f}"])

        writer.writerow(["OVERALL", f"{overall_faithfulness:.2f}"])

    print(f"Wrote faithfulness data for {len(results)} articles to {output_csv}")
    print(f"Overall Faithfulness: {overall_faithfulness:.2f}%")

if __name__ == "__main__":
    main()
