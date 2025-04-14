import json

def check_docids(summaries_path, keyfacts_path):
    """
    Checks whether the doc_id values in the summaries file
    match those in the keyfacts file.
    """
    summaries_doc_ids = set()
    keyfacts_doc_ids = set()

    # Read the summaries JSONL, gather doc_ids
    with open(summaries_path, 'r', encoding='utf-8') as sf:
        for line in sf:
            if line.strip():
                data = json.loads(line)
                doc_id = data['doc_id']
                summaries_doc_ids.add(doc_id)

    # Read the keyfacts JSONL, gather doc_ids
    with open(keyfacts_path, 'r', encoding='utf-8') as kf:
        for line in kf:
            if line.strip():
                data = json.loads(line)
                doc_id = data['doc_id']
                keyfacts_doc_ids.add(doc_id)

    # Compare sets
    only_in_summaries = summaries_doc_ids - keyfacts_doc_ids
    only_in_keyfacts = keyfacts_doc_ids - summaries_doc_ids

    print("\n--- Checking doc_id Consistency ---\n")
    if not only_in_summaries and not only_in_keyfacts:
        print("✔ All doc_ids match between the two files!")
    else:
        if only_in_summaries:
            print("The following doc_ids appear in summaries but NOT in keyfacts:")
            for d in sorted(only_in_summaries):
                print(" ", d)
        if only_in_keyfacts:
            print("\nThe following doc_ids appear in keyfacts but NOT in summaries:")
            for d in sorted(only_in_keyfacts):
                print(" ", d)

    print("\n--- Summary Stats ---")
    print(f"Summaries has {len(summaries_doc_ids)} unique doc_ids.")
    print(f"Keyfacts has {len(keyfacts_doc_ids)} unique doc_ids.")

if __name__ == "__main__":
    # Example usage:
    # python check_docids.py

    # Update these with your actual paths:
    summaries_path = r"C:\THESIS_SUM\finesure_input.jsonl"
    keyfacts_path  = r"C:\THESIS_SUM\keyfacts_from_main\all_keyfacts.jsonl"

    check_docids(summaries_path, keyfacts_path)
