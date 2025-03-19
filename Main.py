import numpy as np
import random
import matplotlib.pyplot as plt
import csv



def check_date_validity(date_day, date_month, date_year):
    try:
        if not (1 <= date_month <= 12):
            return False
            
        if not (1 <= date_day <= 31):
            return False
            
        if date_month in {4, 6, 9, 11} and date_day > 30:
            return False
            
        if date_month == 2:
            is_leap = (date_year % 4 == 0 and date_year % 100 != 0) or (date_year % 400 == 0)
            
            return date_day <= (29 if is_leap else 28)
            
        return True
        
    except:
        return False



TOTAL_INDIVIDUALS = 100

TOTAL_EVOLUTION_CYCLES = 100

CHANCE_OF_CHANGE = 0.15



def create_random_date():
    return random.randint(1, 31), random.randint(1, 12), random.randint(0, 9999)



def create_initial_date_pool():
    return [create_random_date() for _ in range(TOTAL_INDIVIDUALS)]



def get_date_type(date_day, date_month, date_year):
    if not check_date_validity(date_day, date_month, date_year):
        return "Invalid"
        
    return {
        2: "Leap Year" if (date_year % 4 == 0 and date_year % 100 != 0) or (date_year % 400 == 0) else "February",
        4: "30-day Month", 6: "30-day Month", 9: "30-day Month", 11: "30-day Month"
    }.get(date_month, "31-day Month")



def evaluate_date_quality(date_specimen, already_tested_dates, date_type_counts):
    date_day, date_month, date_year = date_specimen
    
    formatted_specimen = f"{date_day:02d}/{date_month:02d}/{date_year:04d}"
    
    
    
    if formatted_specimen in already_tested_dates:
        return 0
    
    
    
    specimen_category = get_date_type(date_day, date_month, date_year)
    
    date_type_counts[specimen_category] = date_type_counts.get(specimen_category, 0) + 1
    
    
    
    quality_multipliers = {"Leap Year": 3, "Invalid": 2, "February": 1.5, "30-day Month": 1, "31-day Month": 1}
    
    specimen_quality = quality_multipliers.get(specimen_category, 1) / (1 + date_type_counts[specimen_category])
    
    
    
    already_tested_dates.add(formatted_specimen)
    
    return specimen_quality



def choose_breeding_specimens(date_pool, quality_ratings):
    total_quality = sum(quality_ratings)
    
    
    
    if total_quality == 0:
        selection_weights = [1 / len(quality_ratings)] * len(quality_ratings)
        
    else:
        selection_weights = [rating / total_quality for rating in quality_ratings]
    
    
    
    specimen_indices = np.arange(len(date_pool))
    
    chosen_indices = np.random.choice(specimen_indices, size=TOTAL_INDIVIDUALS // 2, replace=True, p=selection_weights)
    
    
    
    chosen_specimens = [date_pool[i] for i in chosen_indices]
    
    return chosen_specimens



def combine_parent_dates(parent_date_1, parent_date_2):
    crossover_point = random.randint(0, 2)
    
    return parent_date_1[:crossover_point] + parent_date_2[crossover_point:]



def introduce_date_variations(date_specimen):
    date_day, date_month, date_year = date_specimen
    
    
    
    if random.random() < CHANCE_OF_CHANGE:
        date_day = random.choice([1, date_day, 28, 29, 30, 31])
        
    
    
    if random.random() < CHANCE_OF_CHANGE:
        date_month = random.choice([1, date_month, 2, 6, 12])
        
    
    
    if random.random() < CHANCE_OF_CHANGE:
        date_year = max(0, min(9999, date_year + random.choice([-400, -100, -4, 0, 4, 100, 400])))
        
    
    
    return date_day, date_month, date_year



def analyze_date_coverage(date_collection):
    category_distribution = {}
    
    
    
    for date_entry in date_collection:
        date_day, date_month, date_year = map(int, date_entry.split('/'))
        
        category = get_date_type(date_day, date_month, date_year)
        
        category_distribution[category] = category_distribution.get(category, 0) + 1
    
    
    
    possible_categories = ["Leap Year", "February", "30-day Month", "31-day Month", "Invalid"]
    
    
    
    total_dates = len(date_collection)
    
    coverage_metrics = {}
    
    
    
    for category in possible_categories:
        quantity = category_distribution.get(category, 0)
        
        proportion = (quantity / total_dates * 100) if total_dates > 0 else 0
        
        coverage_metrics[category] = (quantity, proportion)
    
    
    
    return coverage_metrics



def save_test_dates(valid_dates, invalid_dates, edge_case_dates, output_filename="date_test_cases.csv"):
    with open(output_filename, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        
        
        
        csv_writer.writerow(['Date Type', 'Date Value', 'Date Category'])
        
        
        
        for date_entry in valid_dates:
            date_day, date_month, date_year = map(int, date_entry.split('/'))
            
            category = get_date_type(date_day, date_month, date_year)
            
            csv_writer.writerow(['Valid', date_entry, category])
            
            
            
        for date_entry in invalid_dates:
            csv_writer.writerow(['Invalid', date_entry, 'Invalid'])
            
            
            
        for date_entry in edge_case_dates:
            date_day, date_month, date_year = map(int, date_entry.split('/'))
            
            category = get_date_type(date_day, date_month, date_year)
            
            csv_writer.writerow(['Boundary', date_entry, category])
    
    
    
    print(f"Test dates exported to {output_filename}")



def evolve_date_test_cases():
    date_pool = create_initial_date_pool()
    
    coverage_history, tested_dates, date_type_counts = [], set(), {}
    
    valid_test_dates, invalid_test_dates = [], []
    
    
    
    edge_case_dates = {
        "01/01/0000",  
        "31/12/9999",  
        "29/02/2020",  
        "28/02/2100",  
        "29/02/2000",  
        "31/01/2023",  
        "30/04/2023",  
        "28/02/2023",  
        "31/12/1999",  
        "01/01/2000"   
    }
    
    
    
    tested_dates.update(edge_case_dates)
    
    
    
    for generation in range(TOTAL_EVOLUTION_CYCLES):
        quality_scores = [evaluate_date_quality(specimen, tested_dates, date_type_counts) for specimen in date_pool]
        
        
        
        coverage_history.append(len(tested_dates))
        
        
        
        breeding_pool = choose_breeding_specimens(date_pool, quality_scores)
        
        
        
        date_pool = [
            introduce_date_variations(
                combine_parent_dates(
                    random.choice(breeding_pool), 
                    random.choice(breeding_pool)
                )
            )
            for _ in range(TOTAL_INDIVIDUALS)
        ]
    
    
    
    for date_entry in tested_dates:
        date_day, date_month, date_year = map(int, date_entry.split('/'))
        
        
        
        if check_date_validity(date_day, date_month, date_year):
            valid_test_dates.append(date_entry)
            
        else:
            invalid_test_dates.append(date_entry)
    
    
    
    while len(valid_test_dates) < 10:
        new_specimen = create_random_date()
        
        formatted_date = f"{new_specimen[0]:02d}/{new_specimen[1]:02d}/{new_specimen[2]:04d}"
        
        
        
        if check_date_validity(*new_specimen) and formatted_date not in valid_test_dates:
            valid_test_dates.append(formatted_date)
    
    
    
    while len(invalid_test_dates) < 10:
        new_specimen = create_random_date()
        
        formatted_date = f"{new_specimen[0]:02d}/{new_specimen[1]:02d}/{new_specimen[2]:04d}"
        
        
        
        if not check_date_validity(*new_specimen) and formatted_date not in invalid_test_dates:
            invalid_test_dates.append(formatted_date)
    
    
    
    return valid_test_dates, invalid_test_dates, edge_case_dates, coverage_history



valid_test_dates, invalid_test_dates, edge_case_dates, coverage_history = evolve_date_test_cases()



print("Best Test Dates:")

print("Valid:", ", ".join(valid_test_dates[:10]))

print("Invalid:", ", ".join(invalid_test_dates[:10]))

print("Boundary:", ", ".join(edge_case_dates))

print(f"Evolution Cycles Completed: {TOTAL_EVOLUTION_CYCLES}")



all_test_dates = valid_test_dates + invalid_test_dates + list(edge_case_dates)

coverage_metrics = analyze_date_coverage(all_test_dates)



print("\nTest Coverage Analysis:")

print("-" * 45)

print(f"{'Category':<15} {'Count':<10} {'Percentage':<10}")

print("-" * 45)

for category, (count, percentage) in coverage_metrics.items():
    print(f"{category:<15} {count:<10} {percentage:.2f}%")
    
print("-" * 45)

print(f"Total: {len(all_test_dates)} test dates")



save_test_dates(valid_test_dates[:10], invalid_test_dates[:10], edge_case_dates)



plt.figure(figsize=(10, 6))

plt.plot(range(TOTAL_EVOLUTION_CYCLES), coverage_history, marker='o', linestyle='-')

plt.xlabel("Evolution Cycles")

plt.ylabel("Test Dates Discovered")

plt.title("Test Coverage Growth Over Time")

plt.grid(True)

plt.show()



categories = list(coverage_metrics.keys())

counts = [coverage_metrics[cat][0] for cat in categories]



plt.figure(figsize=(10, 6))

plt.bar(categories, counts)

plt.xlabel("Date Categories")

plt.ylabel("Number of Test Dates")

plt.title("Distribution of Test Dates by Category")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()