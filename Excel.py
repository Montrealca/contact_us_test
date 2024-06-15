
import pandas as pd

# Define the test data
data = {
    "fullname": ["John Doe", "Jane Smith", "Emily Davis"],
    "email": ["john@example.com", "jane@example.com", "emily@example.com"],
    "phone": ["1234567890", "0987654321", "1231231234"],
    "message": ["Hello", "Testing", "This is a test message"],
    "expected_result": ["Thank you", "Thank you", "Validation error;Invalid phone number"]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Define the file path
file_path = "C:/Users/Manikandan A/Documents/Test1.xlsx"

# Write the DataFrame to an Excel file
df.to_excel(file_path, index=False)

# Provide the file path for download
file_path
