import csv
import matplotlib.pyplot as plt
from datetime import datetime
import warnings

warnings.filterwarnings("ignore", message="Blended transforms not yet supported")

def filter_similar(roles, keyword="data"):
    filtered = []
    found = False
    for role, salary in roles:
        if keyword in role.lower():
            if not found:
                filtered.append((role, salary))
                found = True
        else:
            filtered.append((role, salary))
    return filtered

job_file = "./JobSalary.csv"
job_role_data = {}

# Read job salary data
with open(job_file, newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row["Country"].strip().upper() == "USA":
            try:
                salary = float(row["Salary"])
            except:
                continue
            role = row["Job Title"].strip()
            if role not in job_role_data:
                job_role_data[role] = {"total": 0, "count": 0}
            job_role_data[role]["total"] += salary
            job_role_data[role]["count"] += 1

# Calculate average monthly salary for each role
avg_monthly_salary_by_role = {}
for role, data in job_role_data.items():
    if data["count"] > 0:
        avg_monthly_salary_by_role[role] = (data["total"] / data["count"]) / 12

# Sort roles by salary
sorted_roles = sorted(avg_monthly_salary_by_role.items(), key=lambda x: x[1])

# Select bottom 3, middle 3, and top 3 salaries
num_roles = len(sorted_roles)
if num_roles < 9:
    selected_roles = sorted_roles
else:
    bottom_three = sorted_roles[1:4]
    middle_three = sorted_roles[num_roles // 3 - 1:num_roles // 2 + 2]
    selected_roles = bottom_three + middle_three

# Ensure at least one data-related role is included
final_selected_roles = []
data_included = False
for role, salary in selected_roles:
    if "data" in role.lower():
        if not data_included:
            final_selected_roles.append((role, salary))
            data_included = True
    else:
        final_selected_roles.append((role, salary))

# Read rental data
housing_file = "./Rental.csv"
dates = []
rental_costs = []

with open(housing_file, newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row["RegionName"].strip().strip('"') == "United States":
            for key in row:
                if key not in ["RegionID", "SizeRank", "RegionName", "RegionType", "StateName"]:
                    try:
                        date_obj = datetime.strptime(key, "%Y-%m-%d")
                        dates.append(date_obj)
                        rental_costs.append(float(row[key]))
                    except:
                        continue
            break

# Sort rental data by date
dates, rental_costs = zip(*sorted(zip(dates, rental_costs)))

# Plot rental cost vs. job salaries
plt.style.use("classic")
plt.figure(figsize=(14, 8))
plt.plot(dates, rental_costs, marker="o", linestyle="-", linewidth=2, color="Purple", label="Monthly Rent (USA)")

colors = plt.cm.tab20.colors
color_index = 0

# Plot horizontal lines for each selected job role salary
for role, avg_monthly_salary in final_selected_roles:
    plt.axhline(y=avg_monthly_salary, color=colors[color_index % len(colors)], linestyle="--", linewidth=2,
                label=f"{role}: ${avg_monthly_salary:,.2f}")
    color_index += 1

# Format plot
plt.xlabel("Date", fontsize=14)
plt.ylabel("Cost in USD", fontsize=14)
plt.title("U.S. Housing Rental Cost vs. Selected Job Role Salaries (US Only)", fontsize=16, fontweight="bold")
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=12, ncol=1, frameon=True)
plt.tight_layout()

# Save and show the plot
plt.savefig("rental_vs_salary_roles_US_only.png", dpi=300)
plt.show()
