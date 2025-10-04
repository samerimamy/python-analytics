@app.get("/mis")
def mis_analytics():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "test.csv")

    # Step 1: Check if file exists
    if not os.path.exists(csv_path):
        return {"error": f"File not found at {csv_path}"}

    # Step 2: Try to read file
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        return {"error": f"Error reading CSV: {str(e)}"}

    # Step 3: Show found columns
    cols = list(df.columns)
    required_cols = ["Semester", "Course", "EmployedWithin6Months", "GPA"]
    missing = [c for c in required_cols if c not in cols]

    # Step 4: If columns are missing, report and stop
    if missing:
        return {
            "error": f"Missing columns: {missing}",
            "found_columns": cols,
            "first_rows": df.head().to_dict(orient="records")
        }

    # Step 5: If all OK, do the analytics
    try:
        result = {
            "Total": int(len(df)),
            "BySemester": df["Semester"].value_counts().to_dict(),
            "ByCourse": df["Course"].value_counts().to_dict(),
            "EmploymentRate": float(df["EmployedWithin6Months"].mean()),
            "AverageGPA": float(df["GPA"].mean())
        }
    except Exception as e:
        return {"error": f"Error during analysis: {str(e)}"}

    return result
