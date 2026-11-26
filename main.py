
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ==========================================
# 1. MAIN APPLICATION WINDOW
# ==========================================

root = tk.Tk()
root.title("DataPilot Analytics")
root.geometry("1100x700")
root.minsize(900, 600)
root.configure(bg="#F4F6F9")

# Global variables
file_path = ""
df = None
report_df = None
# ==========================================
# 2. COLORS
# ==========================================

SIDEBAR_COLOR = "#172554"
BUTTON_COLOR = "#1E3A5F"
ACTIVE_COLOR = "#2563EB"
BACKGROUND_COLOR = "#F4F6F9"

# ==========================================
# 3. MAIN CONTAINER
# ==========================================

main_container = tk.Frame(root, bg=BACKGROUND_COLOR)
main_container.pack(fill="both", expand=True)

# ==========================================
# 4. SIDEBAR
# ==========================================

sidebar = tk.Frame(
    main_container,
    bg=SIDEBAR_COLOR,
    width=240
)

sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

logo = tk.Label(
    sidebar,
    text="DataPilot",
    font=("Arial", 22, "bold"),
    bg=SIDEBAR_COLOR,
    fg="white"
)
logo.pack(pady=(30, 5))

logo_subtitle = tk.Label(
    sidebar,
    text="ANALYTICS PLATFORM",
    font=("Arial", 9),
    bg=SIDEBAR_COLOR,
    fg="#94A3B8"
)
logo_subtitle.pack(pady=(0, 35))

# ==========================================
# 5. CONTENT AREA
# ==========================================


# ==========================================
# 5. CONTENT AREA WITH SCROLLING
# ==========================================

content_container = tk.Frame(
    main_container,
    bg=BACKGROUND_COLOR
)
content_container.pack(side="right", fill="both", expand=True)

content_canvas = tk.Canvas(
    content_container,
    bg=BACKGROUND_COLOR,
    highlightthickness=0
)

vertical_scrollbar = ttk.Scrollbar(
    content_container,
    orient="vertical",
    command=content_canvas.yview
)

content_canvas.configure(
    yscrollcommand=vertical_scrollbar.set
)

vertical_scrollbar.pack(side="right", fill="y")
content_canvas.pack(side="left", fill="both", expand=True)

content_area = tk.Frame(
    content_canvas,
    bg=BACKGROUND_COLOR
)

content_window = content_canvas.create_window(
    (0, 0),
    window=content_area,
    anchor="nw"
)

def update_scroll_region(event):
    content_canvas.configure(
        scrollregion=content_canvas.bbox("all")
    )

def resize_content(event):
    content_canvas.itemconfigure(
        content_window,
        width=event.width
    )

content_area.bind("<Configure>", update_scroll_region)
content_canvas.bind("<Configure>", resize_content)


# ==========================================
# 6. CLEAR PREVIOUS PAGE
# ==========================================

def clear_content():

    for widget in content_area.winfo_children():
        widget.destroy()

# ==========================================
# 7. DASHBOARD PAGE
# ==========================================


def show_dashboard():
    clear_content()

    heading = tk.Label(
        content_area,
        text="Dashboard",
        font=("Arial", 24, "bold"),
        bg=BACKGROUND_COLOR,
        fg=SIDEBAR_COLOR
    )
    heading.pack(anchor="w", padx=35, pady=(25, 5))

    subtitle = tk.Label(
        content_area,
        text="Welcome to your data analytics workspace.",
        font=("Arial", 11),
        bg=BACKGROUND_COLOR,
        fg="#64748B"
    )
    subtitle.pack(anchor="w", padx=35)

    # KPI values
    total_records = "--"
    total_columns = "--"
    total_revenue = "--"
    total_profit = "--"
    average_revenue = "--"

    if df is not None:
        total_records = f"{len(df):,}"
        total_columns = f"{len(df.columns):,}"

        # Find Revenue and Profit columns
        column_lookup = {
            str(col).strip().lower(): col
            for col in df.columns
        }

        revenue_column = column_lookup.get("revenue")
        if revenue_column is None:
            revenue_column = column_lookup.get("total revenue")

        profit_column = column_lookup.get("profit")

        if revenue_column is not None:
            revenue_data = pd.to_numeric(
                df[revenue_column].astype(str).str.replace(
                    ",", "", regex=False
                ),
                errors="coerce"
            )

            total_revenue = f"{revenue_data.sum():,.2f}"
            average_revenue = f"{revenue_data.mean():,.2f}"

        if profit_column is not None:
            profit_data = pd.to_numeric(
                df[profit_column].astype(str).str.replace(
                    ",", "", regex=False
                ),
                errors="coerce"
            )

            total_profit = f"{profit_data.sum():,.2f}"

    # KPI cards
    cards_frame = tk.Frame(
        content_area,
        bg=BACKGROUND_COLOR
    )
    cards_frame.pack(fill="x", padx=25, pady=30)

    kpis = [
        ("Total Records", total_records, "#2563EB"),
        ("Total Columns", total_columns, "#7C3AED"),
        ("Total Revenue", total_revenue, "#15803D"),
        ("Total Profit", total_profit, "#D97706"),
        ("Average Revenue", average_revenue, "#0891B2")
    ]

    for index, (title, value, color) in enumerate(kpis):
        card = tk.Frame(
            cards_frame,
            bg="white",
            padx=15,
            pady=20
        )

        card.grid(
            row=index // 3,
            column=index % 3,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        tk.Label(
            card,
            text=title,
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#64748B"
        ).pack(anchor="w")

        tk.Label(
            card,
            text=value,
            font=("Arial", 19, "bold"),
            bg="white",
            fg=color
        ).pack(anchor="w", pady=10)

    for column in range(3):
        cards_frame.grid_columnconfigure(
            column,
            weight=1
        )

    if df is None:
        tk.Label(
            content_area,
            text="Import a dataset to view your analytics summary.",
            font=("Arial", 11),
            bg=BACKGROUND_COLOR,
            fg="#64748B"
        ).pack(anchor="w", padx=35, pady=10)


    # Revenue vs Profit Chart
    if df is not None and revenue_column is not None and profit_column is not None:

        chart_heading = tk.Label(
            content_area,
            text="Revenue vs Profit Analysis",
            font=("Arial", 16, "bold"),
            bg=BACKGROUND_COLOR,
            fg=SIDEBAR_COLOR
        )
        chart_heading.pack(anchor="w", padx=35, pady=(20, 5))

        chart_frame = tk.Frame(
            content_area,
            bg="white"
        )
        chart_frame.pack(fill="x", padx=35, pady=10)

        fig = Figure(figsize=(8, 3), dpi=100)
        ax = fig.add_subplot(111)

        ax.bar(
            ["Total Revenue", "Total Profit"],
            [revenue_data.sum(), profit_data.sum()],
            color=["#15803D", "#D97706"]
        )

        ax.set_title("Revenue vs Profit")
        ax.set_ylabel("Amount")

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Dataset Summary
        summary_heading = tk.Label(
            content_area,
            text="Dataset Summary",
            font=("Arial", 16, "bold"),
            bg=BACKGROUND_COLOR,
            fg=SIDEBAR_COLOR
        )
        summary_heading.pack(anchor="w", padx=35, pady=(25, 10))

        revenue_clean = revenue_data.dropna()
        profit_clean = profit_data.dropna()

        highest_revenue = (
            f"{revenue_clean.max():,.2f}"
            if not revenue_clean.empty else "--"
        )

        minimum_revenue = (
            f"{revenue_clean.min():,.2f}"
            if not revenue_clean.empty else "--"
        )

        highest_profit = (
            f"{profit_clean.max():,.2f}"
            if not profit_clean.empty else "--"
        )

        minimum_profit = (
            f"{profit_clean.min():,.2f}"
            if not profit_clean.empty else "--"
        )

        summary_frame = tk.Frame(
            content_area,
            bg=BACKGROUND_COLOR
        )
        summary_frame.pack(fill="x", padx=25, pady=10)

        summary_items = [
            ("Highest Revenue", highest_revenue),
            ("Minimum Revenue", minimum_revenue),
            ("Highest Profit", highest_profit),
            ("Minimum Profit", minimum_profit)
        ]

        for index, (title, value) in enumerate(summary_items):
            summary_card = tk.Frame(
                summary_frame,
                bg="white",
                padx=15,
                pady=18
            )

            summary_card.grid(
                row=index // 2,
                column=index % 2,
                padx=10,
                pady=10,
                sticky="nsew"
            )

            tk.Label(
                summary_card,
                text=title,
                font=("Arial", 11, "bold"),
                bg="white",
                fg="#64748B"
            ).pack(anchor="w")

            tk.Label(
                summary_card,
                text=value,
                font=("Arial", 16, "bold"),
                bg="white",
                fg=SIDEBAR_COLOR
            ).pack(anchor="w", pady=8)

        summary_frame.grid_columnconfigure(0, weight=1)
        summary_frame.grid_columnconfigure(1, weight=1)


        # Top 5 Products by Revenue
        product_column = column_lookup.get("product")

        if product_column is not None and revenue_column is not None:

            product_heading = tk.Label(
                content_area,
                text="Top 5 Products by Revenue",
                font=("Arial", 16, "bold"),
                bg=BACKGROUND_COLOR,
                fg=SIDEBAR_COLOR
            )
            product_heading.pack(
                anchor="w",
                padx=35,
                pady=(25, 10)
            )

            product_data = df[
                [product_column, revenue_column]
            ].copy()

            product_data[revenue_column] = pd.to_numeric(
                product_data[revenue_column].astype(str).str.replace(
                    ",", "", regex=False
                ),
                errors="coerce"
            )

            top_products = (
                product_data
                .dropna()
                .groupby(product_column)[revenue_column]
                .sum()
                .nlargest(5)
                .sort_values()
            )

            product_frame = tk.Frame(
                content_area,
                bg="white"
            )
            product_frame.pack(
                fill="x",
                padx=35,
                pady=10
            )

            product_fig = Figure(figsize=(8, 3.5), dpi=100)
            product_ax = product_fig.add_subplot(111)

            product_ax.barh(
                top_products.index.astype(str),
                top_products.values,
                color="#2563EB"
            )

            # Display revenue values on bars
            for index, value in enumerate(top_products.values):
                product_ax.text(
                    value,
                    index,
                    f"{value:,.2f}",
                    va="center",
                    ha="left",
                    fontsize=9,
                    fontweight="bold"
                )

            product_ax.set_xlim(
                0,
                max(top_products.values) * 1.18
            )


            product_ax.set_title("Top 5 Products by Revenue")
            product_ax.set_xlabel("Revenue")

            product_fig.tight_layout()

            product_canvas = FigureCanvasTkAgg(
                product_fig,
                master=product_frame
            )
            product_canvas.draw()
            product_canvas.get_tk_widget().pack(
                fill="both",
                expand=True
            )

# ==========================================
# 8. FILE SELECTION
# ==========================================

def browse_file():

    global file_path, df

    selected_file = filedialog.askopenfilename(
        title="Select Excel or CSV File",
        filetypes=[
            ("Supported Files", "*.csv *.xlsx"),
            ("CSV Files", "*.csv"),
            ("Excel Files", "*.xlsx")
        ]
    )

    if selected_file:

        file_path = selected_file
        df = None

        file_entry.config(state="normal")
        file_entry.delete(0, tk.END)
        file_entry.insert(0, os.path.basename(file_path))
        file_entry.config(state="readonly")

        status_label.config(
            text="File selected. Click Read Data to load it.",
            fg="#2563EB"
        )

        rows_label.config(text="Total Rows: --")
        columns_label.config(text="Total Columns: --")
        headings_label.config(text="Column Headings: --")

        clear_table()

# ==========================================
# 9. READ CSV OR EXCEL FILE
# ==========================================

def read_file():

    global df

    if not file_path:

        messagebox.showerror(
            "File Missing",
            "Please select a CSV or Excel file first."
        )
        return

    try:

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".csv":

            try:
                df = pd.read_csv(file_path, encoding="utf-8-sig")
            except UnicodeDecodeError:
                df = pd.read_csv(file_path, encoding="cp1252")

        elif extension == ".xlsx":

            df = pd.read_excel(file_path, engine="openpyxl")

        else:

            messagebox.showerror(
                "Unsupported Format",
                "Please select a CSV or XLSX file."
            )
            return

        if df.empty:
            messagebox.showwarning(
                "Empty Dataset",
                "The selected file contains no data rows."
            )

        rows_label.config(
            text=f"Total Rows: {len(df):,}"
        )

        columns_label.config(
            text=f"Total Columns: {len(df.columns)}"
        )

        headings_label.config(
            text="Column Headings: " + ", ".join(
                str(column) for column in df.columns
            )
        )

        display_table()

        status_label.config(
            text="Dataset loaded successfully!",
            fg="#15803D"
        )

        messagebox.showinfo(
            "Success",
            "Your dataset has been loaded successfully!"
        )

    except Exception as error:

        df = None

        messagebox.showerror(
            "Reading Error",
            f"Unable to read the selected file.\n\n{error}"
        )

# ==========================================
# 10. CLEAR TABLE
# ==========================================

def clear_table():

    for item in data_table.get_children():
        data_table.delete(item)

    data_table["columns"] = ()

# ==========================================
# 11. DISPLAY DATA PREVIEW
# ==========================================

def display_table():

    clear_table()

    if df is None:
        return

    # Show a maximum of 100 rows in the preview
    preview = df.head(100)

    column_names = [str(col) for col in df.columns]

    data_table["columns"] = column_names

    for column in column_names:

        data_table.heading(column, text=column)

        data_table.column(
            column,
            width=130,
            minwidth=80,
            anchor="center"
        )

    for _, row in preview.iterrows():

        values = [
            "" if pd.isna(value) else str(value)
            for value in row
        ]

        data_table.insert("", tk.END, values=values)

# ==========================================
# DYNAMIC COLUMN DETECTION
# ==========================================

def detect_columns():

    global df

    text_columns = []
    numeric_columns = []

    if df is None:
        return text_columns, numeric_columns

    for column in df.columns:

        series = df[column]

        # Check whether the column is already numeric
        if pd.api.types.is_numeric_dtype(series):
            numeric_columns.append(column)

        else:

            # Try converting text values into numbers
            converted = pd.to_numeric(
                series.dropna().astype(str).str.replace(",", "", regex=False),
                errors="coerce"
            )

            # If all non-empty values are numeric,
            # classify the column as numeric
            if len(converted) > 0 and converted.notna().all():

                numeric_columns.append(column)

            else:

                text_columns.append(column)

    return text_columns, numeric_columns

# ==========================================
# DATA OVERVIEW PAGE
# ==========================================

def show_data_overview():

    clear_content()

    heading = tk.Label(
        content_area,
        text="Data Overview",
        font=("Arial", 24, "bold"),
        bg=BACKGROUND_COLOR,
        fg=SIDEBAR_COLOR
    )

    heading.pack(anchor="w", padx=30, pady=(25, 5))

    if df is None:

        tk.Label(
            content_area,
            text="Please import and read a dataset first.",
            font=("Arial", 12),
            bg=BACKGROUND_COLOR,
            fg="#DC2626"
        ).pack(anchor="w", padx=30, pady=20)

        return

    text_columns, numeric_columns = detect_columns()

    # Dataset information

    info_frame = tk.Frame(
        content_area,
        bg="white",
        padx=20,
        pady=15
    )

    info_frame.pack(fill="x", padx=30, pady=15)

    tk.Label(
        info_frame,
        text=f"Total Rows: {len(df):,}",
        font=("Arial", 12, "bold"),
        bg="white",
        fg=SIDEBAR_COLOR
    ).pack(anchor="w", pady=5)

    tk.Label(
        info_frame,
        text=f"Total Columns: {len(df.columns)}",
        font=("Arial", 12, "bold"),
        bg="white",
        fg=SIDEBAR_COLOR
    ).pack(anchor="w", pady=5)

    # Text columns section

    text_frame = tk.Frame(
        content_area,
        bg="white",
        padx=20,
        pady=15
    )

    text_frame.pack(fill="x", padx=30, pady=10)

    tk.Label(
        text_frame,
        text=f"Text Columns ({len(text_columns)})",
        font=("Arial", 14, "bold"),
        bg="white",
        fg="#2563EB"
    ).pack(anchor="w", pady=5)

    tk.Label(
        text_frame,
        text=", ".join(map(str, text_columns)) or "No text columns detected",
        font=("Arial", 11),
        bg="white",
        fg="#475569",
        wraplength=700,
        justify="left"
    ).pack(anchor="w", pady=5)

    # Numeric columns section

    numeric_frame = tk.Frame(
        content_area,
        bg="white",
        padx=20,
        pady=15
    )

    numeric_frame.pack(fill="x", padx=30, pady=10)

    tk.Label(
        numeric_frame,
        text=f"Numeric Columns ({len(numeric_columns)})",
        font=("Arial", 14, "bold"),
        bg="white",
        fg="#15803D"
    ).pack(anchor="w", pady=5)

    tk.Label(
        numeric_frame,
        text=", ".join(map(str, numeric_columns)) or "No numeric columns detected",
        font=("Arial", 11),
        bg="white",
        fg="#475569",
        wraplength=700,
        justify="left"
    ).pack(anchor="w", pady=5)

    # Detection status

    tk.Label(
        content_area,
        text="Column detection completed successfully!",
        font=("Arial", 10),
        bg=BACKGROUND_COLOR,
        fg="#15803D"
    ).pack(anchor="w", padx=35, pady=10)
# ==========================================
# 12. IMPORT DATA PAGE
# ==========================================

def show_import_page():

    clear_content()

    heading = tk.Label(
        content_area,
        text="Import Data",
        font=("Arial", 24, "bold"),
        bg=BACKGROUND_COLOR,
        fg=SIDEBAR_COLOR
    )
    heading.pack(anchor="w", padx=30, pady=(25, 5))

    subtitle = tk.Label(
        content_area,
        text="Import your Excel or CSV dataset for analysis.",
        font=("Arial", 11),
        bg=BACKGROUND_COLOR,
        fg="#64748B"
    )
    subtitle.pack(anchor="w", padx=30, pady=(0, 20))

    # File selection section

    file_frame = tk.Frame(
        content_area,
        bg="white",
        padx=20,
        pady=20
    )
    file_frame.pack(fill="x", padx=30)

    tk.Label(
        file_frame,
        text="Select Dataset",
        font=("Arial", 13, "bold"),
        bg="white",
        fg=SIDEBAR_COLOR
    ).pack(anchor="w", pady=(0, 12))

    global file_entry

    file_entry = tk.Entry(
        file_frame,
        font=("Arial", 10),
        state="readonly",
        width=45
    )
    file_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

    tk.Button(
        file_frame,
        text="Browse File",
        font=("Arial", 10, "bold"),
        bg=ACTIVE_COLOR,
        fg="white",
        relief="flat",
        padx=15,
        pady=8,
        cursor="hand2",
        command=browse_file
    ).pack(side="left")

    tk.Button(
        file_frame,
        text="Read Data",
        font=("Arial", 10, "bold"),
        bg="#15803D",
        fg="white",
        relief="flat",
        padx=15,
        pady=8,
        cursor="hand2",
        command=read_file
    ).pack(side="left", padx=(10, 0))

    global status_label

    status_label = tk.Label(
        content_area,
        text="No dataset loaded.",
        font=("Arial", 10),
        bg=BACKGROUND_COLOR,
        fg="#64748B"
    )
    status_label.pack(anchor="w", padx=35, pady=12)

    # Dataset summary

    summary_frame = tk.Frame(
        content_area,
        bg="white",
        padx=20,
        pady=15
    )
    summary_frame.pack(fill="x", padx=30, pady=5)

    global rows_label, columns_label, headings_label

    rows_label = tk.Label(
        summary_frame,
        text="Total Rows: --",
        font=("Arial", 12, "bold"),
        bg="white",
        fg=SIDEBAR_COLOR
    )
    rows_label.pack(anchor="w", pady=5)

    columns_label = tk.Label(
        summary_frame,
        text="Total Columns: --",
        font=("Arial", 12, "bold"),
        bg="white",
        fg=SIDEBAR_COLOR
    )
    columns_label.pack(anchor="w", pady=5)

    headings_label = tk.Label(
        summary_frame,
        text="Column Headings: --",
        font=("Arial", 10),
        bg="white",
        fg="#475569",
        wraplength=750,
        justify="left"
    )
    headings_label.pack(anchor="w", pady=5)

    # Data preview table

    table_frame = tk.Frame(content_area, bg="white")
    table_frame.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=15
    )

    global data_table

    data_table = ttk.Treeview(
        table_frame,
        show="headings"
    )

    vertical_scroll = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=data_table.yview
    )

    horizontal_scroll = ttk.Scrollbar(
        table_frame,
        orient="horizontal",
        command=data_table.xview
    )

    data_table.configure(
        yscrollcommand=vertical_scroll.set,
        xscrollcommand=horizontal_scroll.set
    )

    data_table.pack(side="top", fill="both", expand=True)
    vertical_scroll.pack(side="right", fill="y")
    horizontal_scroll.pack(side="bottom", fill="x")

# ==========================================
# 13. NAVIGATION
# ==========================================

menu_items = [
    "Dashboard",
    "Import Data",
    "Data Overview",
    "Report Builder",
    "Chart Builder",
    "Export Reports"
]

navigation_buttons = []


def show_report_builder():
    clear_content()

    if df is None:
        messagebox.showwarning(
            "No Data",
            "Please import a dataset first."
        )
        return

    text_columns, numeric_columns = detect_columns()

    if not text_columns or not numeric_columns:
        messagebox.showwarning(
            "Missing Columns",
            "The dataset needs text and numeric columns."
        )
        return

    tk.Label(
        content_area,
        text="Report Builder",
        font=("Arial", 22, "bold"),
        bg=BACKGROUND_COLOR,
        fg=SIDEBAR_COLOR
    ).pack(anchor="w", padx=20, pady=15)

    options_frame = tk.Frame(
        content_area,
        bg=BACKGROUND_COLOR
    )
    options_frame.pack(fill="x", padx=20, pady=10)

    tk.Label(options_frame, text="Group By:",
             bg=BACKGROUND_COLOR).grid(row=0, column=0, padx=5)

    group_box = ttk.Combobox(
        options_frame,
        values=text_columns,
        state="readonly",
        width=18
    )
    group_box.grid(row=0, column=1, padx=5)
    group_box.current(0)

    tk.Label(options_frame, text="Aggregation:",
             bg=BACKGROUND_COLOR).grid(row=0, column=2, padx=5)

    aggregation_box = ttk.Combobox(
        options_frame,
        values=["Sum", "Mean", "Average", "Max",
                "Min", "Count", "Median"],
        state="readonly",
        width=15
    )
    aggregation_box.grid(row=0, column=3, padx=5)
    aggregation_box.current(0)

    tk.Label(options_frame, text="Value Column:",
             bg=BACKGROUND_COLOR).grid(row=0, column=4, padx=5)

    value_box = ttk.Combobox(
        options_frame,
        values=numeric_columns,
        state="readonly",
        width=18
    )
    value_box.grid(row=0, column=5, padx=5)
    value_box.current(0)

    table_frame = tk.Frame(content_area)
    table_frame.pack(fill="both", expand=True, padx=20, pady=15)

    report_table = ttk.Treeview(
        table_frame,
        show="headings"
    )
    report_table.pack(fill="both", expand=True)

    
    def preview_report():
        global report_df

        try:
            group_column = group_box.get()
            value_column = value_box.get()
            aggregation = aggregation_box.get()

            functions = {
                "Sum": "sum",
                "Mean": "mean",
                "Average": "mean",
                "Max": "max",
                "Min": "min",
                "Count": "count",
                "Median": "median"
            }

            report = df.groupby(
                group_column,
                dropna=False
            )[value_column].agg(
                functions[aggregation]
            ).reset_index()

            report = report.sort_values(
                by=value_column,
                ascending=False
            )

            report_df = report.copy()

            report_table.delete(
                *report_table.get_children()
            )

            report_table["columns"] = [
                group_column,
                value_column
            ]

            for column in [group_column, value_column]:
                report_table.heading(
                    column,
                    text=column
                )
                report_table.column(
                    column,
                    width=180,
                    anchor="center"
                )

            for _, row in report.iterrows():
                report_table.insert(
                    "",
                    "end",
                    values=(
                        row[group_column],
                        round(row[value_column], 2)
                    )
                )

        except Exception as e:
            messagebox.showerror(
                "Report Error",
                str(e)
            )
      
    def export_excel():
        if report_df is None:
            messagebox.showwarning(
                "No Report",
                "Please generate a report first."
            )
            return

        save_path = filedialog.asksaveasfilename(
            initialdir=os.path.dirname(file_path),
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            initialfile="DataPilot_Report.xlsx"
        )

        if save_path:
            try:
                report_df.to_excel(
                    save_path,
                    index=False
                )
                messagebox.showinfo(
                    "Success",
                    "Excel report exported successfully!"
                )
            except Exception as e:
                messagebox.showerror(
                    "Export Error",
                    str(e)
                )


    def export_csv():
        if report_df is None:
            messagebox.showwarning(
                "No Report",
                "Please generate a report first."
            )
            return

        save_path = filedialog.asksaveasfilename(
            initialdir=os.path.dirname(file_path),
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            initialfile="DataPilot_Report.csv"
        )

        if save_path:
            try:
                report_df.to_csv(
                    save_path,
                    index=False
                )
                messagebox.showinfo(
                    "Success",
                    "CSV report exported successfully!"
                )
            except Exception as e:
                messagebox.showerror("Export Error", str(e))

    tk.Button(
        options_frame,
        text="Preview Report",
        command=preview_report,
        bg=SIDEBAR_COLOR,
        fg="white",
        padx=12,
        pady=5
    ).grid(row=1, column=0, columnspan=2, pady=15)


     # Export Excel button
    tk.Button(
        options_frame,
        text="Export Excel",
        command=export_excel,
        bg="#217346",
        fg="white",
        padx=12,
        pady=5
    ).grid(row=1, column=2, padx=5, pady=15)

    # Export CSV button
    tk.Button(
        options_frame,
        text="Export CSV",
        command=export_csv,
        bg="#2874A6",
        fg="white",
        padx=12,
        pady=5
    ).grid(row=1, column=3, padx=5, pady=15)



def show_chart_builder():
    clear_content()

    if df is None:
        messagebox.showwarning(
            "No Data",
            "Please import a dataset first."
        )
        return

    text_columns, numeric_columns = detect_columns()

    if not text_columns or not numeric_columns:
        messagebox.showwarning(
            "Missing Columns",
            "The dataset needs text and numeric columns."
        )
        return

    tk.Label(
        content_area,
        text="Chart Builder",
        font=("Arial", 22, "bold"),
        bg=BACKGROUND_COLOR,
        fg=SIDEBAR_COLOR
    ).pack(anchor="w", padx=20, pady=15)

    options_frame = tk.Frame(
        content_area,
        bg=BACKGROUND_COLOR
    )
    options_frame.pack(fill="x", padx=20, pady=10)

    tk.Label(
        options_frame,
        text="Category Column:",
        bg=BACKGROUND_COLOR
    ).grid(row=0, column=0, padx=5)

    category_box = ttk.Combobox(
        options_frame,
        values=text_columns,
        state="readonly",
        width=18
    )
    category_box.grid(row=0, column=1, padx=5)
    category_box.current(0)

    tk.Label(
        options_frame,
        text="Numeric Column:",
        bg=BACKGROUND_COLOR
    ).grid(row=0, column=2, padx=5)

    value_box = ttk.Combobox(
        options_frame,
        values=numeric_columns,
        state="readonly",
        width=18
    )
    value_box.grid(row=0, column=3, padx=5)
    value_box.current(0)

    tk.Label(
        options_frame,
        text="Chart Type:",
        bg=BACKGROUND_COLOR
    ).grid(row=0, column=4, padx=5)

    chart_box = ttk.Combobox(
        options_frame,
        values=["Bar", "Column", "Line", "Pie"],
        state="readonly",
        width=12
    )
    chart_box.grid(row=0, column=5, padx=5)
    chart_box.current(0)

    current_figure = None
    chart_frame = tk.Frame(
        content_area,
        bg="white"
    )
    chart_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=15
    )

    def generate_chart():
        try:
            category = category_box.get()
            value = value_box.get()
            chart_type = chart_box.get()

            chart_data = df.groupby(
                category,
                dropna=False
            )[value].sum().reset_index()

            chart_data = chart_data.sort_values(
                by=value,
                ascending=False
            )

            nonlocal current_figure
            fig = Figure(figsize=(8, 5), dpi=100)
            ax = fig.add_subplot(111)

            labels = chart_data[category].astype(str)
            values = chart_data[value]

            if chart_type == "Bar":
                ax.barh(labels, values)
                ax.invert_yaxis()

            elif chart_type == "Column":
                ax.bar(labels, values)
                ax.tick_params(axis="x", rotation=45)

            elif chart_type == "Line":
                ax.plot(labels, values, marker="o")
                ax.tick_params(axis="x", rotation=45)

            elif chart_type == "Pie":
                ax.pie(
                    values,
                    labels=labels,
                    autopct="%1.1f%%"
                )
            current_figure = fig
            ax.set_title(f"{value} by {category}")
            if chart_type != "Pie":
                ax.set_ylabel(value)
                fig.tight_layout()

            for widget in chart_frame.winfo_children():
                widget.destroy()

            canvas = FigureCanvasTkAgg(
                fig,
                master=chart_frame
            )
            canvas.draw()
            canvas.get_tk_widget().pack(
                fill="both",
                expand=True
            )

        except Exception as e:
            messagebox.showerror(
                "Chart Error",
                str(e)
            )




    def export_chart():
        if current_figure is None:
            messagebox.showwarning(
                "No Chart",
                "Please generate a chart first."
            )
            return

        save_path = filedialog.asksaveasfilename(
            initialdir=os.path.dirname(file_path),
            defaultextension=".png",
            filetypes=[("PNG Images", "*.png")],
            initialfile="DataPilot_Chart.png"
        )

        if save_path:
            try:
                current_figure.savefig(
                    save_path,
                    dpi=300,
                    bbox_inches="tight"
                )

                messagebox.showinfo(
                    "Success",
                    "Chart exported successfully!"
                )

            except Exception as e:
                messagebox.showerror(
                    "Export Error",
                    str(e)
                )

    tk.Button(
        options_frame,
        text="Generate Chart",
        command=generate_chart,
        bg=SIDEBAR_COLOR,
        fg="white",
        padx=12,
        pady=5
    ).grid(row=1, column=0, columnspan=2, pady=15)

    tk.Button(
        options_frame,
        text="Export PNG",
        command=export_chart,
        bg="#217346",
        fg="white",
        padx=12,
        pady=5
    ).grid(row=1, column=2, padx=10, pady=15)


def show_export_page():
    clear_content()

    tk.Label(
        content_area,
        text="Export Reports",
        font=("Arial", 22, "bold"),
        bg=BACKGROUND_COLOR,
        fg=SIDEBAR_COLOR
    ).pack(anchor="w", padx=20, pady=20)

    tk.Label(
        content_area,
        text="Export your generated reports in your preferred format.",
        font=("Arial", 11),
        bg=BACKGROUND_COLOR,
        fg="#64748B"
    ).pack(anchor="w", padx=20, pady=5)

    options_frame = tk.Frame(
        content_area,
        bg="white"
    )
    options_frame.pack(
        fill="x",
        padx=20,
        pady=25
    )

    def export_excel():
        if report_df is None:
            messagebox.showwarning(
                "No Report",
                "Please generate a report in Report Builder first."
            )
            return

        save_path = filedialog.asksaveasfilename(
            initialdir=os.path.dirname(file_path),
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            initialfile="DataPilot_Report.xlsx"
        )

        if save_path:
            try:
                report_df.to_excel(save_path, index=False)
                messagebox.showinfo(
                    "Success",
                    "Excel report exported successfully!"
                )
            except Exception as e:
                messagebox.showerror("Export Error", str(e))

    def export_csv():
        if report_df is None:
            messagebox.showwarning(
                "No Report",
                "Please generate a report in Report Builder first."
            )
            return

        save_path = filedialog.asksaveasfilename(
            initialdir=os.path.dirname(file_path),
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            initialfile="DataPilot_Report.csv"
        )

        if save_path:
            try:
                report_df.to_csv(save_path, index=False)
                messagebox.showinfo(
                    "Success",
                    "CSV report exported successfully!"
                )
            except Exception as e:
                messagebox.showerror("Export Error", str(e))

    tk.Button(
        options_frame,
        text="Export Excel",
        command=export_excel,
        bg="#217346",
        fg="white",
        padx=20,
        pady=10
    ).pack(side="left", padx=20, pady=20)

    tk.Button(
        options_frame,
        text="Export CSV",
        command=export_csv,
        bg="#2874A6",
        fg="white",
        padx=20,
        pady=10
    ).pack(side="left", padx=20, pady=20)

    
def show_page(page_name):

    for button in navigation_buttons:

        if button.cget("text") == page_name:
            button.config(bg=ACTIVE_COLOR)
        else:
            button.config(bg=BUTTON_COLOR)

    if page_name == "Dashboard":
        show_dashboard()

    elif page_name == "Import Data":
        show_import_page()

    elif page_name == "Data Overview":
        show_data_overview()

    elif page_name == "Report Builder":
        show_report_builder()

    elif page_name == "Chart Builder":
        show_chart_builder()

    elif page_name == "Export Reports":
        show_export_page()

    else:
        clear_content()

        tk.Label(
            content_area,
            text=page_name,
            font=("Arial", 24, "bold"),
            bg=BACKGROUND_COLOR,
            fg=SIDEBAR_COLOR
        ).pack(anchor="w", padx=30, pady=30)

        tk.Label(
            content_area,
            text="This module will be developed in the next stages.",
            font=("Arial", 11),
            bg=BACKGROUND_COLOR,
            fg="#64748B"
        ).pack(anchor="w", padx=30)


for item in menu_items:

    button = tk.Button(
        sidebar,
        text=item,
        font=("Arial", 11),
        bg=BUTTON_COLOR,
        fg="white",
        activebackground=ACTIVE_COLOR,
        activeforeground="white",
        relief="flat",
        anchor="w",
        padx=20,
        pady=13,
        cursor="hand2",
        command=lambda name=item: show_page(name)
    )

    button.pack(fill="x", padx=15, pady=4)

    navigation_buttons.append(button)

# ==========================================
# 14. START APPLICATION
# ==========================================

show_page("Dashboard")

root.mainloop()