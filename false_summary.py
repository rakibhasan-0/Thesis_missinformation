import os
import glob
import json
import openai
import sys

_api_key = "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"
_client = openai.OpenAI(api_key=_api_key)
_model = "gpt-4.1"


def build_falsify_prompt(doc_id, key_facts):
    """
    Constructs the EXACT prompt as specified, 
    filling placeholders for doc_id and bullet-format key_facts.
    """
    keyfacts_str = "\n".join(f"- {fact}" for fact in key_facts) # Convert list to bullet points

    prompt_text = f"""
    You will get a set of key facts from an article and an article ID (doc_id). Your task will be to falsify the key facts in four categories. These four categories will be applied: fabrication, false attribution, inaccurate quantities, and misrepresentation. 

    Falsification Categories:

    For fabrication, you will add fictional data, sources, or events to the given key facts which have no basis in reality. 

    For false attribution, you will preserve the overall narrative but incorrectly attribute an event, statement, action, etc., to a different entity than the original key fact. For Example: Let's say entity X performed an
    action or made a statement. Change it to Y so that the action or statement
    remains unchanged. Also, Y should appear in the original article.

    For inaccurate numerical quantities, subtle or noticeable changes should be introduced to any numeric values in the key facts. This includes tweaking some numerical details such as ("25" to "30") or making a significant difference such as (2 million to 20 million). For example, "25 people died of cholera in New Delhi" can be rewritten as "Dozens died of cholera in New Delhi" to exaggerate the situation intentionally.

    For misrepresentation, you introduce bias in the key facts, technically retaining the original story. This means the keyfact could be written to intentionally show some person or entity in a good or bad light or to downplay or exaggerate certain events.


    Instruction: 

    First step: Read the keyfact one by one and check which error category suitable for the keyfact. Repeat that process until all keyfacts are applied to any of these category which mentioned above.

    Second Step: Then produce a 5-6 sentence summary **only** using those falsified key facts and store it in following JSON format.

    Important guidelines:
    - Do **not** include the original key facts.
    - Do **not** show the categories or the falsified versions item by item.
    - Output **only** the final falsified summary in JSON.
    - No additional text, headings, or markdown formatting.
    - return exactly in this format:
    
    {{
        "doc_id": "{doc_id}",
        "sentences": [
            "Sentence 1",
            "Sentence 2",
            "Sentence 3",
            "Sentence 4",
            "Sentence 5"
        ]
    }}


    Article Id: {doc_id}
    Keyfacts: {keyfacts_str}
"""
    return prompt_text

def run_falsification(doc_id, key_facts, model="gpt-3.5-turbo"):
    """
    Builds the prompt and sends it to the LLM. Returns the LLM's raw text output.
    """
    prompt = build_falsify_prompt(doc_id, key_facts)
    
    response = _client.chat.completions.create(
        model = _model,
        messages = [
            {"role": "user", "content": prompt}
        ],
    )
    
    
    # The LLM's entire textual response
    llm_output = response.choices[0].message.content.strip()
    return llm_output

def parse_llm_output_as_json(llm_output):
    """
    Attempt to parse the LLM output as JSON and verify 
    it has the keys "doc_id" and "sentences".
    
    Returns (True, parsed_dict) if valid, otherwise (False, None).
    """
    try:
        data = json.loads(llm_output)
        if "doc_id" in data and "sentences" in data:
            return (True, data)
        else:
            return (False, None)
    except json.JSONDecodeError:
        return (False, None)


def main():
    if len(sys.argv) < 3:
        print("Usage: python false_summary.py <input_dir> <output_dir>")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    json_files = glob.glob(os.path.join(input_dir, "*.json"))
    if not json_files:
        print(f"No JSON files found in {input_dir}")
        return

    for in_file in json_files:
        with open(in_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            doc_id = data["doc_id"]
            key_facts = data["key_facts"]

        llm_output = run_falsification(doc_id, key_facts)
        success, parsed = parse_llm_output_as_json(llm_output)

        # Prepare the final dictionary for output
        if success:
            # Use the parsed JSON from the model
            # The doc_id from the file and from the model should match,
            # but we can keep whichever we like:
            result_dict = {
                "doc_id": parsed["doc_id"],  # or doc_id from the input
                "sentences": parsed["sentences"]
            }
        else:
            # If not valid JSON, we can fallback to storing as a single array or similar
            result_dict = {
                "doc_id": doc_id,
                "sentences": [llm_output]  # fallback: store raw text in a one-item array
            }

        out_file = os.path.join(
            output_dir,
            os.path.basename(in_file).replace(".json", "_falsified.json")
        )
        with open(out_file, "w", encoding="utf-8") as outf:
            json.dump(result_dict, outf, indent=2, ensure_ascii=False)

        print(f"Processed {in_file}, output -> {out_file}")

if __name__ == "__main__":
    main()