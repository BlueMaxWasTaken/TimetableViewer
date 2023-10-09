import os
import csv
from prettytable import PrettyTable
from datetime import datetime

class TimetableViewer:
    def __init__(self):
        # Initialize an empty list to store timetable data (list of dictionaries)
        self.data = []

    def load_data(self, folder_path):
        # List CSV files in the specified folder
        csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

        if not csv_files:
            print("No CSV files found in the specified folder.")
            return

        # Load and preprocess raw data from CSV files
        for csv_file in csv_files:
            file_path = os.path.join(folder_path, csv_file)
            with open(file_path, 'r') as file:
                # Use a CSV DictReader to handle CSV data as dictionaries
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    # Eliminate records with the field name "Scheduled Days" with "Online Learning" value
                    if row['Scheduled Days'] != 'Online Learning':
                        self.data.append(row)  # Add the preprocessed row to the data list

    def bubble_sort(self, data, key, ascending=True):
        n = len(data)
        for i in range(n - 1):
            swapped = False
            for j in range(0, n - i - 1):
                # Convert the date strings to datetime objects for comparison
                date1 = datetime.strptime(data[j][key], "%d/%m/%Y")
                date2 = datetime.strptime(data[j + 1][key], "%d/%m/%Y")
                
                # Compare the datetime objects based on the specified key
                if (date1 > date2) if ascending else (date1 < date2):
                    data[j], data[j + 1] = data[j + 1], data[j]  # Swap the elements
                    swapped = True
            if not swapped:
                break

    def list_schedules(self, options):
        if not self.data:
            print("Please load data first.")
            return

        # Check if all filter options are empty
        all_empty = all(value == "" for value in options.values())

        # Apply filters based on user options
        filtered_data = self.data.copy()
        for key, value in options.items():
            if value != "":
                if key == 'Module':
                    # Use list comprehension to filter data by module code substring in the "Description" column
                    filtered_data = [row for row in filtered_data if value.lower() in row['Description'].lower()]
                elif key == 'Lecturer':
                    # Use list comprehension to filter data by lecturer name
                    filtered_data = [row for row in filtered_data if row['Allocated Staff Name'] == value]
                elif key == 'Location':
                    # Use list comprehension to filter data by location/room
                    filtered_data = [row for row in filtered_data if row['Allocated Location Name'] == value]
                elif key == 'Date':
                    # Use list comprehension to filter data by date
                    filtered_data = [row for row in filtered_data if row['Activity Dates (Individual)'] == value]
                elif key == 'Time':
                    # Use list comprehension to filter data by time
                    filtered_data = [row for row in filtered_data if row['Scheduled Start Time'] == value]
                elif key == 'Scheduled Day':
                    filtered_data = [row for row in filtered_data if row['Scheduled Days'].lower() == value.lower()]

        # Sort the filtered data if any filter conditions are applied
        if 'SortBy' in options and not all_empty:
            if options['Module']:
                sort_by = 'Description'
            else:
                sort_by = options['SortBy']

            ascending = options.get('Ascending', True)
            # Sort the filtered data based on the specified field and order using Bubble Sort
            self.bubble_sort(filtered_data, sort_by, ascending)

        # Display the filtered and sorted data in a pretty table
        table = PrettyTable()
        column_order = [
            'Description', 'Activity Dates (Individual)', 'Scheduled Days', 'Scheduled Start Time', 'Scheduled End Time',
            'Duration', 'Allocated Location Name', 'Planned Size', 'Allocated Staff Name', 'Zone Name'
        ]
        table.field_names = column_order
        for row in filtered_data:
            table.add_row([row[column] for column in column_order])

        # Rename columns
        table.field_names = [
            'Description', 'Activity Dates', 'Scheduled Days', 'Scheduled Start Time', 'Scheduled End Time',
            'Duration', 'Location Name', 'Size', 'Staff Name', 'Zone Name'
        ]

        # Center-align the data in each cell
        for field in table.field_names:
            table.align[field] = "c"

        print(table)

if __name__ == "__main__":
    app = TimetableViewer()

    while True:
        print("\nTimetable Viewer Menu:")
        print("1. Load Data")
        print("2. List Schedules")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            folder_path = input("Enter the folder path containing CSV files: ")
            app.load_data(folder_path)
            print("Data loaded successfully!")

        elif choice == '2':
            options = {}
            options['Module'] = input("Enter module code (Leave empty for all modules): ")
            options['Lecturer'] = input("Enter lecturer name (Leave empty for all lecturers): ")
            options['Location'] = input("Enter location/room (Leave empty for all locations): ")
            options['Date'] = input("Enter date (Leave empty for all dates): ")
            options['Time'] = input("Enter time (Leave empty for all times): ")
            options['Scheduled Day'] = input("Enter scheduled day (Leave empty for all days): ")
            options['SortBy'] = input("Enter sorting field: ")
            sort_order = input("Sort in ascending order? (y/n): ").lower()
            options['Ascending'] = sort_order == 'y'

            app.list_schedules(options)
            continue
        
        elif choice == '3':
            break

        else:
            print("Invalid choice. Please try again.")
