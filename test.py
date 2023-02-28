import re

# Sample string
string_with_stars = "Hello ***** world! This is a ******** test ** string *****."

# Replace all occurrences of more than 5 consecutive asterisks with '***'
new_string = re.sub(r'\*{5,}', '***', string_with_stars)

print(new_string)
