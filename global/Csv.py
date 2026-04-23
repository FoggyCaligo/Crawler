import csv

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Ingredients', 'Steps'])
        for recipe in data:
            title = recipe['title']
            print(title)
            ingredients = '; '.join([f"{ing['name']} ({ing['quantity']})" for ing in recipe['ingredients']])
            print(ingredients)
            steps = '; '.join([f"{step['description']} ({step['image']})" for step in recipe['steps']])
            print(steps)

            writer.writerow([title, ingredients, steps])
        print(f"Data saved to {filename}")
        