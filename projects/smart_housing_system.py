import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import csv

DATABASE = "smart_housing.db"


# =========================================================
# DATABASE
# =========================================================

def connect_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def setup_database():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS houses (
            house_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            location TEXT NOT NULL,
            rent REAL NOT NULL CHECK(rent >= 0),
            bedrooms INTEGER NOT NULL CHECK(bedrooms >= 0),
            house_type TEXT NOT NULL,
            facilities TEXT,
            description TEXT,
            contact TEXT NOT NULL,
            available INTEGER NOT NULL DEFAULT 1
                CHECK(available IN (0, 1)),
            last_updated TEXT NOT NULL
        )
    """)

    # Add sample houses only when database is empty
    cursor.execute("SELECT COUNT(*) FROM houses")

    if cursor.fetchone()[0] == 0:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        sample_houses = [
            (
                "Modern 2 Bedroom House",
                "Thimphu",
                12000,
                2,
                "House",
                "Parking, Water, Kitchen, Internet",
                "Comfortable two-bedroom house suitable for a small family.",
                "17XXXXXX",
                1,
                now
            ),
            (
                "Cozy 1 Bedroom Apartment",
                "Babesa",
                8000,
                1,
                "Apartment",
                "Water, Kitchen, Balcony",
                "Affordable apartment close to shops and transport.",
                "17XXXXXX",
                1,
                now
            ),
            (
                "Spacious 3 Bedroom House",
                "Changzamtog",
                18000,
                3,
                "House",
                "Parking, Water, Kitchen, Garden",
                "Spacious rental house with a small garden and parking.",
                "17XXXXXX",
                1,
                now
            ),
            (
                "Studio Room",
                "Motithang",
                5500,
                1,
                "Room",
                "Water, Electricity, Wi-Fi",
                "Simple studio room for a single tenant.",
                "17XXXXXX",
                1,
                now
            )
        ]

        cursor.executemany("""
            INSERT INTO houses
            (
                title,
                location,
                rent,
                bedrooms,
                house_type,
                facilities,
                description,
                contact,
                available,
                last_updated
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_houses)

        conn.commit()

    conn.close()


# =========================================================
# MAIN APPLICATION
# =========================================================

class SmartHousingApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "SMART HOUSING - Rental House Finder"
        )

        self.root.geometry("1180x760")
        self.root.minsize(1050, 680)

        self.setup_style()
        self.build_ui()
        self.refresh_list()

    # -----------------------------------------------------
    # STYLE
    # -----------------------------------------------------

    def setup_style(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 25, "bold")
        )

        style.configure(
            "Treeview",
            rowheight=30,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )

        style.configure(
            "Accent.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=8
        )

    # -----------------------------------------------------
    # USER INTERFACE
    # -----------------------------------------------------

    def build_ui(self):

        # HEADER
        header = tk.Frame(
            self.root,
            bg="#173B57",
            height=105
        )

        header.pack(fill="x")

        tk.Label(
            header,
            text="SMART HOUSING",
            fg="white",
            bg="#173B57",
            font=("Segoe UI", 25, "bold")
        ).pack(
            anchor="w",
            padx=28,
            pady=(18, 0)
        )

        tk.Label(
            header,
            text="Find rental houses quickly without searching everywhere",
            fg="#D7E8F5",
            bg="#173B57",
            font=("Segoe UI", 11)
        ).pack(
            anchor="w",
            padx=30,
            pady=(2, 15)
        )

        # -------------------------------------------------
        # SEARCH AREA
        # -------------------------------------------------

        search = tk.Frame(
            self.root,
            bg="#EAF1F6",
            padx=18,
            pady=14
        )

        search.pack(fill="x")

        tk.Label(
            search,
            text="SEARCH & FILTER",
            bg="#EAF1F6",
            font=("Segoe UI", 11, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=(0, 8)
        )

        # Variables

        self.location_var = tk.StringVar()
        self.type_var = tk.StringVar(value="All")
        self.min_rent_var = tk.StringVar()
        self.max_rent_var = tk.StringVar()
        self.bed_var = tk.StringVar(value="Any")

        # LocationS
        tk.Label(
            search,
            text="Location",
            bg="#EAF1F6"
        ).grid(
            row=1,
            column=0,
            padx=5,
            sticky="w"
        )

        ttk.Entry(
            search,
            textvariable=self.location_var,
            width=20
        ).grid(
            row=2,
            column=0,
            padx=5
        )

        # House Type

        tk.Label(
            search,
            text="House Type",
            bg="#EAF1F6"
        ).grid(
            row=1,
            column=1,
            padx=5,
            sticky="w"
        )

        ttk.Combobox(
            search,
            textvariable=self.type_var,
            values=[
                "All",
                "House",
                "Apartment",
                "Room",
                "Studio"
            ],
            state="readonly",
            width=16
        ).grid(
            row=2,
            column=1,
            padx=5
        )

        # Minimum Rent

        tk.Label(
            search,
            text="Min Rent",
            bg="#EAF1F6"
        ).grid(
            row=1,
            column=2,
            padx=5,
            sticky="w"
        )

        ttk.Entry(
            search,
            textvariable=self.min_rent_var,
            width=13
        ).grid(
            row=2,
            column=2,
            padx=5
        )

        # Maximum Rent

        tk.Label(
            search,
            text="Max Rent",
            bg="#EAF1F6"
        ).grid(
            row=1,
            column=3,
            padx=5,
            sticky="w"
        )

        ttk.Entry(
            search,
            textvariable=self.max_rent_var,
            width=13
        ).grid(
            row=2,
            column=3,
            padx=5
        )

        # Bedrooms

        tk.Label(
            search,
            text="Bedrooms",
            bg="#EAF1F6"
        ).grid(
            row=1,
            column=4,
            padx=5,
            sticky="w"
        )

        ttk.Combobox(
            search,
            textvariable=self.bed_var,
            values=[
                "Any",
                "1",
                "2",
                "3",
                "4",
                "5+"
            ],
            state="readonly",
            width=10
        ).grid(
            row=2,
            column=4,
            padx=5
        )

        # Search Button

        ttk.Button(
            search,
            text="Search",
            style="Accent.TButton",
            command=self.refresh_list
        ).grid(
            row=2,
            column=5,
            padx=(12, 5)
        )

        # Reset

        ttk.Button(
            search,
            text="Reset",
            command=self.reset_search
        ).grid(
            row=2,
            column=6,
            padx=5
        )

        # Manage Listings

        ttk.Button(
            search,
            text="Manage Listings",
            command=self.open_manage
        ).grid(
            row=2,
            column=7,
            padx=5
        )

        # -------------------------------------------------
        # DASHBOARD
        # -------------------------------------------------

        stats = tk.Frame(
            self.root,
            bg="#F7F9FB",
            padx=18,
            pady=12
        )

        stats.pack(fill="x")

        self.total_var = tk.StringVar(value="0")
        self.available_var = tk.StringVar(value="0")
        self.avg_var = tk.StringVar(value="Nu. 0")
        self.location_count_var = tk.StringVar(value="0")

        cards = [
            ("TOTAL LISTINGS", self.total_var),
            ("AVAILABLE", self.available_var),
            ("AVERAGE RENT", self.avg_var),
            ("LOCATIONS", self.location_count_var)
        ]

        for col, (title, variable) in enumerate(cards):

            card = tk.Frame(
                stats,
                bg="white",
                bd=1,
                relief="solid",
                padx=18,
                pady=8
            )

            card.grid(
                row=0,
                column=col,
                sticky="ew",
                padx=6
            )

            stats.columnconfigure(
                col,
                weight=1
            )

            tk.Label(
                card,
                text=title,
                bg="white",
                fg="#667085",
                font=("Segoe UI", 9, "bold")
            ).pack(anchor="w")

            tk.Label(
                card,
                textvariable=variable,
                bg="white",
                fg="#173B57",
                font=("Segoe UI", 17, "bold")
            ).pack(anchor="w")

        # -------------------------------------------------
        # LISTINGS TABLE
        # -------------------------------------------------

        body = tk.Frame(
            self.root,
            bg="white",
            padx=18,
            pady=8
        )

        body.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            body,
            text="AVAILABLE RENTAL HOUSES",
            bg="white",
            font=("Segoe UI", 13, "bold")
        ).pack(
            anchor="w",
            pady=(3, 8)
        )

        columns = (
            "id",
            "title",
            "location",
            "rent",
            "bedrooms",
            "type",
            "facilities",
            "status"
        )

        self.tree = ttk.Treeview(
            body,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "title": "House / Room",
            "location": "Location",
            "rent": "Rent / Month",
            "bedrooms": "Bedrooms",
            "type": "Type",
            "facilities": "Facilities",
            "status": "Status"
        }

        widths = {
            "id": 50,
            "title": 210,
            "location": 120,
            "rent": 105,
            "bedrooms": 75,
            "type": 95,
            "facilities": 310,
            "status": 90
        }

        for column in columns:

            self.tree.heading(
                column,
                text=headings[column]
            )

            self.tree.column(
                column,
                width=widths[column]
            )

        self.tree.pack(
            fill="both",
            expand=True,
            side="left"
        )

        scrollbar = ttk.Scrollbar(
            body,
            orient="vertical",
            command=self.tree.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.bind(
            "<Double-1>",
            self.show_details
        )

        # -------------------------------------------------
        # BOTTOM BAR
        # -------------------------------------------------

        bottom = tk.Frame(
            self.root,
            bg="#F7F9FB",
            padx=18,
            pady=10
        )

        bottom.pack(fill="x")

        self.status_var = tk.StringVar(
            value="Ready"
        )

        tk.Label(
            bottom,
            textvariable=self.status_var,
            bg="#F7F9FB",
            fg="#475467"
        ).pack(side="left")

        ttk.Button(
            bottom,
            text="Export CSV",
            command=self.export_csv
        ).pack(side="right")

    # =====================================================
    # SEARCH
    # =====================================================

    def query_rows(self):

        sql = """
            SELECT
                house_id,
                title,
                location,
                rent,
                bedrooms,
                house_type,
                facilities,
                available,
                description,
                contact,
                last_updated
            FROM houses
            WHERE 1=1
        """

        parameters = []

        # Location

        if self.location_var.get().strip():

            sql += """
                AND LOWER(location)
                LIKE LOWER(?)
            """

            parameters.append(
                "%" +
                self.location_var.get().strip() +
                "%"
            )

        # House type

        if self.type_var.get() != "All":

            sql += """
                AND house_type = ?
            """

            parameters.append(
                self.type_var.get()
            )

        # Minimum rent

        if self.min_rent_var.get().strip():

            try:
                minimum = float(
                    self.min_rent_var.get()
                )
            except ValueError:

                raise ValueError(
                    "Minimum rent must be a number."
                )

            sql += " AND rent >= ?"

            parameters.append(
                minimum
            )

        # Maximum rent

        if self.max_rent_var.get().strip():

            try:
                maximum = float(
                    self.max_rent_var.get()
                )
            except ValueError:

                raise ValueError(
                    "Maximum rent must be a number."
                )

            sql += " AND rent <= ?"

            parameters.append(
                maximum
            )

        # Bedrooms

        if self.bed_var.get() != "Any":

            if self.bed_var.get() == "5+":

                sql += " AND bedrooms >= 5"

            else:

                sql += """
                    AND bedrooms = ?
                """

                parameters.append(
                    int(self.bed_var.get())
                )

        sql += """
            ORDER BY available DESC, rent ASC
        """

        conn = connect_db()

        rows = conn.execute(
            sql,
            parameters
        ).fetchall()

        conn.close()

        return rows

    # =====================================================
    # DISPLAY RESULTS
    # =====================================================

    def refresh_list(self):

        try:

            rows = self.query_rows()

        except ValueError as error:

            messagebox.showerror(
                "Invalid Search",
                str(error)
            )

            return

        for item in self.tree.get_children():

            self.tree.delete(item)

        for row in rows:

            (
                house_id,
                title,
                location,
                rent,
                bedrooms,
                house_type,
                facilities,
                available,
                *_
            ) = row

            self.tree.insert(
                "",
                "end",
                values=(
                    house_id,
                    title,
                    location,
                    f"Nu. {rent:,.0f}",
                    bedrooms,
                    house_type,
                    facilities or "-",
                    "Available"
                    if available
                    else "Rented"
                )
            )

        self.update_stats()

        self.status_var.set(
            f"{len(rows)} listing(s) found"
        )

    # =====================================================
    # DASHBOARD
    # =====================================================

    def update_stats(self):

        conn = connect_db()

        result = conn.execute("""
            SELECT
                COUNT(*),
                COALESCE(
                    SUM(
                        CASE
                            WHEN available = 1
                            THEN 1
                            ELSE 0
                        END
                    ),
                    0
                ),
                COALESCE(AVG(rent), 0),
                COUNT(DISTINCT location)
            FROM houses
        """).fetchone()

        conn.close()

        total, available, average, locations = result

        self.total_var.set(
            str(total)
        )

        self.available_var.set(
            str(available)
        )

        self.avg_var.set(
            f"Nu. {average:,.0f}"
        )

        self.location_count_var.set(
            str(locations)
        )

    # =====================================================
    # RESET
    # =====================================================

    def reset_search(self):

        self.location_var.set("")
        self.type_var.set("All")
        self.min_rent_var.set("")
        self.max_rent_var.set("")
        self.bed_var.set("Any")

        self.refresh_list()

    # =====================================================
    # HOUSE DETAILS
    # =====================================================

    def show_details(self, event=None):

        selected = self.tree.focus()

        if not selected:
            return

        house_id = self.tree.item(
            selected,
            "values"
        )[0]

        conn = connect_db()

        row = conn.execute("""
            SELECT
                title,
                location,
                rent,
                bedrooms,
                house_type,
                facilities,
                description,
                contact,
                available,
                last_updated
            FROM houses
            WHERE house_id = ?
        """, (house_id,)).fetchone()

        conn.close()

        if not row:
            return

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "House Details"
        )

        window.geometry(
            "560x520"
        )

        window.transient(
            self.root
        )

        tk.Label(
            window,
            text=row[0],
            font=("Segoe UI", 20, "bold"),
            fg="#173B57"
        ).pack(
            anchor="w",
            padx=25,
            pady=(22, 5)
        )

        tk.Label(
            window,
            text=f"{row[1]}  •  Nu. {row[2]:,.0f}/month",
            font=("Segoe UI", 12, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=4
        )

        info_frame = tk.Frame(
            window,
            padx=25,
            pady=15
        )

        info_frame.pack(
            fill="x"
        )

        information = [
            ("Bedrooms", str(row[3])),
            ("Type", row[4]),
            ("Facilities", row[5] or "Not specified"),
            ("Contact", row[7]),
            (
                "Status",
                "Available"
                if row[8]
                else "Rented"
            ),
            ("Last Updated", row[9])
        ]

        for index, (label, value) in enumerate(
            information
        ):

            tk.Label(
                info_frame,
                text=label + ":",
                font=("Segoe UI", 10, "bold")
            ).grid(
                row=index,
                column=0,
                sticky="nw",
                pady=5
            )

            tk.Label(
                info_frame,
                text=value,
                wraplength=390,
                justify="left"
            ).grid(
                row=index,
                column=1,
                sticky="w",
                padx=12,
                pady=5
            )

        tk.Label(
            window,
            text="Description",
            font=("Segoe UI", 11, "bold")
        ).pack(
            anchor="w",
            padx=25
        )

        tk.Message(
            window,
            text=row[6] or "No description provided.",
            width=500,
            font=("Segoe UI", 10),
            justify="left"
        ).pack(
            anchor="w",
            padx=25,
            pady=8
        )

    # =====================================================
    # MANAGE LISTINGS
    # =====================================================

    def open_manage(self):

        ManageListings(
            self.root,
            self
        )

    # =====================================================
    # CSV EXPORT
    # =====================================================

    def export_csv(self):

        filename = "rental_houses_export.csv"

        conn = connect_db()

        rows = conn.execute("""
            SELECT
                house_id,
                title,
                location,
                rent,
                bedrooms,
                house_type,
                facilities,
                description,
                contact,
                available,
                last_updated
            FROM houses
            ORDER BY house_id
        """).fetchall()

        conn.close()

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "ID",
                "Title",
                "Location",
                "Rent",
                "Bedrooms",
                "Type",
                "Facilities",
                "Description",
                "Contact",
                "Available",
                "Last Updated"
            ])

            writer.writerows(rows)

        messagebox.showinfo(
            "Export Complete",
            f"Listings exported to {filename}"
        )


# =========================================================
# MANAGE LISTINGS WINDOW
# =========================================================

class ManageListings:

    def __init__(self, parent, app):

        self.app = app

        self.window = tk.Toplevel(
            parent
        )

        self.window.title(
            "Manage Rental Listings"
        )

        self.window.geometry(
            "1040x650"
        )

        self.window.transient(
            parent
        )

        # Variables

        self.variables = {}

        fields = [
            "title",
            "location",
            "rent",
            "bedrooms",
            "type",
            "facilities",
            "contact",
            "description"
        ]

        for field in fields:

            self.variables[field] = (
                tk.StringVar()
            )

        self.available_var = tk.IntVar(
            value=1
        )

        # -------------------------------------------------
        # FORM
        # -------------------------------------------------

        form = tk.Frame(
            self.window,
            bg="#F7F9FB",
            padx=18,
            pady=15
        )

        form.pack(
            fill="x"
        )

        fields_info = [
            ("House / Room Title", "title"),
            ("Location", "location"),
            ("Rent / Month", "rent"),
            ("Bedrooms", "bedrooms"),
            ("House Type", "type"),
            ("Facilities", "facilities"),
            ("Contact", "contact"),
            ("Description", "description")
        ]

        for index, (label, key) in enumerate(
            fields_info
        ):

            row = (index // 2) * 2
            column = index % 2

            tk.Label(
                form,
                text=label,
                bg="#F7F9FB"
            ).grid(
                row=row,
                column=column,
                sticky="w",
                padx=7
            )

            if key == "type":

                widget = ttk.Combobox(
                    form,
                    textvariable=self.variables[key],
                    values=[
                        "House",
                        "Apartment",
                        "Room",
                        "Studio"
                    ],
                    state="readonly",
                    width=35
                )

            else:

                widget = ttk.Entry(
                    form,
                    textvariable=self.variables[key],
                    width=38
                )

            widget.grid(
                row=row + 1,
                column=column,
                padx=7,
                pady=(0, 8),
                sticky="w"
            )

        # Available checkbox

        tk.Checkbutton(
            form,
            text="Available for rent",
            variable=self.available_var,
            bg="#F7F9FB"
        ).grid(
            row=8,
            column=0,
            sticky="w",
            padx=7
        )

        # Buttons

        buttons = tk.Frame(
            form,
            bg="#F7F9FB"
        )

        buttons.grid(
            row=8,
            column=1,
            sticky="e"
        )

        ttk.Button(
            buttons,
            text="Add Listing",
            command=self.add
        ).pack(
            side="left",
            padx=3
        )

        ttk.Button(
            buttons,
            text="Update",
            command=self.update
        ).pack(
            side="left",
            padx=3
        )

        ttk.Button(
            buttons,
            text="Delete",
            command=self.delete
        ).pack(
            side="left",
            padx=3
        )

        ttk.Button(
            buttons,
            text="Clear",
            command=self.clear
        ).pack(
            side="left",
            padx=3
        )

        # -------------------------------------------------
        # MANAGEMENT TABLE
        # -------------------------------------------------

        body = tk.Frame(
            self.window,
            padx=18,
            pady=10
        )

        body.pack(
            fill="both",
            expand=True
        )

        columns = (
            "id",
            "title",
            "location",
            "rent",
            "bedrooms",
            "type",
            "status"
        )

        self.tree = ttk.Treeview(
            body,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "title": "Title",
            "location": "Location",
            "rent": "Rent",
            "bedrooms": "Beds",
            "type": "Type",
            "status": "Status"
        }

        widths = {
            "id": 50,
            "title": 240,
            "location": 130,
            "rent": 100,
            "bedrooms": 70,
            "type": 110,
            "status": 100
        }

        for column in columns:

            self.tree.heading(
                column,
                text=headings[column]
            )

            self.tree.column(
                column,
                width=widths[column]
            )

        self.tree.pack(
            fill="both",
            expand=True
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select
        )

        self.refresh()

    # =====================================================
    # REFRESH MANAGEMENT TABLE
    # =====================================================

    def refresh(self):

        for item in self.tree.get_children():

            self.tree.delete(item)

        conn = connect_db()

        rows = conn.execute("""
            SELECT
                house_id,
                title,
                location,
                rent,
                bedrooms,
                house_type,
                available
            FROM houses
            ORDER BY house_id
        """).fetchall()

        conn.close()

        for row in rows:

            self.tree.insert(
                "",
                "end",
                values=(
                    row[0],
                    row[1],
                    row[2],
                    f"Nu. {row[3]:,.0f}",
                    row[4],
                    row[5],
                    "Available"
                    if row[6]
                    else "Rented"
                )
            )

    # =====================================================
    # GET FORM DATA
    # =====================================================

    def get_form_data(self):

        title = self.variables[
            "title"
        ].get().strip()

        location = self.variables[
            "location"
        ].get().strip()

        contact = self.variables[
            "contact"
        ].get().strip()

        if not title:

            raise ValueError(
                "House/room title is required."
            )

        if not location:

            raise ValueError(
                "Location is required."
            )

        if not contact:

            raise ValueError(
                "Contact is required."
            )

        try:

            rent = float(
                self.variables[
                    "rent"
                ].get()
            )

            bedrooms = int(
                self.variables[
                    "bedrooms"
                ].get()
            )

        except ValueError:

            raise ValueError(
                "Rent must be a number and bedrooms must be a whole number."
            )

        if rent < 0:

            raise ValueError(
                "Rent cannot be negative."
            )

        if bedrooms < 0:

            raise ValueError(
                "Bedrooms cannot be negative."
            )

        house_type = self.variables[
            "type"
        ].get().strip()

        if not house_type:

            house_type = "House"

        return (
            title,
            location,
            rent,
            bedrooms,
            house_type,
            self.variables[
                "facilities"
            ].get().strip(),
            self.variables[
                "description"
            ].get().strip(),
            contact,
            self.available_var.get(),
            datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            )
        )

    # =====================================================
    # ADD
    # =====================================================

    def add(self):

        try:

            data = self.get_form_data()

        except ValueError as error:

            messagebox.showerror(
                "Validation",
                str(error),
                parent=self.window
            )

            return

        conn = connect_db()

        conn.execute("""
            INSERT INTO houses
            (
                title,
                location,
                rent,
                bedrooms,
                house_type,
                facilities,
                description,
                contact,
                available,
                last_updated
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data)

        conn.commit()
        conn.close()

        self.clear()
        self.refresh()
        self.app.refresh_list()

        messagebox.showinfo(
            "Success",
            "Rental house added successfully.",
            parent=self.window
        )

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self):

        selected = self.tree.focus()

        if not selected:

            messagebox.showwarning(
                "Select Listing",
                "Select a listing first.",
                parent=self.window
            )

            return

        try:

            data = self.get_form_data()

        except ValueError as error:

            messagebox.showerror(
                "Validation",
                str(error),
                parent=self.window
            )

            return

        house_id = self.tree.item(
            selected,
            "values"
        )[0]

        conn = connect_db()

        conn.execute("""
            UPDATE houses
            SET
                title = ?,
                location = ?,
                rent = ?,
                bedrooms = ?,
                house_type = ?,
                facilities = ?,
                description = ?,
                contact = ?,
                available = ?,
                last_updated = ?
            WHERE house_id = ?
        """, (*data, house_id))

        conn.commit()
        conn.close()

        self.clear()
        self.refresh()
        self.app.refresh_list()

        messagebox.showinfo(
            "Success",
            "Rental listing updated successfully.",
            parent=self.window
        )

    # =====================================================
    # DELETE
    # =====================================================

    def delete(self):

        selected = self.tree.focus()

        if not selected:

            messagebox.showwarning(
                "Select Listing",
                "Select a listing first.",
                parent=self.window
            )

            return

        house_id = self.tree.item(
            selected,
            "values"
        )[0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this rental listing?",
            parent=self.window
        )

        if not confirm:
            return

        conn = connect_db()

        conn.execute(
            "DELETE FROM houses WHERE house_id = ?",
            (house_id,)
        )

        conn.commit()
        conn.close()

        self.clear()
        self.refresh()
        self.app.refresh_list()

        messagebox.showinfo(
            "Deleted",
            "Rental listing deleted successfully.",
            parent=self.window
        )

    # =====================================================
    # SELECT LISTING
    # =====================================================

    def select(self, event=None):

        selected = self.tree.focus()

        if not selected:
            return

        house_id = self.tree.item(
            selected,
            "values"
        )[0]

        conn = connect_db()

        row = conn.execute("""
            SELECT
                title,
                location,
                rent,
                bedrooms,
                house_type,
                facilities,
                description,
                contact,
                available
            FROM houses
            WHERE house_id = ?
        """, (house_id,)).fetchone()

        conn.close()

        if row:

            keys = [
                "title",
                "location",
                "rent",
                "bedrooms",
                "type",
                "facilities",
                "description",
                "contact"
            ]

            for key, value in zip(
                keys,
                row[:8]
            ):

                self.variables[
                    key
                ].set(value)

            self.available_var.set(
                row[8]
            )

    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self):

        for variable in self.variables.values():

            variable.set("")

        self.available_var.set(1)


# =========================================================
# PROGRAM START
# =========================================================

if __name__ == "__main__":

    setup_database()

    root = tk.Tk()

    application = SmartHousingApp(
        root
    )

    root.mainloop()