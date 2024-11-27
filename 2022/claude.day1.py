def find_max_calories(input_data):
    current_calories = 0
    max_calories = 0
    
    # Split input into lines
    lines = input_data.strip().split('\n')
    
    for line in lines:
        if line.strip():
            # Add calories for current elf
            current_calories += int(line)
        else:
            # Empty line - check if current elf has max calories
            max_calories = max(max_calories, current_calories)
            current_calories = 0
    
    # Check final elf
    max_calories = max(max_calories, current_calories)
    
    return max_calories

# Example usage
example_input = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

example_input = open('day1.dat', 'r').read()

result = find_max_calories(example_input)
print(f"Maximum calories carried: {result}")  # Should output 24000

