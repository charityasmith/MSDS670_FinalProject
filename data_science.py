"""""
data_science.py

Python 3 
This script generates data visualizations for data science salaries in 2023

Author: Charity Smith
""" 

#%%
# import libraries

import pandas as pd
import matplotlib.pyplot as plt
import pycountry
import numpy as np
import os
import seaborn as sns
import plotly.express as px
import pycountry

dpi = 300

# file path
project_dir = r''
data_dir = project_dir + r'data/'
output_dir = project_dir + r'output/'

#%%

# Data Source: Data Science Salaries 2023
# https://www.kaggle.com/datasets/arnabchaki/data-science-salaries-2023/data
# Load the dataset
data_filename = "ds_salaries.csv"
df = pd.read_csv(data_dir + data_filename)


# Plot 1: Bar Chart - Top 10 Company Locations by Salary

# Group by company location and calculate the average salary
location_salary = df.groupby("company_location")["salary_in_usd"].mean().sort_values(ascending=False)

# Select the top 10 highest-paying locations
top_10_locations = location_salary.head(10)

# Convert ISO country codes to full country names
def get_country_name(iso_code):
    try:
        country_name = pycountry.countries.get(alpha_2=iso_code).name
        # Manually rename long country names
        if country_name == "Russian Federation":
            return "Russia"
        elif country_name == "Bosnia and Herzegovina":
            return "Bosnia"
        return country_name
    except AttributeError:
        return iso_code  # Keep original if no match found

top_10_locations.index = [get_country_name(code) for code in top_10_locations.index]

# Create the figure
fig, ax = plt.subplots(figsize=(11, 6))

# Horizontal bar chart
ax.barh(top_10_locations.index[::-1], top_10_locations.values[::-1], color="#2E8B57")  

# Title and Axes Formatting
ax.set_title("Highest Paying Countries for Data Science Jobs", fontsize=16, fontweight="bold", pad=15)
ax.set_xlabel("Average Salary (USD)", fontsize=12, fontweight="bold", labelpad=12)
ax.set_ylabel("Country", fontsize=12, fontweight="bold", labelpad=12)

# Format x-axis to use commas for large numbers
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))

# Remove gridlines
ax.grid(False)

# Save the figure
os.makedirs(output_dir, exist_ok=True)
plot_filename = os.path.join(output_dir, "top_10_company_locations_by_salary.png")
fig.savefig(plot_filename, dpi=dpi, bbox_inches="tight")



# Plot 2: Histogram - Salary Distribution (Detect Skewness)

# Extract salary column
salaries = df["salary_in_usd"]

# Compute median salary
median_salary = salaries.median()

# Create figure
plt.figure(figsize=(10, 6))
n, bins, patches = plt.hist(salaries, bins=30, color="seagreen", edgecolor="black", alpha=0.80)

# Add vertical dashed line for median
plt.axvline(median_salary, color="royalblue", linestyle="dashed", linewidth=2.5, label=f"Median: ${median_salary:,.0f}")

# Find max frequency (height of the tallest bar)
max_freq = max(n)

# Title and Axes Formatting
plt.title("Data Science Salary Distribution", fontsize=16, fontweight="bold")
plt.xlim(left=0)
plt.xlabel("Salary (USD)", fontsize=12, fontweight="bold", labelpad=12)
plt.ylabel("Frequency", fontsize=12, fontweight="bold", labelpad=12)

# Median legend
plt.legend(loc="upper right", bbox_to_anchor=(0.92, 0.85), fontsize=12, frameon=False)

# Format x-axis with commas
plt.gca().xaxis.set_major_formatter(plt.matplotlib.ticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))

# Remove gridlines
plt.grid(False)

# Save the plot
os.makedirs(output_dir, exist_ok=True)
plot_filename = os.path.join(output_dir, "salary_distribution.png")
plt.savefig(plot_filename, dpi=300, bbox_inches="tight")



# Plot 3: Vertical Bar Chart - Top 10 Job Titles by Frequency

# Count job titles and get top 10
job_counts = df["job_title"].value_counts().nlargest(10)

# Rename long job titles for better display
job_counts = job_counts.rename(index={
    "Machine Learning Engineer": "ML Engineer",
    "Data Science Manager": "Manager"
    })

# Create figure
plt.figure(figsize=(12, 7)) 

# Plot bar chart
plt.bar(job_counts.index, job_counts.values, color="royalblue", edgecolor="black", alpha=0.75, width=0.85)

# Title and Axes Formatting
plt.title("Most Common Data Science Jobs", fontsize=16, fontweight="bold", pad=20)
plt.xlabel("Job Title", fontsize=11, fontweight="bold", labelpad=12)
plt.xticks(rotation=22, ha="right", fontsize=12) # Improve readability of job titles
plt.ylabel("Count", fontsize=12, fontweight="bold", labelpad=12)

# Increase bottom padding to avoid labels being cut off
plt.subplots_adjust(bottom=0.35)

# Format y-axis with comma separators for readability
plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

# Remove gridlines for a cleaner look
plt.grid(False)

# Save the plot
os.makedirs(output_dir, exist_ok=True)
plot_filename = os.path.join(output_dir, "top_10_job_titles.png")
plt.savefig(plot_filename, dpi=300, bbox_inches="tight")



# Plot 4: Horizontal Bar Chart - Highest-Paying Jobs by Median

# Compute median salary per job title and select top 10
top_paying_jobs = df.groupby("job_title")["salary_in_usd"].median().nlargest(10)

# Create figure
plt.figure(figsize=(11, 7))

# Plot horizontal bar chart
plt.barh(top_paying_jobs.index, top_paying_jobs.values, color="#4B0082", edgecolor="black", linewidth=0.7, alpha=0.75, height=0.75)

# Title and labels
plt.title("Highest-Paying Data Science Jobs", fontsize=16, fontweight="bold", pad=15)
plt.xlim(0, top_paying_jobs.max() * 1.15)  # Extra breathing room on the right
plt.xlabel("Median Salary (USD)", fontsize=12, fontweight="bold", labelpad=12)
plt.xticks(ticks=range(0, 400000, 75000))  # Increase step size
plt.ylabel("Job Title", fontsize=12, fontweight="bold", labelpad=12)

# Format x-axis with commas for readability
plt.gca().xaxis.set_major_formatter(plt.matplotlib.ticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))

# Sort in descending order
plt.gca().invert_yaxis()

# Adjust spacing to prevent y-axis labels from getting cut off
plt.subplots_adjust(left=0.35)  # Increase left padding

# Remove gridlines for a cleaner look
plt.grid(False)

# Save the plot
os.makedirs(output_dir, exist_ok=True)
plot_filename = os.path.join(output_dir, "highest_paying_job_titles.png")
plt.savefig(plot_filename, dpi=300, bbox_inches="tight")



# Plot 5: Line Chart - Salary Over Time (Top Job Titles)

# Get the top 4 job titles by count and filter those present in all years
top_jobs = df["job_title"].value_counts().index[:4]
df_filtered = df[df["job_title"].isin(top_jobs)]

# Keep only jobs that have salary data for all four years
valid_jobs = df_filtered.groupby("job_title")["work_year"].nunique()
valid_jobs = valid_jobs[valid_jobs == 4].index  # Ensure 4 years present

# Rename "Machine Learning Engineer" to "ML Engineer" for better display
valid_jobs = valid_jobs.str.replace("Machine Learning Engineer", "ML Engineer")

# Filter dataset for valid jobs
df_top_jobs = df[df["job_title"].isin(valid_jobs)]

# Compute average salary per job title per year
salary_over_time = df_top_jobs.groupby(["work_year", "job_title"])["salary_in_usd"].mean().unstack()

# Rename column in the dataframe to reflect the new job title
salary_over_time = salary_over_time.rename(columns={"Machine Learning Engineer": "ML Engineer"})

# Define custom colors that avoid red but provide differentiation
custom_colors = ["#1f77b4", "#cc5500", "#2ca02c", "#9467bd"]  # Blue, Orange, Green, Purple

# Reduce plot width while leaving room for the legend
plt.figure(figsize=(10, 6))

# Plot the average salary lines with the color scheme
for i, job in enumerate(valid_jobs):
    plt.plot(salary_over_time.index, salary_over_time[job], label=job, color=custom_colors[i], linewidth=2.5)

# Title and labels
plt.title("Salary Over Time for Top Job Titles", fontsize=16, fontweight="bold", pad=15)
plt.xlabel("Year", fontsize=12, fontweight="bold", labelpad=12)
plt.ylabel("Average Salary (USD)", fontsize=12, fontweight="bold", labelpad=12)

# Format x-axis to show whole years only
plt.xticks(ticks=salary_over_time.index, labels=[int(year) for year in salary_over_time.index], fontsize=12)

# Format y-axis without the dollar sign
plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

# Remove gridlines for a cleaner look
plt.grid(False)

# Legend
plt.legend(title="Job Title", fontsize=10, title_fontsize=12, loc="lower right", bbox_to_anchor=(0.98, 0.02), frameon=True, framealpha=0.8)

# Save the plot
os.makedirs(output_dir, exist_ok=True)
plot_filename = os.path.join(output_dir, "salary_over_time_top4.png")
plt.savefig(plot_filename, dpi=300, bbox_inches="tight")



# Plot 6: Box Plot - Salary Distribution by Experience Level

# Define the order of experience levels
experience_order = ["Entry-Level", "Mid-Level", "Senior-Level", "Executive-Level"]

# Map experience codes to full names
experience_labels = {
    "EN": "Entry-Level",
    "MI": "Mid-Level",
    "SE": "Senior-Level",
    "EX": "Executive-Level"
}

# Replace short codes with full labels in the dataset
df["experience_level"] = df["experience_level"].map(experience_labels)

# Create figure
plt.figure(figsize=(10, 6))

# Custom colors
soft_colors = ["#8DA0CB", "#FC8D62", "#66C2A5", "#E78AC3"]

# Create a box plot with no outliers
sns.boxplot(
    x="experience_level", 
    y="salary_in_usd", 
    data=df, 
    order=experience_order, 
    palette=soft_colors,  
    linewidth=2,  
    whiskerprops={'linewidth': 1.5, 'color': '#333333'},  
    medianprops={'linewidth': 2, 'color': 'black'},  
    showfliers=False  # Hides outliers
)


# Title and labels
plt.title("Salary Ranges by Experience Level", fontsize=16, fontweight="bold", pad=20)
plt.xlabel("Experience Level", fontsize=12, fontweight="bold", labelpad=12)
plt.ylabel("Salary (USD)", fontsize=12, fontweight="bold", labelpad=12)

# Format y-axis with commas for large numbers
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))

# Remove gridlines
plt.grid(False)

# Save the figure
os.makedirs(output_dir, exist_ok=True)
plot_filename = os.path.join(output_dir, "salary_distribution_experience.png")
plt.savefig(plot_filename, dpi=300, bbox_inches="tight")

plt.show()

# Plot 7: Choropleth Map - Average Data Science Salary by Country

# Remove "Other (543)" or invalid country values
df = df[df["company_location"] != "Other (543)"]

# Convert Alpha-2 to Alpha-3 ISO country codes
def convert_iso2_to_iso3(iso2):
    try:
        return pycountry.countries.get(alpha_2=iso2).alpha_3
    except AttributeError:
        return None  # Handle missing codes

df["iso_code"] = df["company_location"].apply(convert_iso2_to_iso3)
df = df.dropna(subset=["iso_code"])  # Drop invalid country codes

# Aggregate salary by country
country_salary = df.groupby(["iso_code", "company_location"])["salary_in_usd"].mean().reset_index()

# Create Choropleth Map
fig = px.choropleth(
    country_salary,
    locations="iso_code",  
    locationmode="ISO-3",  
    color="salary_in_usd",
    hover_name="company_location",
    hover_data={"salary_in_usd": ":,.0f"},  
    color_continuous_scale="Viridis",
    title="Average Data Science Salary by Country"
)

# Adjust map projection & formatting
fig.update_layout(
    geo=dict(showcoastlines=True, projection_type="natural earth"),
    coloraxis_colorbar=dict(title="Avg Salary (USD)", tickprefix="$"),
)

# Save as PNG
png_filename = os.path.join(output_dir, "average_salary_map.png")
fig.write_image(png_filename, scale=3)  # High-resolution PNG

# Save as HTML (Interactive)
html_filename = os.path.join(output_dir, "average_salary_map.html")
fig.write_html(html_filename)

# Show plot
fig.show()


