import pandas as pd
import os

CLEANED_FILE = "cleaned_data.csv"
OUTPUT_FILE = "custom_search.csv"


def display_banner():
    print("\n" + "=" * 50)
    print(" " * 10 + "EMPLOYEE INVESTIGATION TOOL")
    print("=" * 50 + "\n")


def get_user_input():
    test=False
    while not(test):
        keyword = input("Enter a job title keyword to search for: ").strip()
        if keyword:
            test=True
            return keyword
        print("Error: Please enter a valid keyword.\n")


def search_employees(df, keyword):
    try:
        matches = df[df["JobTitle"].str.contains(keyword, case=False, na=False)]
        return matches
    except Exception as e:
        print(f"Error during search: {e}")
        return pd.DataFrame()


def calculate_statistics(df_matches):
    stats = {
        "count": len(df_matches),
        "avg_base_pay": 0,
        "highest_total_pay": 0
    }
    
    if len(df_matches) > 0:
        if "BasePay" in df_matches.columns:
            stats["avg_base_pay"] = df_matches["BasePay"].mean()
        
        if "TotalPay" in df_matches.columns:
            stats["highest_total_pay"] = df_matches["TotalPay"].max()
    return stats


def display_results(keyword, stats):
    print("\n" + "-" * 50)
    print(f"SEARCH RESULTS FOR: '{keyword}'")
    print("-" * 50)
    print(f"Number of matches: {stats['count']}")
    
    if stats['count'] > 0:
        print(f"Average BasePay: ${stats['avg_base_pay']:,.2f}")
        print(f"Highest TotalPay: ${stats['highest_total_pay']:,.2f}")
    else:
        print("No employees found matching your search.")
    print("-" * 50 + "\n")


def save_results(df_matches, keyword):
    try:
        if len(df_matches) > 0:
            df_matches.to_csv(OUTPUT_FILE, index=False)
            print(f"Results saved to '{OUTPUT_FILE}'")
        else:
            print("No results to save.")
    except Exception as e:
        print(f"Error saving results: {e}")


def main():
    try:
        # Display banner
        display_banner()
        
        # Check if cleaned data exists
        if not os.path.exists(CLEANED_FILE):
            print(f"Error: '{CLEANED_FILE}' not found!")
            print("Please run the data cleaning process first.")
            return
        
        # Load the data
        print(f"Loading data from '{CLEANED_FILE}'...")
        df = pd.read_csv(CLEANED_FILE, low_memory=False, encoding="utf-8")
        print(f"✓ Loaded {len(df)} employee records.\n")
        
        # Check for required columns
        if "JobTitle" not in df.columns:
            print("Error: 'JobTitle' column not found in dataset!")
            return
        
        # Get user input
        keyword = get_user_input()
        
        # Search for matches
        print(f"\nSearching for '{keyword}'...")
        df_matches = search_employees(df, keyword)
        
        # Calculate statistics
        stats = calculate_statistics(df_matches)
        
        # Display results
        display_results(keyword, stats)
        
        # Save results
        if stats['count'] > 0:
            save_choice = input("Do you want to save these results? (y/n): ").strip().lower()
            if save_choice == 'y':
                save_results(df_matches, keyword)
        
        # Ask if user wants to search again
        print("\n" + "=" * 50)
        again = input("Do you want to perform another search? (y/n): ").strip().lower()
        if again == 'y':
            main()  # Recursive call for another search
        else:
            print("\nThank you for using the Employee Investigation Tool!")
            print("=" * 50 + "\n")
    
    except KeyboardInterrupt:
        print("\n\nSearch interrupted by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
