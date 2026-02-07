from functions.get_file_content import get_file_content

results = get_file_content("calculator", "lorem.txt")

print(len(results))
print(results[-100:])

results = get_file_content("calculator", "main.py")
print(results)

results = get_file_content("calculator", "pkg/calculator.py")
print(results)

results = get_file_content("calculator", "/bin/cat")
print(results)

results = get_file_content("calculator", "pkg/does_not_exist.py")
print(results)