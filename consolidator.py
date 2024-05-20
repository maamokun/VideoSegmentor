import os
import shutil

# Directory paths
processed_output_dir = 'oaiw_processed'
consolidated_dir = 'consolidated_data'

def consolidate_files(processed_output_dir, consolidated_dir):
    os.makedirs(consolidated_dir, exist_ok=True)
    consolidated_manifest_path = os.path.join(consolidated_dir, 'consolidated_manifest.txt')

    manifest_lines = []
    file_counter = 1

    # Iterate through all subdirectories in the processed output directory
    for subdir in os.listdir(processed_output_dir):
        subdir_path = os.path.join(processed_output_dir, subdir)

        if os.path.isdir(subdir_path):
            manifest_path = os.path.join(subdir_path, 'manifest.txt')

            # Read the manifest file of the subdirectory
            with open(manifest_path, 'r', encoding='utf-8') as manifest_file:
                lines = manifest_file.readlines()

            # Move each audio file and update the manifest
            for line in lines:
                audio_file, _, transcription = line.strip().partition('|0|')
                src_audio_path = os.path.join(subdir_path, audio_file)

                if os.path.exists(src_audio_path):
                    dest_audio_filename = f"audio{file_counter}.wav"
                    dest_audio_path = os.path.join(consolidated_dir, dest_audio_filename)

                    shutil.move(src_audio_path, dest_audio_path)
                    manifest_lines.append(f"{dest_audio_filename}|0|{transcription}")
                    file_counter += 1
                else:
                    print(f"Warning: Missing audio file {src_audio_path}")

    # Write the consolidated manifest file
    with open(consolidated_manifest_path, 'w', encoding='utf-8') as consolidated_manifest_file:
        consolidated_manifest_file.write("\n".join(manifest_lines))

# Run the consolidation process
consolidate_files(processed_output_dir, consolidated_dir)

print("Consolidation complete! UwU 🎉")
