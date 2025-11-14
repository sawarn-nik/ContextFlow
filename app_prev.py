from flask import Flask, request, jsonify
from flask_cors import CORS
from symspellpy import SymSpell
from transformers import T5Tokenizer, T5ForConditionalGeneration, pipeline
import os

app = Flask(__name__)
CORS(app)

print("🔄 Loading AI model... this may take a minute.")

# Load your fine-tuned T5 model
tokenizer = T5Tokenizer.from_pretrained("./grammar-model/checkpoint-72", use_fast=False)
model = T5ForConditionalGeneration.from_pretrained("./grammar-model/checkpoint-72")

nlp = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer
)

print("✅ Transformer model loaded successfully!")

# -------------------------------
# Initialize SymSpell
# -------------------------------

sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = os.path.join(os.path.dirname(__file__), "frequency_dictionary_en_82_765.txt")

if not os.path.exists(dictionary_path):
    import urllib.request
    print("📥 Downloading SymSpell dictionary...")
    url = "https://raw.githubusercontent.com/mammothb/symspellpy/master/symspellpy/frequency_dictionary_en_82_765.txt"
    urllib.request.urlretrieve(url, dictionary_path)

sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

print("✅ SymSpell dictionary loaded.")
test = nlp("fix: she sing well")
print("heyyy",test)

@app.route('/')
def home():
    return jsonify({"message": "Hybrid AI Spell & Grammar Correction API is running!"})


# @app.route('/spellcheck', methods=['POST'])
# def spellcheck():
#     try:
#         data = request.get_json()
#         text = data.get("text", "").strip()

#         if not text:
#             return jsonify({"error": "No text provided"}), 400

#         print(f"Received text: {text}")

#         # -------------------------------
#         # 1️⃣ Step 1 — Spelling correction
#         # -------------------------------
#         suggestions = sym_spell.lookup_compound(text, max_edit_distance=2)
#         basic_correction = suggestions[0].term if suggestions else text
#         print(f"After SymSpell: {basic_correction}")

#         # -------------------------------
#         # 2️⃣ Step 2 — Grammar correction
#         # -------------------------------
#         model_input = "fix: " + basic_correction   # IMPORTANT PREFIX

#         result = nlp(
#             model_input,
#             max_new_tokens=64,
#             num_beams=5,
#             early_stopping=True,
#             repetition_penalty=2.5,
#             clean_up_tokenization_spaces=True
#         )

#         corrected_text = result[0]["generated_text"].strip()

#         # Capitalize first letter
#         if corrected_text:
#             corrected_text = corrected_text[0].upper() + corrected_text[1:]

#         print(f"Final corrected text: {corrected_text}")

#         return jsonify({"correctedText": corrected_text})

#     except Exception as e:
#         print("❌ Error:", str(e))
#         return jsonify({"error": str(e)}), 500


@app.route('/spellcheck', methods=['POST'])
def spellcheck():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "No text provided"}), 400

        print(f"Received text: {text}")

        # Step 1 — Grammar correction (T5)
        model_input = "fix: " + text
        result = nlp(
            model_input,
            max_new_tokens=128,
            num_beams=1,
            do_sample=True,
            top_k=50,
            top_p=0.95
        )


        print(f"Grammar corrected text: {result[0]['generated_text'].strip()}")
        corrected_text = result[0]["generated_text"].strip()

        # Step 2 — Optional spell correction AFTER grammar fixing
        suggestions = sym_spell.lookup_compound(corrected_text, max_edit_distance=2)
        corrected_text = suggestions[0].term if suggestions else corrected_text

        # Capitalize first letter
        if corrected_text:
            corrected_text = corrected_text[0].upper() + corrected_text[1:]

        print(f"Final corrected text: {corrected_text}")

        return jsonify({"correctedText": corrected_text})

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(debug=True, host="0.0.0.0", port=port)
