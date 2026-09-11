inventory = 0
failed_entries = 0

while True:
    stock_input = input("Enter Stock Quantity (or 'quit' to stop): ")

    if stock_input.lower() == "quit":
        break

    elif not stock_input.lstrip("-").isdigit():
        print("Invalid input. Please enter a valid stock quantity.")
        failed_entries += 1
        continue

    else:
        stock_quantity = int(stock_input)

        if stock_quantity < 0:
            print("Stock quantity cannot be negative.")
            failed_entries += 1
            continue

        inventory += stock_quantity

        if inventory > 500:
            print("Inventory limit exceeded!")
            break

print("Total Units Processed:", inventory)
print("Number of Failed/Rejected Entries:", failed_entries)