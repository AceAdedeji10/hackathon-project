import pandas as pd

# To load the dataset
df = pd.read_csv("C:/Users/HP SPECTER X360/Downloads/DATASET.csv")

# To explore the data
print("          Data Exploration ")
print(df.head())
print(df.info())
print(df.describe())

# To check for duplicates
print("\n       Checking for Duplicates ")
print("Number of duplicate rows:", df.duplicated().sum())

# To Handle the missing Values
print("\n       Missing Value Handling ")
# shop_id: Missing values were replaced with -1 as a placeholder
# final_order_status: Missing values were replaced with Null
print("Missing values in final_order_status:", df['final_order_status'].isnull().sum())

# To verify data integrity
print("\n       Unique Values in Key Columns ")
print("Unique values in event_type:", df['event_type'].unique())
print("Unique values in platform:", df['platform'].unique())
print("Unique values in variation:", df['variation'].unique())

# To analyze user distribution
print("\n       User Distribution Analysis ")
control_users = df[df['variation'] == 1]['user_id'].nunique()
test_users = df[df['variation'] == 2]['user_id'].nunique()
print("Control Group Users:", control_users)
print("Test Group Users:", test_users)
total_users = control_users + test_users
print("Percentage of users in Control Group:", (control_users / total_users) * 100)
print("Percentage of users in Test Group:", (test_users / total_users) * 100)

# To define successful orders ('order_paid' or 'order_finished')
successful_orders = df[df["final_order_status"] == "successful"]

# To count users who entered a shop (potential customers)
shop_entries = df[df["event_type"] == "entry_to_shop"]

# To calculate order rates for each variation
order_rate_control = successful_orders[successful_orders["variation"] == 1]["user_id"].nunique() / \
                     shop_entries[shop_entries["variation"] == 1]["user_id"].nunique()

order_rate_test = successful_orders[successful_orders["variation"] == 2]["user_id"].nunique() / \
                  shop_entries[shop_entries["variation"] == 2]["user_id"].nunique()

# To display order rates
print("Control Group Order Rate:", order_rate_control)
print("Test Group Order Rate:", order_rate_test)

# To calculate required values for statistical testing
successes_control = successful_orders[successful_orders["variation"] == 1]["user_id"].nunique()
successes_test = successful_orders[successful_orders["variation"] == 2]["user_id"].nunique()

total_control = shop_entries[shop_entries["variation"] == 1]["user_id"].nunique()
total_test = shop_entries[shop_entries["variation"] == 2]["user_id"].nunique()

# To print values for reference
print(f"Control Group: {successes_control}/{total_control} orders")
print(f"Test Group: {successes_test}/{total_test} orders")

from statsmodels.stats.proportion import proportions_ztest

# To define counts and sample sizes
counts = [successes_test, successes_control]  # Number of successful orders
nobs = [total_test, total_control]  # Total number of users who entered a shop

# To perform Z-test
z_stat, p_value = proportions_ztest(count=counts, nobs=nobs, alternative='larger')

# To print results
print(f"Z-Statistic: {z_stat:.3f}")
print(f"P-Value: {p_value:.5f}")

# To perform platform analysis and print results
print("\n       Platform Analysis ")
platform_order_rates = (
    successful_orders.groupby('platform')['user_id'].nunique() /
    shop_entries.groupby('platform')['user_id'].nunique()
)
print("Order Rates by Platform:")
print(platform_order_rates)

import matplotlib.pyplot as plt

# Plot order rates by platform
plt.figure(figsize=(10, 6))
platform_order_rates.plot(kind='bar', color=['skyblue', 'lightgreen', 'salmon'])
plt.title('Order Rates by Platform')
plt.xlabel('Platform')
plt.ylabel('Order Rate')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Data for pie chart
labels = ['Control Group', 'Test Group']
sizes = [control_users, test_users]
colors = ['lightblue', 'lightcoral']
explode = (0.1, 0)  # Highlight the first slice (Control Group)

# Plot pie chart
plt.figure(figsize=(6, 6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.title('User Distribution in Control and Test Groups')
plt.show()

# Data for grouped bar plot
variations = ['Control Group', 'Test Group']
order_rates = [order_rate_control, order_rate_test]

# Plot grouped bar plot
plt.figure(figsize=(8, 6))
plt.bar(variations, order_rates, color=['skyblue', 'lightgreen'])
plt.title('Order Rates by Variation')
plt.xlabel('Variation')
plt.ylabel('Order Rate')
plt.ylim(0, 1)  # Set y-axis limit to 1 for better visualization
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

