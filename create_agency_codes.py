import pandas as pd


# Sample agency mapping data
agency_data = {
    "Agency": [
        "San Francisco",
        "San Francisco Police Department", 
        "San Francisco Fire Department",
        "San Francisco Sheriff's Department",
        "San Francisco Public Works",
        "San Francisco Municipal Transportation Agency",
        "San Francisco Recreation and Parks",
        "San Francisco Public Health",
        "San Francisco Public Utilities Commission",
        "San Francisco City Attorney"
    ],
    "Agency_Code": [
        "SF-001",
        "SF-PD",
        "SF-FD",
        "SF-SD",
        "SF-PW",
        "SF-MTA",
        "SF-RP",
        "SF-PH",
        "SF-PUC",
        "SF-CA"
    ],
    "Department_Type": [
        "General",
        "Public Safety",
        "Public Safety",
        "Public Safety",
        "Infrastructure",
        "Transportation",
        "Recreation",
        "Health",
        "Utilities",
        "Legal"
    ]
}

# Create DataFrame
df = pd.DataFrame(agency_data)

# Save to CSV
df.to_csv("agency_codes.csv", index=False)

print("agency_codes.csv created successfully!")
print(f"  Total agencies: {len(df)}")
print("\nPreview:")
print(df.to_string(index=False))