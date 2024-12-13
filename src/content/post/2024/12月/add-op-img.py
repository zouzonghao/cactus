import os

def update_md_headers(directory):
    """Recursively update the headers of all .md files in the given directory."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                # Find the header block
                if len(lines) > 1 and lines[0].strip() == '---':
                    try:
                        header_end_index = lines[1:].index('---\n') + 1
                    except ValueError:
                        print(f"Skipping file with malformed header: {file_path}")
                        continue

                    # Insert ogImage line if not present
                    if not any(line.startswith('ogImage:') for line in lines[:header_end_index]):
                        lines.insert(header_end_index, 'ogImage: "/social-card.avif"\n')

                        # Write the updated content back to the file
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.writelines(lines)
                        print(f"Updated file: {file_path}")
                    else:
                        print(f"File already contains ogImage: {file_path}")
                else:
                    print(f"No valid header found in file: {file_path}")

if __name__ == "__main__":
    directory = input("Please enter the directory containing .md files: ").strip()
    if os.path.isdir(directory):
        print(f"Scanning directory: {directory}")
        update_md_headers(directory)
    else:
        print(f"The specified directory does not exist: {directory}")
