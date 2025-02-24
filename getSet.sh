#!/bin/sh
# Check if a file is provided as an argument
if [ $# -eq 0 ]; then
echo "Usage: $0 <input_file>"
exit 1
fi

input_file="$1"

# Check if the file exists
if [ ! -f "$input_file" ]; then
echo "Error: File '$input_file' not found."
exit 1
fi

# Read the file line by line and execute a command for each line
while IFS= read -r line; do
	# Replace the following line with the command you want to execute
	echo "Pulling: $line"
	ollama pull "$line"
done < "$input_file"
