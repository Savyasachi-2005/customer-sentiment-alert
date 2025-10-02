import pandas as pd
import re

# Read the CSV
path = "data/sample_feedback.csv"

print("Testing CSV reading...")
print("=" * 50)

# Try reading
try:
    df = pd.read_csv(path, quoting=3)  # QUOTE_NONE
    print(f"Loaded {len(df)} rows")
    print(f"Columns: {df.columns.tolist()}")
    print("\nFirst 3 rows:")
    print(df.head(3))
    
    # Test parsing first row
    if 'feedback' in df.columns:
        first_row = df['feedback'].iloc[0]
        print(f"\nFirst row raw: {first_row}")
        
        # Parse it
        feedback_str = str(first_row).strip().strip('"')
        text_match = re.search(r'""(.*?)""', feedback_str)
        if text_match:
            text = text_match.group(1).strip('"')
            print(f"Extracted text: {text}")
        
        parts = re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', feedback_str)
        print(f"Parts: {parts}")
        if len(parts) > 2:
            print(f"Source: {parts[2].strip().strip('\"')}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
