# patel_nandni_midtermproject

**Name:** Nandni Patel  
**Email:** np888@njit.edu  
**Instructor:** Dr. Yasser Abduallah  
**Course:** CS634 – Data Mining

## Project Overview

This project focuses on Frequent Itemset Mining and Association Rule Learning using three approaches:

- **Brute Force Method** – Implemented from scratch to understand the fundamental logic behind frequent itemset generation and rule formation.  
- **Apriori Algorithm** – Implemented using Python’s `mlxtend` library to demonstrate a candidate-generation-based approach.  
- **FP-Growth Algorithm** – Implemented using Python’s `mlxtend` library to explore a more scalable, memory-efficient alternative to Apriori.

The goal is to compare these methods in terms of performance, scalability, and pattern discovery effectiveness.

## Dataset Description

Five synthetic transactional datasets were created manually. Each represents a different type of store and contains at least 20 transactions. All datasets were exported as CSV files and can be easily imported using Python or data mining tools.

**Datasets created:**
- Amazon – Programming and web development books  
- BestBuy – Electronics and accessories  
- Kmart – Home and bedding products  
- Nike – Sportswear and athletic products  
- Generic – Simple labeled items A–F for controlled examples

## How to Run the Code

### 1. Environment Setup

Use Python 3.10 to 3.12. Avoid Python 3.13 because some libraries (like 'mlxtend') may not fully support it yet.

You can use Anaconda, Miniconda, or create a virtual environment manually:

- python -m venv env
- source env/bin/activate      # macOS/Linux
- env\Scripts\activate         # Windows

### 2. Install Required Libraries

Use the following command to install the required dependencies:

pip install pandas numpy mlxtend jupyter

### 3. Running the Project

### Option 1: Jupyter Notebook
- Open the notebook file.  
- Run each cell sequentially (`Shift + Enter`) to execute and view results for **Brute Force**, **Apriori**, and **FP-Growth**.

### Option 2: Visual Studio Code
- Open the project folder.  
- Run the Python scripts in the `src` directory. For example: python src/brute_force.py
- Follow the prompts to select a dataset, set support and confidence values, and view the results.

## Conclusion

- **Brute Force** is simple but not scalable for large datasets.  
- **Apriori** improves efficiency but involves multiple scans.  
- **FP-Growth** is the most scalable and performs best overall.  
- As support and confidence values increase, the number of frequent itemsets and rules decreases for all methods, which matches expected behavior.

