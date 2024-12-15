import json

# File paths
input_file = r"C:\Users\bhara\Desktop\Self Projects\RPA_Automation\Spotify Playlist\pending\Soothing______.txt"
output_file = r"C:\Users\bhara\Desktop\Self Projects\RPA_Automation\Spotify Playlist\extracted\Extracted_Soothing______.txt"

try:
    # Read the JSON from the file
    with open(input_file, "r") as file:
        json_data = json.load(file)

    # Extract the "name" fields
    names = []
    items = json_data["data"]["playlistV2"]["content"]["items"]

    for item in items:
        name = item["itemV2"]["data"].get("name")
        if name:
            names.append(name)

    # Write the names to the output file
    with open(output_file, "w") as file:
        file.write("\n".join(names))

    print(f"Names extracted and saved to {output_file}")

except FileNotFoundError:
    print(f"Error: Input file {input_file} not found.")
except json.JSONDecodeError:
    print("Error: The file does not contain valid JSON.")
except KeyError as e:
    print(f"Error: Missing expected key in JSON structure: {e}")
