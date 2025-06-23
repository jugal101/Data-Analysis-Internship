import pandas as pd

# Load data (update path to your downloaded file)
df = pd.read_csv(r'D:\Task1\Data\KaggleV2-May-2016.csv')

# 1. Initial inspection
print("=== INITIAL INSPECTION ===")
print(f"Shape: {df.shape}")
print("\nMissing values:")
print(df.isnull().sum())
print("\nDuplicates:", df.duplicated().sum())
print("\nData types:")
print(df.dtypes)
print("\nUnique values in categorical columns:")
print(f"Gender: {df['Gender'].unique()}")
print(f"No-show: {df['No-show'].unique()}")

# 2. Clean column names
df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')

# 3. Fix misspelled column names
df = df.rename(columns={
    'hipertension': 'hypertension',
    'handcap': 'handicap'
})

# 4. Handle missing values
# No missing values in this dataset, but adding for generality
for col in ['age', 'gender', 'appointmentday']:
    if df[col].isnull().sum() > 0:
        if df[col].dtype == 'object':
            df[col].fillna(df[col].mode()[0], inplace=True)
        else:
            df[col].fillna(df[col].median(), inplace=True)

# 5. Remove duplicates
initial_count = len(df)
df.drop_duplicates(inplace=True)
duplicates_removed = initial_count - len(df)

# 6. Standardize text values
df['gender'] = df['gender'].str.upper().map({
    'M': 'MALE', 
    'F': 'FEMALE',
    'MALE': 'MALE',
    'FEMALE': 'FEMALE'
})

# 7. Fix date formats
df['scheduledday'] = pd.to_datetime(df['scheduledday'])
df['appointmentday'] = pd.to_datetime(df['appointmentday'])

# 8. Fix data types
df['patientid'] = df['patientid'].astype('int64').astype('str')
df['age'] = df['age'].astype(int)

# 9. Handle invalid age values
invalid_ages = df[df['age'] < 0]
df = df[df['age'] >= 0]

# 10. Final checks
print("\n=== AFTER CLEANING ===")
print(f"New shape: {df.shape}")
print("\nRemaining missing values:")
print(df.isnull().sum())
print(f"\nInvalid ages removed: {len(invalid_ages)}")
print(f"Duplicates removed: {duplicates_removed}")

# 11. Save cleaned data
df.to_csv('cleaned_medical_appointments.csv', index=False)

# 12. Generate summary
# 12. Generate and save summary
summary = f"""
DATA CLEANING SUMMARY (Medical Appointment No Shows)
====================================================

1. COLUMN RENAMING:
   - Converted to lowercase with underscores
   - Fixed misspellings: 
        hipertension → hypertension
        handcap → handicap

2. MISSING VALUES:
   - No missing values found

3. DUPLICATES REMOVED: {duplicates_removed} rows

4. STANDARDIZATION:
   - Gender: Mapped to 'MALE'/'FEMALE'

5. DATE FORMATS:
   - Converted to datetime: 
        scheduledday → {df['scheduledday'].dtype}
        appointmentday → {df['appointmentday'].dtype}

6. DATA TYPE CORRECTIONS:
   - PatientID: converted to string
   - Age: converted to integer

7. INVALID DATA:
   - Removed {len(invalid_ages)} rows with negative age values

FINAL DATASET: {df.shape[0]} rows, {df.shape[1]} columns
"""

# Save with UTF-8 encoding
with open('cleaning_summary.txt', 'w', encoding='utf-8') as f:
    f.write(summary)