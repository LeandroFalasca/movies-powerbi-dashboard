import pandas as pd
import re
import os

# Configuration
input_path = r'c:\Users\falasca\Downloads\movies.csv'
output_dir = r'C:\Users\falasca\.gemini\antigravity\scratch\movies_powerbi'
os.makedirs(output_dir, exist_ok=True)

print(f"Reading file from: {input_path}")

try:
    df = pd.read_csv(input_path)
except UnicodeDecodeError:
    print("UTF-8 decode failed, trying cp1252...")
    df = pd.read_csv(input_path, encoding='cp1252')

print(f"Loaded {len(df)} rows.")

# 1. Extract Year
def extract_year(title):
    # Matches (1995) at the end of the string (or anywhere, but usually end)
    match = re.search(r'\((\d{4})\)', str(title))
    if match:
        return int(match.group(1))
    return None

df['Year'] = df['Title'].apply(extract_year)

# 2. Clean Title
def clean_title(title):
    t = str(title)
    # Remove (1995)
    t = re.sub(r'\s*\(\d{4}\)', '', t)
    # Remove (not_def) if it exists
    t = re.sub(r'\s*\(not_def\)', '', t)
    return t.strip()

df['Title_Clean'] = df['Title'].apply(clean_title)

# 3. Process Genres
def split_genres(x):
    if pd.isna(x) or str(x).lower() == 'nan':
        return []
    s = str(x)
    # Fix separators (Comedy--Horror -> Comedy|Horror)
    s = s.replace('--', '|')
    # Fix typos
    s = s.replace('Dramma', 'Drama')
    s = s.replace('Dramatic', 'Drama') # Proactive fix for Schindler's List
    return s.split('|')

df['Genres_List'] = df['Genres'].apply(split_genres)
df['Genre_Count'] = df['Genres_List'].apply(len)

# Select and Reorder columns for the 'Unique' table
# We keep the original 'Title' and 'Genres' as requested, plus the new clean ones
cols_unique = ['MovieID', 'Title', 'Title_Clean', 'Year', 'Genre_Count', 'Genres', 'Language', 'Country', 'Total Views']
# Ensure columns exist (handling potential missing cols strictly)
cols_unique = [c for c in cols_unique if c in df.columns]

df_unique = df[cols_unique].copy()

# 4. Explode for Power BI (One row per genre)
# We explode the list column
df_exploded = df.explode('Genres_List')
df_exploded.rename(columns={'Genres_List': 'Genre_Individual'}, inplace=True)

# Select columns for exploded view
cols_exploded = ['MovieID', 'Title_Clean', 'Year', 'Genre_Individual', 'Genre_Count', 'Total Views']
# Keep relevant columns
df_exploded = df_exploded[cols_exploded]

# 5. Wide Format (Genre_1, Genre_2...) to avoid row duplication
# This expands the list into separate columns
df_wide_genres = df['Genres_List'].apply(pd.Series)
# Rename columns to Genre_1, Genre_2, etc.
df_wide_genres.columns = [f'Genre_{i+1}' for i in df_wide_genres.columns]
# Join back to the unique dataframe (excluding original Genres and list)
df_wide = df_unique.join(df_wide_genres)

# Save files
unique_path = os.path.join(output_dir, 'movies_processed_unique.csv')
exploded_path = os.path.join(output_dir, 'movies_processed_exploded.csv')
wide_path = os.path.join(output_dir, 'movies_processed_wide.csv')

df_unique.to_csv(unique_path, index=False)
df_exploded.to_csv(exploded_path, index=False)
df_wide.to_csv(wide_path, index=False)

print(f"Processing Complete.")
print(f"Unique Movies saved to: {unique_path}")
print(f"Exploded Data saved to: {exploded_path} (Rows: {len(df_exploded)})")
print(f"Wide Format saved to: {wide_path} (Rows: {len(df_wide)})")
