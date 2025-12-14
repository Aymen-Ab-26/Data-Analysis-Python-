from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import pandas as pd
import os

FILENAME = "data.csv"
CLEANED_FILE = "cleaned_data.csv"
AGENCY_FILE = "agency_codes.csv"
MERGED_FILE = "merged_data.csv"


# ==========================
# fill QTableWidget
# ==========================
def fill_table(df):
    win.tw.setRowCount(0)
    win.tw.setColumnCount(len(df.columns))
    win.tw.setHorizontalHeaderLabels(df.columns)

    for r in range(len(df)):
        win.tw.insertRow(r)
        for c in range(len(df.columns)):
            win.tw.setItem(
                r, c,
                QTableWidgetItem(str(df.iat[r, c]))
            )

    win.tw.resizeColumnsToContents()


# ==========================
# TASK 1 – Preview Data
# ==========================
def preview():
    if not os.path.exists(FILENAME):
        QMessageBox.critical(win, "Error", "data.csv not found")
        return

    try:
        n = int(win.le_lines.text())
        if n <= 0:
            raise ValueError
    except:
        QMessageBox.critical(win, "Error", "Enter a valid positive number")
        return

    df = pd.read_csv(FILENAME, low_memory=False, encoding="utf-8")

    if n > len(df):
        QMessageBox.critical(win, "Error", "Number exceeds dataset size")
        return

    fill_table(df.head(n))


# ==========================
# TASK 2 – Search for Chief
# ==========================
def searchForChief():
    if not os.path.exists(FILENAME):
        QMessageBox.critical(win, "Error", "data.csv not found")
        return

    df = pd.read_csv(FILENAME, low_memory=False, encoding="utf-8")

    if "JobTitle" not in df.columns:
        QMessageBox.critical(win, "Error", "Column JobTitle not found")
        return

    df_chief = df[df["JobTitle"].str.contains("chief", case=False, na=False)]

    if df_chief.empty:
        QMessageBox.information(win, "Result", "No matching rows")
        win.tw.setRowCount(0)
        return

    fill_table(df_chief)


# ==========================
# TASK 3 – Two Columns
# ==========================
def getTwoColumns():
    if not os.path.exists(FILENAME):
        QMessageBox.critical(win, "Error", "data.csv not found")
        return

    df = pd.read_csv(FILENAME, low_memory=False, encoding="utf-8")

    required = {"EmployeeName", "JobTitle"}
    if not required.issubset(df.columns):
        QMessageBox.critical(win, "Error", "Required columns not found")
        return

    fill_table(df[list(required)])


# ==========================
# TASK 4 – Clean Data
# ==========================
def check_column(column):
    return column.str.contains("Not Provided", case=False, na=False)

def cleanData():
    df = pd.read_csv(FILENAME, low_memory=False)

    df= df.drop(columns=['Notes'])
    #first i will remove any lines with " Not provided" to only have useful data
    df_as_text = df.astype(str)
    contains_not_provided = df_as_text.apply(check_column)
    rows_with_not_provided = contains_not_provided.any(axis=1)
    df = df[~rows_with_not_provided]
    df = df.reset_index(drop=True) #update indexes


    #replace missing numerics with 0
    numeric_cols = ["BasePay", "OvertimePay", "OtherPay", "Benefits", "TotalPay", "TotalPayBenefits","Year"]
    df[numeric_cols] = df[numeric_cols].fillna(0)

    #replace missing strings or objects with N/A
    text_cols = ['EmployeeName', 'JobTitle', 'Agency', 'Status']
    df[text_cols] = df[text_cols].fillna("N/A")
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)

    df.to_csv("cleaned_data.csv", index=False) 

    QMessageBox.information(win, "Success", "Data cleaned successfully")
    fill_table(df)


# ==========================
# TASK 5a – High Earners
# ==========================
def highEarners():
    if not os.path.exists(CLEANED_FILE):
        QMessageBox.critical(win, "Error", "Run data cleaning first")
        return

    df = pd.read_csv(CLEANED_FILE, low_memory=False, encoding="utf-8")

    if "TotalPay" not in df.columns:
        QMessageBox.critical(win, "Error", "Column TotalPay not found")
        return

    avg = df["TotalPay"].mean()
    df_high = df[df["TotalPay"] > avg]

    fill_table(df_high)


# ==========================
# TASK 5b – Employees from 2013
# ==========================
def employees2013():
    if not os.path.exists(CLEANED_FILE):
        QMessageBox.critical(win, "Error", "Run data cleaning first")
        return

    df = pd.read_csv(CLEANED_FILE, low_memory=False, encoding="utf-8")

    if "Year" not in df.columns:
        QMessageBox.critical(win, "Error", "Column Year not found")
        return

    # Filter employees from year 2013
    df_2013 = df[df["Year"] == 2013]

    if df_2013.empty:
        QMessageBox.information(win, "Result", "No employees found from year 2013")
        win.tw.setRowCount(0)
        return

    # Display count in message
    count = len(df_2013)
    QMessageBox.information(win, "Result", f"Found {count} employees from year 2013")
    
    fill_table(df_2013)


# ==========================
# TASK 5c – Police Employees
# ==========================
def policeEmployees():
    if not os.path.exists(CLEANED_FILE):
        QMessageBox.critical(win, "Error", "Run data cleaning first")
        return

    df = pd.read_csv(CLEANED_FILE, low_memory=False, encoding="utf-8")

    if "JobTitle" not in df.columns:
        QMessageBox.critical(win, "Error", "Column JobTitle not found")
        return

    # Filter employees with "POLICE" in JobTitle
    df_police = df[df["JobTitle"].str.contains("POLICE", case=False, na=False)]

    if df_police.empty:
        QMessageBox.information(win, "Result", "No police employees found")
        win.tw.setRowCount(0)
        return

    # Display count in message
    count = len(df_police)
    QMessageBox.information(win, "Result", f"Found {count} police employees")
    
    fill_table(df_police)


# ==========================
# TASK 6 – Create Computed Columns (Is_Manager)
# ==========================
def addManagerColumn():
    if not os.path.exists(CLEANED_FILE):
        QMessageBox.critical(win, "Error", "Run data cleaning first")
        return

    df = pd.read_csv(CLEANED_FILE, low_memory=False, encoding="utf-8")

    if "JobTitle" not in df.columns:
        QMessageBox.critical(win, "Error", "Column JobTitle not found")
        return

    # Create Is_Manager column
    # True if JobTitle contains "MANAGER" or "CHIEF" (case insensitive)
    df["Is_Manager"] = df["JobTitle"].str.contains("MANAGER|CHIEF", case=False, na=False)

    # Save the updated dataframe
    df.to_csv(CLEANED_FILE, index=False)

    # Show summary
    manager_count = df["Is_Manager"].sum()
    total_count = len(df)
    
    QMessageBox.information(
        win, 
        "Success", 
        f"Is_Manager column added!\n\nManagers/Chiefs: {manager_count}\nTotal Employees: {total_count}"
    )
    
    # Display the dataframe with new column
    fill_table(df)


# ==========================
# TASK 7 – Summary Statistics
# ==========================
def showSummaryStats():
    if not os.path.exists(CLEANED_FILE):
        QMessageBox.critical(win, "Error", "Run data cleaning first")
        return

    df = pd.read_csv(CLEANED_FILE, low_memory=False, encoding="utf-8")

    # Clear the list widget
    win.lw.clear()

    # 1. Total number of employees
    total_employees = len(df)
    win.lw.addItem(f"=== SUMMARY STATISTICS ===")
    win.lw.addItem("")
    win.lw.addItem(f"Total Employees: {total_employees}")
    win.lw.addItem("")

    # 2. Average BasePay
    if "BasePay" in df.columns:
        avg_base_pay = df["BasePay"].mean()
        win.lw.addItem(f"Average BasePay: ${avg_base_pay:,.2f}")
    
    # 3. Average TotalPay
    if "TotalPay" in df.columns:
        avg_total_pay = df["TotalPay"].mean()
        win.lw.addItem(f"Average TotalPay: ${avg_total_pay:,.2f}")
    
    win.lw.addItem("")

    # 4. Top 5 most common job titles
    if "JobTitle" in df.columns:
        win.lw.addItem("=== TOP 5 JOB TITLES ===")
        top_titles = df["JobTitle"].value_counts().head(5)
        for i, (title, count) in enumerate(top_titles.items(), 1):
            win.lw.addItem(f"{i}. {title}: {count} employees")
    
    win.lw.addItem("")
    
    # 5. Year distribution
    if "Year" in df.columns:
        win.lw.addItem("=== YEAR DISTRIBUTION ===")
        year_counts = df["Year"].value_counts().sort_index()
        for year, count in year_counts.items():
            win.lw.addItem(f"Year {int(year)}: {count} employees")

    QMessageBox.information(win, "Success", "Summary statistics displayed in the list widget")


# ==========================
# TASK 8 – Group-based Aggregation (Average TotalPay per Year)
# ==========================
def groupByYear():
    if not os.path.exists(CLEANED_FILE):
        QMessageBox.critical(win, "Error", "Run data cleaning first")
        return

    df = pd.read_csv(CLEANED_FILE, low_memory=False, encoding="utf-8")

    if "Year" not in df.columns or "TotalPay" not in df.columns:
        QMessageBox.critical(win, "Error", "Required columns not found")
        return

    # Group by Year and calculate average TotalPay
    grouped = df.groupby("Year")["TotalPay"].mean().reset_index()
    grouped.columns = ["Year", "Average_TotalPay"]
    
    # Round to 2 decimal places
    grouped["Average_TotalPay"] = grouped["Average_TotalPay"].round(2)
    
    # Sort by Year
    grouped = grouped.sort_values("Year")

    # Display in list widget
    win.lw.clear()
    win.lw.addItem("=== AVERAGE TOTAL PAY PER YEAR ===")
    win.lw.addItem("")
    
    for _, row in grouped.iterrows():
        year = int(row["Year"])
        avg_pay = row["Average_TotalPay"]
        win.lw.addItem(f"Year {year}: ${avg_pay:,.2f}")

    # Also display in table
    fill_table(grouped)
    
    QMessageBox.information(win, "Success", "Group analysis completed")


# ==========================
# TASK 9 – Merge with Agency Codes
# ==========================
def mergeWithAgencyCodes():
    if not os.path.exists(CLEANED_FILE):
        QMessageBox.critical(win, "Error", "Run data cleaning first")
        return
    
    if not os.path.exists(AGENCY_FILE):
        QMessageBox.critical(
            win, 
            "Error", 
            f"'{AGENCY_FILE}' not found!\n\nPlease create the agency mapping file first.\nYou can run 'create_agency_codes.py' to generate a sample file."
        )
        return

    try:
        # Load both files
        df_main = pd.read_csv(CLEANED_FILE, low_memory=False, encoding="utf-8")
        df_agency = pd.read_csv(AGENCY_FILE, encoding="utf-8")
        
        if "Agency" not in df_main.columns:
            QMessageBox.critical(win, "Error", "Column 'Agency' not found in main dataset")
            return
        
        if "Agency" not in df_agency.columns:
            QMessageBox.critical(win, "Error", "Column 'Agency' not found in agency_codes.csv")
            return
        
        # Perform left merge (keep all records from main dataset)
        df_merged = pd.merge(df_main, df_agency, on="Agency", how="left")
        
        # Save merged data
        df_merged.to_csv(MERGED_FILE, index=False)
        
        # Count matched vs unmatched
        matched = df_merged[df_agency.columns[1]].notna().sum()  # Check if agency code exists
        total = len(df_merged)
        
        QMessageBox.information(
            win,
            "Success",
            f"Data merged successfully!\n\nTotal records: {total}\nMatched agencies: {matched}\nUnmatched: {total - matched}\n\nSaved to '{MERGED_FILE}'"
        )
        
        # Display merged data
        fill_table(df_merged)
        
    except Exception as e:
        QMessageBox.critical(win, "Error", f"Merge failed: {str(e)}")


# ==========================
# Close App
# ==========================
def close_app():
    win.close()


# ==========================
# Main
# ==========================
app = QApplication([])
win = loadUi("interface.ui")
win.show()

win.b_preview.clicked.connect(preview)
win.b_search.clicked.connect(searchForChief)
win.b_two.clicked.connect(getTwoColumns)
win.b_clean.clicked.connect(cleanData)
win.b_high.clicked.connect(highEarners)
win.b_quit.clicked.connect(close_app)

# Connect Task 5b button (pushButton_9)
win.pushButton_9.clicked.connect(employees2013)

# Connect Task 5c button (pushButton_7)
win.pushButton_7.clicked.connect(policeEmployees)

# Connect Task 6 button
win.b_manager.clicked.connect(addManagerColumn)

# Connect Task 7 button
win.b_summary.clicked.connect(showSummaryStats)

# Connect Task 8 button
win.b_groupby.clicked.connect(groupByYear)

# Connect Task 9 button
win.b_merge.clicked.connect(mergeWithAgencyCodes)

app.exec_()