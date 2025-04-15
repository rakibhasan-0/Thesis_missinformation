import json
import os

input_jsonl_path = r"C:\THESIS_SUM\keyfacts_from_main"
output_json_path = r"C:\THESIS_SUM\all_keyfacts.json"

# This list will hold all objects from all lines of all JSONL files
combined_data = []

for filename in os.listdir(input_jsonl_path):
    # Process only files ending with ".jsonl"
    if filename.endswith(".jsonl"):
        full_path = os.path.join(input_jsonl_path, filename)

        with open(full_path, 'r', encoding='utf-8') as f:
            # Each line in a JSONL file is a separate JSON object
            for line in f:
                # strip() in case of trailing whitespace/newlines
                line = line.strip()
                if not line:
                    continue  # skip empty lines
                data = json.loads(line)
                combined_data.append(data)

# Now write out all collected data to a single JSON array
with open(output_json_path, 'w', encoding='utf-8') as out:
    json.dump(combined_data, out, ensure_ascii=False, indent=2)

print(f"Done! Combined {len(combined_data)} records into {output_json_path}")
