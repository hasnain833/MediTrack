import csv
import os
import sys
from datetime import date

# Add root directory to path to import database modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.models import Medicine

def clean_dataset():
    csv_path = os.path.join('data', 'Pakistan Medicines Dataset.csv')
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        return

    print(f"Reading dataset from {csv_path}...")
    
    success_count = 0
    fail_count = 0
    
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Clean and map fields
                # CSV Columns: Drug Name, Manufacturer, Strength, Form, Indication, Side Effects, Available In, Age Restriction, Prescription Required, Price
                
                name = row.get('Drug Name', '').strip()
                if not name:
                    continue
                    
                # Clean Price (remove non-numeric chars, handle NaN)
                price_str = row.get('Price', '0').strip()
                try:
                    price = float(price_str) if price_str.lower() != 'nan' else 0.0
                except ValueError:
                    price = 0.0

                # Map to database dictionary
                data = {
                    'medicine_name': name,
                    'category': 'General', # Dataset doesn't have a direct category, use default
                    'company': row.get('Manufacturer', 'Generic').strip(),
                    'barcode': None, # Use None (NULL) to avoid duplicate empty string error
                    'strength': row.get('Strength', '').strip(),
                    'form': row.get('Form', '').strip(),
                    'batch_no': 'IMPORT-2026',
                    'expiry_date': date(2027, 12, 31), # placeholder
                    'stock_qty': 100, # default stock
                    'price': price,
                    'reorder_level': 20,
                    'indication': row.get('Indication', '').strip(),
                    'side_effects': row.get('Side Effects', '').strip(),
                    'age_restriction': row.get('Age Restriction', '').strip(),
                    'prescription_required': row.get('Prescription Required', 'No').strip().lower() == 'yes'
                }
                
                Medicine.create(data)
                success_count += 1
                if success_count % 10 == 0:
                    print(f"Imported {success_count} items...")
                    
            except Exception as e:
                print(f"Failed to import row {row.get('Drug Name')}: {e}")
                fail_count += 1

    print(f"\n--- Import Complete ---")
    print(f"Successfully imported: {success_count}")
    print(f"Failed: {fail_count}")

if __name__ == "__main__":
    clean_dataset()
