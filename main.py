from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import pandas as pd
import os

FILENAME = "data.csv"
CLEANED_FILE = "cleaned_data.csv"


# ==========================
# Helper: fill QTableWidget
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
# TASK 5 – High Earners
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

app.exec_()
