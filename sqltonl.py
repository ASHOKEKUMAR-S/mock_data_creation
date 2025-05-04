import pandas as pd
import time
from transformers import T5Tokenizer, T5ForConditionalGeneration

# ----------------------------
# Config
# ----------------------------
MODEL_NAME = "dbernsohn/t5_wikisql_SQL2en"
INPUT_CSV = "sql_queries.csv"
OUTPUT_CSV = "sql_to_nl_output.csv"
NUM_VARIANTS = 10  # Number of NL sentences per SQL
SLEEP_BETWEEN = 0.2  # seconds between generations

# ----------------------------
# Load model and tokenizer
# ----------------------------
print(f"🔄 Loading model {MODEL_NAME}...")
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)

# ----------------------------
# Read SQL queries from CSV
# ----------------------------
print(f"📄 Reading queries from {INPUT_CSV}...")
df = pd.read_csv(INPUT_CSV)

results = []

# ----------------------------
# Generate NL for each SQL query
# ----------------------------
for idx, row in df.iterrows():
    sql_query = row['query']
    seen_nl = set()
    start_time = time.time()

    for _ in range(NUM_VARIANTS * 2):  # Try extra to ensure uniqueness
        input_text = f"translate SQL to English: {sql_query} </s>"
        input_ids = tokenizer.encode(input_text, return_tensors="pt")

        output_ids = model.generate(
            input_ids,
            max_length=64,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7
        )
        decoded = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()
        seen_nl.add(decoded)
        time.sleep(SLEEP_BETWEEN)
        if len(seen_nl) >= NUM_VARIANTS:
            break

    end_time = time.time()
    total_time = round(end_time - start_time, 3)

    for nl in list(seen_nl):
        results.append({
            "sql_query": sql_query,
            "nl_input": nl,
            "generation_time_sec": total_time
        })

# ----------------------------
# Save output to CSV
# ----------------------------
print(f"💾 Saving {len(results)} rows to {OUTPUT_CSV}...")
out_df = pd.DataFrame(results)
out_df.to_csv(OUTPUT_CSV, index=False)

print("✅ Done! Check sql_to_nl_output.csv for results.")
