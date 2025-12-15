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