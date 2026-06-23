import os
import re
import sys
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Please download the spaCy language model: python -m spacy download en_core_web_sm")
    sys.exit(1)

def extract_short_name(step_text):
    """Isolates verbs and nouns to create clean, condensed function names."""
    doc = nlp(step_text)
    words = []
    for token in doc:
        if token.pos_ in ["VERB", "NOUN", "PROPN"] and not token.is_stop:
            if token.lemma_.lower() not in ["step", "test", "verify", "check"]:
                words.append(token.lemma_.lower())
    if not words:
        clean_text = re.sub(r'[^a-zA-Z0-9\s_]', '', step_text)
        return re.sub(r'\s+', '_', clean_text).strip('_').lower()
    return "step_" + "_".join(words[:4])

def generate_behave_template(feature_file_path):
    if not os.path.exists(feature_file_path):
        print(f"Error: File '{feature_file_path}' not found.")
        return

    last_main_keyword = "step" 
    seen_steps = set()
    generated_blocks = []
    used_func_names = {}

    step_pattern = re.compile(r'^\s*(Given|When|Then|And|But)\s+(.+)$', re.IGNORECASE)

    with open(feature_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = step_pattern.match(line)
            if match:
                keyword, step_text = match.groups()
                keyword_lower = keyword.lower()
                decorator = keyword_lower if keyword_lower not in ['and', 'but'] else last_main_keyword
                last_main_keyword = decorator

                step_text_clean = step_text.strip()
                if (decorator, step_text_clean) in seen_steps:
                    continue
                seen_steps.add((decorator, step_text_clean))

                func_name = extract_short_name(step_text_clean)
                if func_name in used_func_names:
                    used_func_names[func_name] += 1
                    func_name = f"{func_name}_{used_func_names[func_name]}"
                else:
                    used_func_names[func_name] = 1
                
                block = f"@{decorator}('{step_text_clean}')\ndef {func_name}(context):\n    # TODO: Implement step logic\n    pass\n"
                generated_blocks.append(block)

    output_content = "from behave import given, when, then, step\n\n\n" + "\n".join(generated_blocks)
    base_path, _ = os.path.splitext(feature_file_path)
    output_file_path = f"{base_path}_steps_template.py"

    with open(output_file_path, 'w', encoding='utf-8') as out_file:
        out_file.write(output_content)
    print(f"Success! Condensed template generated at: {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_steps.py <path_to_feature_file>")
    else:
        generate_behave_template(sys.argv[1])
