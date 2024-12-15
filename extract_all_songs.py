import json
import os
import shutil

# Get the current working directory
current_directory = os.getcwd()

# Define the paths dynamically based on the current directory
pending_dir = os.path.join(current_directory, "Spotify Playlist", "pending")
extracted_dir = os.path.join(current_directory, "Spotify Playlist", "extracted")
completed_dir = os.path.join(current_directory, "Spotify Playlist", "completed")

# pending_dir = r"C:\Users\bhara\Desktop\Self Projects\RPA_Automation\Spotify Playlist\pending"
# extracted_dir = r"C:\Users\bhara\Desktop\Self Projects\RPA_Automation\Spotify Playlist\extracted"
# completed_dir = r"C:\Users\bhara\Desktop\Self Projects\RPA_Automation\Spotify Playlist\completed"

# Get all text files in the 'pending' directory
pending_files = [f for f in os.listdir(pending_dir) if f.endswith(".txt")]

for file_name in pending_files:
    input_file = os.path.join(pending_dir, file_name)
    output_file = os.path.join(extracted_dir, f"extracted_{file_name}")
   
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

        # Move the processed file to 'completed'
        completed_file = os.path.join(completed_dir, file_name)
        shutil.move(input_file, completed_file)
        print(f"File {file_name} moved to completed directory.")

    except FileNotFoundError:
        print(f"Error: Input file {input_file} not found.")
    except json.JSONDecodeError:
        print(f"Error: The file {input_file} does not contain valid JSON.")
    except KeyError as e:
        print(f"Error: Missing expected key in JSON structure: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while processing {input_file}: {e}")
