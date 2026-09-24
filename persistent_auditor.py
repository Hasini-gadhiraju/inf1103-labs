
file = "inventory.txt"
history = []


def get_valid_input():
    while True:
        stock_input = input("Enter Stock Quantity (or 'quit' to stop): ")

        if stock_input.lower() == "quit":
            return None

        elif not stock_input.lstrip("-").isdigit():
            print("Invalid input. Please enter a valid stock quantity.")
            return "invalid"

        else:
            stock_quantity = int(stock_input)

            if stock_quantity < 0:
                print("Stock quantity cannot be negative.")
                return "invalid"

            return stock_quantity


def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total


def calculate_tax(amount):
    tax = amount * 0.10
    return tax


def generate_report(total_units, failed_attempts):
    print("\n--- Final Report ---")
    print("Total inventory units:", total_units)
    print("Failed attempts:", failed_attempts)
    print("Transaction history:", history)


# Load previously saved inventory and history
def load_inventory():
    try:
        with open(file, "r") as f:
            inventory = int(f.readline().strip())

            for line in f:
                history.append(int(line.strip()))

            return inventory

    except FileNotFoundError:
        return 0


# Save the final total and transaction history
def save_inventory(inventory):
    with open(file, "w") as f:
        f.write(str(inventory) + "\n")

        for entry in history:
            f.write(str(entry) + "\n")


# Main program
inventory = load_inventory()
failed_entries = 0

while True:
    stock_quantity = get_valid_input()

    if stock_quantity is None:
        break

    if stock_quantity == "invalid":
        failed_entries += 1
        continue

    history.append(stock_quantity)
    inventory = process_delivery(inventory, stock_quantity)

    tax = calculate_tax(stock_quantity)
    print("Tax for this delivery:", tax)

    if inventory > 500:
        print("Inventory limit exceeded!")
        break

generate_report(inventory, failed_entries)
save_inventory(inventory)