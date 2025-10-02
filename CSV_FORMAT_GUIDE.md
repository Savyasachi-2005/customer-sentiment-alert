# CSV File Format Guide

## Supported CSV Formats

The Customer Sentiment Alert system now supports **ANY** CSV format! It automatically detects and adapts to your data structure.

## ✅ Recommended Format (sample_feedback_clean.csv)

```csv
text,sentiment,source,timestamp
I love this product!,Positive,Twitter,2023-06-15 09:23:14
The service was terrible.,Negative,Yelp Reviews,2023-06-15 11:45:32
```

**Columns:**
- `text`: The feedback/review/comment text (required)
- `sentiment`: Optional - will be analyzed by AI
- `source`: Where the feedback came from
- `timestamp`: When it was received

## 🔄 Auto-Detection Features

### 1. Text Column Detection
The system automatically finds text by looking for:
- Columns named: `text`, `feedback`, `review`, `comment`, `message`, `content`
- Or the column with the longest average text length

### 2. ID Generation
- If no `id` column exists, IDs are generated automatically (1, 2, 3...)

### 3. Source Detection
- Uses existing `source` column
- Falls back to `Hotel_Name_City`, `category`, or other suitable columns
- Defaults to "CSV Data" if nothing found

### 4. Timestamp Handling
- Uses existing `timestamp`, `date`, or `date_of_review` columns
- Generates timestamps if none exist

## 📊 Special Format Support

### Ratings-Only Data (Hotel Reviews)
If your CSV has ratings but no text:
```csv
Hotel_Name_City,Review_Overall_Rating,Rating_Service,Rating_Cleanliness
Bombay Hotel,1,3,2
```

The system will generate text like:
- `"Poor experience. poor cleanliness."`

### Single Column Format
Even malformed CSVs with everything in one column can be parsed!

## 🎯 Urgency Detection Keywords

The system marks feedback as **HIGH URGENCY** when NEGATIVE sentiment + these keywords:
- `scam`, `refund`, `angry`, `worst`, `crash`
- `terrible`, `horrible`, `awful`, `disaster`, `garbage`
- `poor experience`, `poor service`, `poor cleanliness`
- `defective`, `broken`, `never again`, `waste of money`
- **Or** multiple mentions of "poor" (2+)

## 📁 CSV Files in This Project

1. **sample_feedback_clean.csv** ← RECOMMENDED
   - Clean, standard format
   - 25 feedback items
   - Mix of positive/negative with urgent cases
   - Ready to use!

2. **sample_feedback.csv** (if exists)
   - Your original/custom data
   - May have special formatting

3. **feedback_backup2.csv**
   - Backup of previous data

## 🚀 Quick Start

1. **Use the provided clean CSV:**
   - Just run the app, it will use `sample_feedback_clean.csv` by default

2. **Add your own CSV:**
   - Drop any CSV file into the `data/` folder
   - Select it from the dropdown in the sidebar
   - The system will auto-detect and adapt!

3. **Configure settings:**
   - Max Items: Limit how many rows to process
   - Stream Delay: Control speed of display
   - Slack Webhook: Optional alerts

## 📋 CSV Requirements Summary

**Minimum:** ONE column with text data

**The system handles:**
- ✅ Any column names
- ✅ Missing IDs, sources, or timestamps
- ✅ Ratings-only data
- ✅ Large datasets (use Max Items to limit)
- ✅ Different quote styles and formats

## 💡 Tips

1. **For best results:** Use standard column names (`text`, `source`, `timestamp`)
2. **For large CSVs:** Set "Max Items to Process" to 50-100 for demos
3. **For urgency testing:** Include words like "terrible", "scam", "worst" in negative feedback
4. **Speed adjustment:** Lower stream delay (0.5s) for faster demos

Enjoy! 🎉
