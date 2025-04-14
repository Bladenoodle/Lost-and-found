from datetime import date, timedelta

# Set the start and end date
start_date=date(2023, 1, 1)
end_date=date.today()

# Read the original content of init.sql
with open("init.sql", "r") as file:
    lines=file.readlines()

# Remove old Time inserts (optional: keeps other inserts like Location)
filtered_lines=[line for line in lines if not ("INSERT INTO classes" in line and "Time" in line)]

# Add a delete statement to clear old Time values
filtered_lines.append("\nDELETE FROM classes WHERE class_name='Time';\n")

# Generate new inserts for each date
current_date=end_date
while current_date >= start_date:
    filtered_lines.append(
        f"INSERT INTO classes (class_name, value) VALUES ('Time', '{current_date}');\n"
    )
    current_date -= timedelta(days=1)

# Write back to init.sql
with open("init.sql", "w") as file:
    file.writelines(filtered_lines)
