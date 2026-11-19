# The Summit Event Planner - Tkinter version
# Same logic as the console program: enter a budget and eight costs,
# then compare the total cost against the budget.

import tkinter as tk
from tkinter import ttk, messagebox

CURRENCY = "£"  # change to "$" or "" if you prefer

# (label shown on screen, internal key) - order matches the original program
COST_FIELDS = [
    ("Venue cost", "venue"),
    ("Staff cost", "staff"),
    ("Catering cost", "catering"),
    ("Entertainment cost", "entertainment"),
    ("Production cost", "production"),
    ("Logistics cost", "logistics"),
    ("Insurance cost", "insurance"),
    ("Other costs", "other"),
]

GREEN = "#1b7a3d"
RED = "#b3261e"
BLUE = "#1f4e8c"


def money(value):
    return f"{CURRENCY}{value:,.2f}"


class EventPlannerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("The Summit Event Planner")
        self.minsize(460, 620)
        self.resizable(False, False)

        style = ttk.Style(self)
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("Sub.TLabel", font=("Segoe UI", 10))
        style.configure("Total.TLabel", font=("Segoe UI", 11, "bold"))

        self.container = ttk.Frame(self, padding=20)
        self.container.pack(fill="both", expand=True)

        self.show_welcome()

    # ---------- helpers ----------
    def clear(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # ---------- welcome screen (replaces "Are you ready to start?") ----------
    def show_welcome(self):
        self.clear()
        ttk.Label(self.container, text="Event Planner", style="Title.TLabel").pack(pady=(40, 10))
        ttk.Label(
            self.container,
            text="Welcome to the event planning application.\n"
                 "We will help you calculate your costs\nin regard to your budget.",
            style="Sub.TLabel", justify="center",
        ).pack(pady=10)
        ttk.Label(self.container, text="Are you ready to start the calculation?",
                  style="Sub.TLabel").pack(pady=(30, 10))

        buttons = ttk.Frame(self.container)
        buttons.pack()
        ttk.Button(buttons, text="Yes, let's start", command=self.show_planner).grid(row=0, column=0, padx=5)
        ttk.Button(buttons, text="No", command=self.say_goodbye).grid(row=0, column=1, padx=5)

    def say_goodbye(self):
        messagebox.showinfo("Goodbye", "You can always come back.")
        self.destroy()

    # ---------- main planner screen ----------
    def show_planner(self):
        self.clear()
        ttk.Label(self.container, text="Event Planner", style="Title.TLabel").pack(anchor="w")
        ttk.Label(self.container,
                  text="Enter your costs. If you don't have a specific cost, enter 0 (or leave it blank).",
                  style="Sub.TLabel", wraplength=410).pack(anchor="w", pady=(2, 12))

        form = ttk.Frame(self.container)
        form.pack(fill="x")

        self.vars = {}

        # Budget row
        ttk.Label(form, text="Your budget").grid(row=0, column=0, sticky="w", pady=4)
        self.vars["budget"] = tk.StringVar()
        budget_entry = ttk.Entry(form, textvariable=self.vars["budget"], width=18)
        budget_entry.grid(row=0, column=1, sticky="e", pady=4, padx=(10, 0))
        form.columnconfigure(0, weight=1)

        ttk.Separator(form).grid(row=1, column=0, columnspan=2, sticky="ew", pady=8)

        # Cost rows
        self.entries = [budget_entry]
        for i, (label, key) in enumerate(COST_FIELDS, start=2):
            ttk.Label(form, text=label).grid(row=i, column=0, sticky="w", pady=4)
            self.vars[key] = tk.StringVar()
            self.vars[key].trace_add("write", self.update_live_total)
            entry = ttk.Entry(form, textvariable=self.vars[key], width=18)
            entry.grid(row=i, column=1, sticky="e", pady=4, padx=(10, 0))
            self.entries.append(entry)

        budget_entry.focus()

        # Live running total (updates while typing)
        self.live_total = tk.StringVar(value=f"Running total: {money(0)}")
        ttk.Label(self.container, textvariable=self.live_total, style="Total.TLabel").pack(anchor="w", pady=(12, 6))

        # Buttons
        buttons = ttk.Frame(self.container)
        buttons.pack(fill="x", pady=6)
        ttk.Button(buttons, text="Calculate", command=self.calculate).pack(side="left")
        ttk.Button(buttons, text="Clear", command=self.clear_fields).pack(side="left", padx=6)
        ttk.Button(buttons, text="Quit", command=self.destroy).pack(side="right")

        # Result area
        self.result_title = tk.Label(self.container, text="", font=("Segoe UI", 12, "bold"), anchor="w")
        self.result_title.pack(fill="x", pady=(10, 0))
        self.result_detail = tk.Label(self.container, text="", font=("Segoe UI", 10),
                                      anchor="w", justify="left")
        self.result_detail.pack(fill="x")

        self.bind("<Return>", lambda event: self.calculate())

    # ---------- reading and validating numbers ----------
    @staticmethod
    def parse_amount(text):
        """Blank counts as 0. Raises ValueError for text or negative numbers."""
        text = text.strip().replace(",", "").lstrip(CURRENCY) if text.strip() else "0"
        value = float(text)
        if value < 0:
            raise ValueError("negative")
        return value

    def update_live_total(self, *args):
        total = 0.0
        for _, key in COST_FIELDS:
            try:
                total += self.parse_amount(self.vars[key].get())
            except ValueError:
                pass  # ignore half-typed or invalid values while typing
        self.live_total.set(f"Running total: {money(total)}")

    def calculate(self):
        # Validate budget (required) and every cost field
        invalid = []
        values = {}

        budget_text = self.vars["budget"].get().strip()
        if not budget_text:
            invalid.append("Your budget (required)")
        else:
            try:
                values["budget"] = self.parse_amount(budget_text)
            except ValueError:
                invalid.append("Your budget")

        for label, key in COST_FIELDS:
            try:
                values[key] = self.parse_amount(self.vars[key].get())
            except ValueError:
                invalid.append(label)

        if invalid:
            messagebox.showerror(
                "Invalid input",
                "Please enter a number of 0 or more in:\n\n• " + "\n• ".join(invalid),
            )
            return

        # Calculations (same as the original)
        budget = values["budget"]
        total_cost = sum(values[key] for _, key in COST_FIELDS)

        if total_cost == budget:
            title, colour = "Exactly on budget", BLUE
            detail = f"Your cost is exactly what your budget is.\nTotal cost: {money(total_cost)}"
        elif budget > total_cost:
            leftover = budget - total_cost
            title, colour = "Under budget", GREEN
            detail = (f"Your cost is under the budget.\nTotal cost: {money(total_cost)}\n"
                      f"You have {money(leftover)} remaining.")
        else:
            over = total_cost - budget
            title, colour = "Over budget", RED
            detail = (f"Your cost is over the budget.\nTotal cost: {money(total_cost)}\n"
                      f"You went over by {money(over)}.")

        self.result_title.config(text=title, fg=colour)
        self.result_detail.config(text=detail)

    def clear_fields(self):
        for var in self.vars.values():
            var.set("")
        self.result_title.config(text="")
        self.result_detail.config(text="")
        self.entries[0].focus()


if __name__ == "__main__":
    EventPlannerApp().mainloop()
