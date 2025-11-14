from flask import Flask, request, jsonify
from flask_cors import CORS
from symspellpy import SymSpell
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import os
import urllib.request

app = Flask(__name__)
CORS(app)

print("🔄 Loading Grammar Correction Model (BART-GEC)...")

# ---------------------------------------------------
# Load the best open-source grammar correction model
# ---------------------------------------------------

MODEL_NAME = "prithivida/grammar_error_correcter_v1"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

nlp = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer
)

print("✅ BART-GEC Model Loaded Successfully!")

# ---------------------------------------------------
# Initialize SymSpell (Spell Correction)
# ---------------------------------------------------

print("🔄 Loading SymSpell Dictionary...")

sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = os.path.join(os.path.dirname(__file__), "frequency_dictionary_en_82_765.txt")

if not os.path.exists(dictionary_path):
    print("📥 Downloading SymSpell dictionary...")
    url = "https://raw.githubusercontent.com/mammothb/symspellpy/master/symspellpy/frequency_dictionary_en_82_765.txt"
    urllib.request.urlretrieve(url, dictionary_path)

sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

print("✅ SymSpell Dictionary Loaded!")

# ---------------------------------------------------
# TEST RUN
# ---------------------------------------------------
test_sentence = "she go school every day"
test_output = nlp(test_sentence, max_new_tokens=60)
print("🔍 Model Test Output:", test_output)


@app.route("/")
def home():
    return jsonify({"message": "Grammar + Spell Correction API is running"})


@app.route("/spellcheck", methods=["POST"])
def spellcheck():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "No text provided"}), 400

        print(f"📩 Received text: {text}")

        # -----------------------------
        # Step 1: Grammar Correction
        # -----------------------------
        result = nlp(
            text,
            max_new_tokens=80,
            num_beams=4,
            early_stopping=True
        )

        grammar_corrected = result[0]["generated_text"].strip()
        print(f"✍️ Grammar Corrected: {grammar_corrected}")

        # -----------------------------
        # Step 2: Spell Correction
        # -----------------------------
        suggestions = sym_spell.lookup_compound(grammar_corrected, max_edit_distance=2)
        final_text = suggestions[0].term if suggestions else grammar_corrected

        # Capitalize first letter
        if final_text:
            final_text = final_text[0].upper() + final_text[1:]

        print(f"✅ Final Output: {final_text}")

        return jsonify({"correctedText": final_text})

    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(debug=True, host="0.0.0.0", port=port)

