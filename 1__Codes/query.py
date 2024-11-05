import subprocess
import csv

# Set the query
query = "Among patients with septic shock and relative adrenal insufficiency, do corticosteroids reduce 28-day mortality?"

# Run the graphrag.query command to receive the response
result = subprocess.run(
    ["python", "-m", "graphrag.query", "--root", ".", "--method", "local", query],
    capture_output=True,
    text=True
)

# Remove unnecessary logs from the response content
response = result.stdout.split("SUCCESS: Local Search Response:\n")[-1].strip()

# Save to CSV file
with open("response_output.csv", mode="w", newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Query", "Response"])
    writer.writerow([query, response])

print("Response has been saved to response_output.csv in the correct format.")