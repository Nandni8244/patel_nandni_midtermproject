import pandas as pd
import time
import os
from mlxtend.frequent_patterns import apriori, association_rules

dataset_names = ["Amazon.csv", "Nike.csv", "Generic.csv", "BestBuy.csv", "Kmart.csv"]

datasets = [os.path.join("data", name) for name in dataset_names]

print("Available Datasets:")
for i, name in enumerate(dataset_names, start=1):
    print(f"{i}. {name}")

while True:
    try:
        choice = int(input("\nEnter the number of the dataset you want to use (1-5): "))
        if 1 <= choice <= len(datasets):
            dataset_name = datasets[choice - 1]
            break
        else:
            print("Please enter a number between 1 and 5.")
    except ValueError:
        print("Invalid input. Please enter a number.")

if not os.path.exists(dataset_name):
    print(f"File '{dataset_name}' not found in current directory.")
    exit()

df = pd.read_csv(dataset_name)

possible_cols = [c for c in df.columns if any(k in c.lower() for k in ['item', 'transaction'])]
if not possible_cols:
    print("Could not find column with 'Item' or 'Transaction' in your CSV file.")
    print("Columns found:", list(df.columns))
    exit()
col_name = possible_cols[0]

transactions = df[col_name].astype(str).apply(lambda x: [i.strip() for i in x.split(',')]).tolist()
num_transactions = len(transactions)

print(f"\nLoaded dataset: {dataset_name}")
print(f"Total Transactions: {num_transactions}")

def get_float_input(prompt):
    while True:
        try:
            val = float(input(prompt))
            if 0 < val <= 1:
                return val
            else:
                print("Value must be between 0 and 1.")
        except ValueError:
            print("Please enter a numeric value between 0 and 1.")

min_support = get_float_input("\nEnter minimum support (0–1): ")
min_conf = get_float_input("Enter minimum confidence (0–1): ")

all_items = sorted(set(item for t in transactions for item in t))
encoded_vals = []

for t in transactions:
    encoded_vals.append({item: (item in t) for item in all_items})

df_encoded = pd.DataFrame(encoded_vals)

print("\nRunning Apriori Algorithm...")
start_time = time.time()

frequent_itemsets = apriori(df_encoded, min_support=min_support, use_colnames=True)
end_time = time.time()
execution_time = end_time - start_time

print(f"Apriori completed in {execution_time:.6f} seconds.")

rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_conf)

print("\n=== Frequent Itemsets ===")
for _, row in frequent_itemsets.iterrows():
    items = ', '.join(list(row['itemsets']))
    print(f"{{{items}}} (support={row['support']:.2f})")

print("\n=== Association Rules ===")
if not rules.empty:
    for _, row in rules.iterrows():
        antecedent = ', '.join(list(row['antecedents']))
        consequent = ', '.join(list(row['consequents']))
        print(f"{antecedent} → {consequent} (confidence={row['confidence']:.2f})")
else:
    print("No rules found for given support/confidence.")

print("\n=== Summary ===")
print(f"Dataset used: {dataset_name}")
print(f"Total transactions: {num_transactions}")
print(f"Frequent itemsets found: {len(frequent_itemsets)}")
print(f"Association rules found: {len(rules)}")
print(f"Execution time: {execution_time:.6f} s")
    