"""
Utility Functions Module
Helper functions for data loading and stream simulation.
"""

import pandas as pd
import time
from typing import Generator, Optional


def detect_text_column(df: pd.DataFrame) -> Optional[str]:
    """
    Auto-detect which column likely contains the main text/feedback.
    
    Args:
        df (pd.DataFrame): DataFrame to analyze
        
    Returns:
        str: Name of the detected text column, or None
    """
    # Common text column names
    text_column_names = ['text', 'feedback', 'review', 'comment', 'message', 'content', 'description']
    
    # Check for exact matches first
    for col in df.columns:
        if col.lower() in text_column_names:
            return col
    
    # Find column with longest average string length (likely the text column)
    max_avg_length = 0
    text_col = None
    
    for col in df.columns:
        if df[col].dtype == 'object':  # String columns
            try:
                avg_length = df[col].astype(str).str.len().mean()
                if avg_length > max_avg_length and avg_length > 20:  # Must be reasonably long
                    max_avg_length = avg_length
                    text_col = col
            except:
                continue
    
    return text_col


def create_text_from_ratings(row: pd.Series) -> str:
    """
    Create synthetic text description from rating columns.
    Used when CSV has ratings but no actual text reviews.
    
    Args:
        row (pd.Series): Row with rating information
        
    Returns:
        str: Generated text description
    """
    parts = []
    
    # Check for overall rating
    if 'Review_Overall_Rating' in row.index and pd.notna(row['Review_Overall_Rating']):
        rating = int(row['Review_Overall_Rating'])
        if rating >= 4:
            parts.append("Great experience")
        elif rating == 3:
            parts.append("Average experience")
        else:
            parts.append("Poor experience")
    
    # Add review type
    if 'Review_Type' in row.index and pd.notna(row['Review_Type']) and row['Review_Type'] != 'NA':
        parts.append(f"visited {row['Review_Type']}")
    
    # Check specific ratings
    rating_descriptions = []
    rating_cols = {
        'Rating_Location': 'location',
        'Rating_Sleep_Quality': 'sleep quality',
        'Rating_Rooms': 'rooms',
        'Rating_Cleanliness': 'cleanliness',
        'Rating_Service': 'service'
    }
    
    for col, desc in rating_cols.items():
        if col in row.index and pd.notna(row[col]) and row[col] != 'NA':
            try:
                rating_val = float(row[col])
                if rating_val >= 4:
                    rating_descriptions.append(f"excellent {desc}")
                elif rating_val <= 2:
                    rating_descriptions.append(f"poor {desc}")
            except:
                continue
    
    if rating_descriptions:
        parts.append(", ".join(rating_descriptions))
    
    return ". ".join(parts) + "." if parts else "Customer review with ratings only"


def parse_feedback_string(feedback_str: str) -> dict:
    """
    Parse a feedback string that contains comma-separated values.
    
    Args:
        feedback_str (str): String like "text", Sentiment, Source, timestamp, user, location, score
        
    Returns:
        dict: Parsed components
    """
    import re
    
    # Clean up the string - remove leading/trailing quotes
    feedback_str = str(feedback_str).strip().strip('"')
    
    # Extract text (between triple quotes or double quotes)
    text_match = re.search(r'""(.*?)""', feedback_str)
    if not text_match:
        text_match = re.search(r'"(.*?)"', feedback_str)
    
    text = text_match.group(1).strip('"') if text_match else feedback_str[:50]
    
    # Split the rest by commas (outside quotes)
    parts = re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', feedback_str)
    
    # Try to extract source (usually third element)
    source = "Unknown"
    timestamp = ""
    
    if len(parts) > 2:
        source = parts[2].strip().strip('"')
    
    # Try to extract timestamp (usually fourth element)
    if len(parts) > 3:
        timestamp = parts[3].strip().strip('"')
    
    return {
        'text': text if text else "No text",
        'source': source if source else "Unknown",
        'timestamp': timestamp if timestamp else "2025-10-01"
    }


def transform_to_standard_format(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform any CSV format to the standard format with required columns.
    
    Args:
        df (pd.DataFrame): Original DataFrame
        
    Returns:
        pd.DataFrame: Transformed DataFrame with columns: id, text, source, timestamp
    """
    result_df = pd.DataFrame()
    
    # Handle 'id' column
    if 'id' in df.columns:
        result_df['id'] = df['id']
    else:
        result_df['id'] = range(1, len(df) + 1)
    
    # Check if we have a single "feedback" column with all data concatenated
    if 'feedback' in df.columns and len(df.columns) == 1:
        print("⚠️ Detected single 'feedback' column format. Parsing...")
        parsed_data = df['feedback'].apply(parse_feedback_string)
        result_df['text'] = parsed_data.apply(lambda x: x['text'])
        result_df['source'] = parsed_data.apply(lambda x: x['source'])
        result_df['timestamp'] = parsed_data.apply(lambda x: x['timestamp'])
        result_df['id'] = range(1, len(result_df) + 1)
    else:
        # Handle 'text' column - auto-detect
        text_col = detect_text_column(df)
        if text_col:
            result_df['text'] = df[text_col].astype(str)
        else:
            # Check if this is a ratings-only dataset (like hotel reviews)
            rating_cols = ['Review_Overall_Rating', 'Rating_Value', 'rating', 'score']
            has_ratings = any(col in df.columns for col in rating_cols)
            
            if has_ratings:
                # Generate text from ratings
                print("⚠️ No text column found. Generating descriptions from ratings...")
                result_df['text'] = df.apply(create_text_from_ratings, axis=1)
            else:
                # Concatenate all string columns
                string_cols = df.select_dtypes(include=['object']).columns.tolist()
                if string_cols:
                    result_df['text'] = df[string_cols].astype(str).agg(' | '.join, axis=1)
                else:
                    raise ValueError("No text data found in CSV file")
        
        # Handle 'source' column
        if 'source' in df.columns:
            result_df['source'] = df['source']
        elif 'Hotel_Name_City' in df.columns:  # For hotel review dataset
            result_df['source'] = df['Hotel_Name_City']
        else:
            result_df['source'] = 'CSV Data'
        
        # Handle 'timestamp' column
        if 'timestamp' in df.columns:
            result_df['timestamp'] = df['timestamp']
        elif 'date' in df.columns or 'date_of_review' in df.columns:
            date_col = 'date' if 'date' in df.columns else 'date_of_review'
            result_df['timestamp'] = df[date_col]
        else:
            # Generate timestamps
            result_df['timestamp'] = pd.date_range(start='2025-10-01', periods=len(df), freq='H').astype(str)
    
    # Remove any rows with empty text
    result_df = result_df[result_df['text'].str.strip() != '']
    
    return result_df


def load_data(path: str = "data/sample_feedback.csv") -> pd.DataFrame:
    """
    Load customer feedback data from CSV file.
    Automatically transforms any CSV format to the required standard format.
    
    Args:
        path (str): Path to the CSV file. Defaults to "data/sample_feedback.csv"
        
    Returns:
        pd.DataFrame: DataFrame containing the feedback data with columns:
                     id, text, source, timestamp
    """
    try:
        # Try different CSV reading approaches
        df = None
        
        # First try: standard CSV reading
        try:
            df = pd.read_csv(path)
        except:
            # Second try: with different quoting
            df = pd.read_csv(path, quoting=3)  # QUOTE_NONE
        
        if df is None or df.empty:
            raise ValueError("Failed to read CSV or CSV is empty")
            
        print(f"📁 Loaded {len(df)} rows from {path}")
        print(f"📋 Detected columns: {', '.join(df.columns.tolist())}")
        
        # Transform to standard format
        df = transform_to_standard_format(df)
        
        if df.empty:
            raise ValueError("No valid data after transformation")
            
        print(f"✅ Processed {len(df)} feedback entries")
        
        return df
    except FileNotFoundError:
        print(f"❌ Error: File not found at {path}")
        raise
    except pd.errors.EmptyDataError:
        print(f"❌ Error: File at {path} is empty")
        raise
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        import traceback
        traceback.print_exc()
        raise


def simulate_stream(df: pd.DataFrame, delay: int = 2) -> Generator[dict, None, None]:
    """
    Simulate a live stream of feedback by yielding rows one at a time.
    This mimics real-time data ingestion for demo purposes.
    
    Args:
        df (pd.DataFrame): DataFrame containing feedback data
        delay (int): Delay in seconds between each row. Defaults to 2 seconds
        
    Yields:
        dict: Each row as a dictionary with feedback information
    """
    print(f"🔄 Starting simulated stream with {delay}s delay between items...")
    
    for idx, row in df.iterrows():
        # Convert row to dictionary
        feedback = row.to_dict()
        
        # Simulate delay (like real-time data arrival)
        if idx > 0:  # Don't delay before first item
            time.sleep(delay)
        
        yield feedback


def validate_feedback_data(df: pd.DataFrame) -> bool:
    """
    Validate that the feedback DataFrame has required columns and data.
    
    Args:
        df (pd.DataFrame): DataFrame to validate
        
    Returns:
        bool: True if valid, raises ValueError otherwise
    """
    required_columns = ['id', 'text', 'source', 'timestamp']
    
    # Check if all required columns exist
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"⚠️ Warning: Missing columns: {missing_columns}")
        return False
    
    # Check if DataFrame is empty
    if df.empty:
        raise ValueError("DataFrame is empty")
    
    # Check for null values in critical columns
    if df['text'].isnull().any():
        print(f"⚠️ Warning: Found {df['text'].isnull().sum()} null values in 'text' column")
    
    print("✅ Data validation passed")
    return True


def get_data_summary(df: pd.DataFrame) -> dict:
    """
    Get a summary of the feedback data.
    
    Args:
        df (pd.DataFrame): DataFrame containing feedback data
        
    Returns:
        dict: Summary statistics including total count, sources, date range
    """
    summary = {
        "total_feedback": len(df),
        "unique_sources": df['source'].nunique() if 'source' in df.columns else 0,
    }
    
    # Only show top sources if there are many
    if 'source' in df.columns:
        if df['source'].nunique() <= 10:
            summary["sources"] = df['source'].unique().tolist()
            summary["source_counts"] = df['source'].value_counts().to_dict()
        else:
            summary["top_sources"] = df['source'].value_counts().head(10).to_dict()
    
    # Try to parse timestamps if possible
    if 'timestamp' in df.columns:
        try:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            summary["date_range"] = {
                "start": df['timestamp'].min().strftime("%Y-%m-%d %H:%M:%S"),
                "end": df['timestamp'].max().strftime("%Y-%m-%d %H:%M:%S")
            }
        except:
            summary["date_range"] = "Unable to parse timestamps"
    
    return summary


# Example usage for testing
if __name__ == "__main__":
    # Test data loading
    df = load_data()
    print("\nDataFrame Info:")
    print(df.head())
    
    # Test validation
    print("\nValidating data...")
    validate_feedback_data(df)
    
    # Test summary
    print("\nData Summary:")
    summary = get_data_summary(df)
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # Test stream simulation (limited to 2 items for testing)
    print("\nTesting stream simulation (first 2 items):")
    for i, feedback in enumerate(simulate_stream(df.head(2), delay=1)):
        print(f"  Item {i+1}: {feedback['text'][:50]}...")
