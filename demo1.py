# Becoming a Data Engineer
# Step 1: Handling Large Data Sets In Python

import pandas as pd
# Read the file moma.csv into a dataframe named moma.
moma = pd.read_csv("moma-exhibitions/MoMAExhibitions1929to1989.csv")

# The DataFrame.info() method returns an estimate for the amount of memory a dataframe consumes.
# Display the memory usage of the moma dataframe.
print(moma.info())

print("--" * 60)

# Retrieve the underlying BlockManager instance.
print(moma._data)

print("--" * 60)

# Recreate the estimate of the memory footprint by multiplying the number of values
# in the moma dataframe by 8. Assign this number to total_bytes.
# Use the DataFrame.size attribute to return the number of values in a dataframe.
total_bytes = moma.size * 8

# Convert total_bytes from bytes to megabytes, and assign the result to total_megabytes.
total_megabytes = total_bytes / 1048576

print(total_bytes)
print(total_megabytes)

print("--" * 60)

# Select just the object columns from the moma dataframe
# and assign the resulting dataframe to obj_cols.
obj_cols = moma.select_dtypes(include=['object'])

# Use the DataFrame.memory_usage() method and set the deep parameter to True
# to return the memory footprint of each column in obj_cols.
# Assign the resulting series to obj_cols_mem.
obj_cols_mem = obj_cols.memory_usage(deep=True)
print(obj_cols_mem)

# Use the Series.sum() method to sum the values in obj_cols_mem,
# convert the result to megabytes, and assign the result to obj_cols_sum.
obj_cols_sum = obj_cols_mem.sum()/1048576
print(obj_cols_sum)

print("--" * 60)

# Find the smallest int subtype that can accommodate the values in the ExhibitionSortOrder column.
# Use the Series.astype() function to set the type, and assign it back to the moma dataframe.

col_max = moma['ExhibitionSortOrder'].max()
col_min = moma['ExhibitionSortOrder'].min()

if col_max <  np.iinfo("int8").max and col_min > np.iinfo("int8").min:
    moma['ExhibitionSortOrder'] = moma['ExhibitionSortOrder'].astype("int8")
elif col_max <  np.iinfo("int16").max and col_min > np.iinfo("int16").min:
    moma['ExhibitionSortOrder'] = moma['ExhibitionSortOrder'].astype("int16")
elif col_max <  np.iinfo("int32").max and col_min > np.iinfo("int32").min:
    moma['ExhibitionSortOrder'] = moma['ExhibitionSortOrder'].astype("int32")
elif col_max <  np.iinfo("int64").max and col_min > np.iinfo("int64").min:
    moma['ExhibitionSortOrder'] = moma['ExhibitionSortOrder'].astype("int64")

print(moma['ExhibitionSortOrder'].dtype)
print(moma['ExhibitionSortOrder'].memory_usage(deep=True))

print("--" * 60)

# Convert the remaining float columns to the most space efficient float subtype.
# Select the float columns again, and display their dtypes using the DataFrame.dtypes attribute.

moma['ExhibitionSortOrder'] = moma['ExhibitionSortOrder'].astype("int16")

float_cols = moma.select_dtypes(include=['float'])

print(float_cols.dtypes)

for col in float_cols.columns:
    moma[col] = pd.to_numeric(moma[col], downcast='float')

print(moma.select_dtypes(include=['float']).dtypes)

print("--" * 60)

# Convert the ExhibitionBeginDate and ExhibitionEndDate columns to the datetime type,
# and assign the results back to the moma dataframe.
# Display the memory usage for both of these columns using the DataFrame.memory_usage() method.

moma["ExhibitionBeginDate"] = pd.to_datetime(moma["ExhibitionBeginDate"])
moma["ExhibitionEndDate"] = pd.to_datetime(moma["ExhibitionEndDate"])

print(moma[["ExhibitionBeginDate", "ExhibitionEndDate"]].memory_usage(deep=True))

print("--" * 60)

# Convert all object columns where less than half of
# the column's values are unique to the category dtype.
# Return the deep memory footprint using the DataFrame.info() method.

obj_cols = moma.select_dtypes(include=['object'])

for col in obj_cols.columns:
    num_unique_values = len(moma[col].unique())
    num_total_values = len(moma[col])
    if num_unique_values / num_total_values < 0.5:
        moma[col] = moma[col].astype('category')
        
print(moma.info(memory_usage='deep'))

print("--" * 60)

# Read "moma.csv" into a dataframe named moma:
# Set the ExhibitionBeginDate and ExhibitionEndDate columns to the datetime type.
# Include only these columns:
  # ExhibitionID
  # ExhibitionNumber
  # ExhibitionBeginDate
  # ExhibitionEndDate
  # ExhibitionSortOrder
  # ExhibitionRole
  # ConstituentType
  # DisplayName
  # Institution
  # Nationality
  # Gender
# Display the deep memory footprint in megabytes.

keep_cols = ['ExhibitionID', 'ExhibitionNumber', 'ExhibitionBeginDate',
             'ExhibitionEndDate', 'ExhibitionSortOrder', 'ExhibitionRole',
             'ConstituentType', 'DisplayName', 'Institution', 'Nationality', 'Gender']

moma = pd.read_csv("moma-exhibitions/MoMAExhibitions1929to1989.csv",
                   parse_dates=["ExhibitionBeginDate", "ExhibitionEndDate"],
                   usecols=keep_cols)

print(moma.memory_usage(deep=True).sum() / (1024*1024))
