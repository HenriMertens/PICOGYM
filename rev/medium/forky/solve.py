from numpy import int32

initial_value = int32(1000000000)
increment_value = int32(1234567890)
process_count = 16

final_value = initial_value
for _ in range(process_count):
    final_value += increment_value

print(final_value)  # This will give an error but also print the number
