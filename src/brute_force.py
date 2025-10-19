import pandas as pd
import itertools
import time
import os

datasets = [
    os.path.join("data", "Amazon.csv"),
    os.path.join("data", "Nike.csv"),
    os.path.join("data", "Generic.csv"),
    os.path.join("data", "BestBuy.csv"),
    os.path.join("data", "Kmart.csv")
]

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
    print("Could not find a column containing 'Item' or 'Transaction' in your CSV file.")
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

start_time = time.time()

items = sorted(set(itertools.chain.from_iterable(transactions)))
frequent_itemsets = []

k = 1
current_itemsets = [[item] for item in items]

while current_itemsets:
    print(f"\n🔹 Checking {k}-itemsets ...")
    next_itemsets = []
    for itemset in current_itemsets:
        count = sum(1 for t in transactions if set(itemset).issubset(set(t)))
        support = count / num_transactions
        if support >= min_support:
            frequent_itemsets.append((itemset, support))
            next_itemsets.extend([
                sorted(list(set(itemset) | {new_item}))
                for new_item in items if new_item not in itemset
            ])
            print(f"{set(itemset)} (support={support:.2f})")

    current_itemsets = [list(x) for x in set(tuple(x) for x in next_itemsets)]
    k += 1

end_time = time.time()
print(f"\nBrute-force frequent itemset mining completed in {end_time - start_time:.2f} seconds.")

print("\n=== Association Rules ===")
rules = []
for itemset, support in frequent_itemsets:
    if len(itemset) < 2:
        continue
    for i in range(1, len(itemset)):
        for antecedent in itertools.combinations(itemset, i):
            consequent = tuple(sorted(set(itemset) - set(antecedent)))
            antecedent_count = sum(1 for t in transactions if set(antecedent).issubset(set(t)))
            if antecedent_count == 0:
                continue
            confidence = support / (antecedent_count / num_transactions)
            if confidence >= min_conf:
                print(f"{set(antecedent)} → {set(consequent)} (confidence={confidence:.2f})")
                rules.append((antecedent, consequent, confidence))

print("\n=== Summary ===")
print(f"Dataset used: {dataset_name}")
print(f"Total transactions: {num_transactions}")
print(f"Frequent itemsets found: {len(frequent_itemsets)}")
print(f"Association rules found: {len(rules)}")
print(f"Execution time: {end_time - start_time:.6f} s")
