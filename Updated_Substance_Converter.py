
import json

def save_substances_to_file(substances_dict, filename="substances.json"):
    with open(filename, 'w') as f:
        json.dump(substances_dict, f, indent=4)

def load_substances_from_file(filename="substances.json"):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file does not exist
substances = {}

def convert_density(value, unit):
    """Convert various density units to g/mL."""
    unit = unit.lower()
    if unit == "g/ml":
        return value  # Already in g/mL
    elif unit == "kg/l":
        return value * 1000  # 1 kg/L = 1000 g/mL
    elif unit == "oz/fluid oz":
        return value * 29.5735  # 1 oz/fl oz = 29.5735 g/mL
    elif unit == "lb/gal":
        return value * 119.826  # 1 lb/gal = 119.826 g/mL
    else:
        return None  # Unsupported unit

def calculate_volume(substance, mass_mg):
    """Calculate the volume of a substance based on its mass and density."""
    if substance in substances:
        density = substances[substance]  # density in g/mL
        mass_g = mass_mg / 1000  # convert mg to g
        volume_ml = mass_g / density  # volume in mL
        volume_tablespoons = volume_ml / 14.7868  # convert mL to tablespoons
        return volume_ml, volume_tablespoons
    else:
        return None, None


def parse_input(user_input):
    """Parse the user input to extract the mass in mg and the substance name."""
    parts = user_input.split()
    if len(parts) == 2 and parts[0].endswith("mg"):
        mass_mg = int(parts[0][:-2])  # Remove 'mg' and convert to integer
        substance = parts[1].lower()  # Convert substance name to lowercase
        return mass_mg, substance
    else:
        return None, None


def add_substance(input_string):
    """Add a new substance to the dictionary with improved parsing."""
    parts = input_string.split()
    if len(parts) >= 3 and parts[0].lower() == "add":
        substance = parts[1].lower()  # Substance name

        # Combine the remaining parts and split on the unit boundary
        density_str = ''.join(parts[2:])
        matched = False
        for unit in ["g/ml", "kg/l", "oz/fl oz", "lb/gal"]:
            unit_clean = unit.replace(" ", "").replace("/", "").lower()
            density_str_clean = density_str.lower().replace(" ", "").replace("/", "")
            if unit_clean in density_str_clean:
                matched = True
                density_value_str = density_str_clean.split(unit_clean)[0]
                try:
                    density_value = float(density_value_str)  # Convert to float
                except ValueError:
                    return "Invalid density value."

                # Convert to g/mL
                standardized_density = convert_density(density_value, unit)
                if standardized_density is not None:
                    substances[substance] = standardized_density
                    save_substances_to_file(substances)  # Save the updated dictionary
                    return f"Added {substance} with density {standardized_density} g/mL to the database."
                else:
                    return "Unsupported density unit."
        if not matched:
            return "Density unit not found."
    else:
        return "Invalid format for adding substance."





def main():
    global substances
    substances = load_substances_from_file()  # Load the substances at the start
    
    while True:
        user_input = input("Enter a command, or 'exit' to quit: ")
        if user_input.lower() == 'exit':
            save_substances_to_file(substances)  # Save the substances before exiting
            break
        if user_input.lower() == 'exit':
            break

        if user_input.lower().startswith("add"):
            feedback = add_substance(user_input)
            print(feedback)
        else:
            mass_mg, substance = parse_input(user_input)
            if mass_mg is not None:
                volume_ml, volume_tablespoons = calculate_volume(substance, mass_mg)
                if volume_ml is not None:
                    print(f"For {mass_mg} mg of {substance}, you need {volume_ml:.2f} mL or {volume_tablespoons:.2f} tablespoons.")
                else:
                    print(f"Substance '{substance}' not found in the database.")
            else:
                print("Invalid input format. Please use the format '250mg salt' or 'add substance density'.")

# This condition checks if the script is being run directly (not imported as a module)
if __name__ == "__main__":
    main()  # This should start the main function when you run the script
"Program updated to include substance addition feature. To run it, use the 'main()' function in a Python environment."


        # ... rest of the main function logic

main()  # This should start the main function when you run the script
"Program updated to include substance addition feature. To run it, use the 'main()' function in a Python environment."
