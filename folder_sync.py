import os
import time
import shutil
import hashlib
import argparse
from datetime import datetime

def calculate_md5(file_path):
    """Calculate the MD5 checksum of a file."""
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            md5.update(chunk)
    return md5.hexdigest()

def sync_folders(source, replica, log_file):
    """Synchronize two folders to ensure the replica is an identical copy of the source."""
    
    # Open the log file in append mode to record actions
    with open(log_file, 'a') as log:
        
        # Iterate through the source folder
        for root, dirs, files in os.walk(source):
            relative_path = os.path.relpath(root, source)
            replica_root = os.path.join(replica, relative_path)
            
            # Check and create missing directories in the replica
            if not os.path.exists(replica_root):
                os.makedirs(replica_root)
                log_message = f"{datetime.now()} - Created directory: {replica_root}"
                print(log_message)
                log.write(log_message + "\n")
        
        # Copy or update files from source to replica
        for root, dirs, files in os.walk(source):
            relative_path = os.path.relpath(root, source)
            replica_root = os.path.join(replica, relative_path)
            
            for file in files:
                source_file = os.path.join(root, file)
                replica_file = os.path.join(replica_root, file)

                # Check if file needs to be copied or updated
                if not os.path.exists(replica_file) or calculate_md5(source_file) != calculate_md5(replica_file):
                    shutil.copy2(source_file, replica_file)
                    log_message = f"{datetime.now()} - Copied file: {source_file} to {replica_file}"
                    print(log_message)
                    log.write(log_message + "\n")
        
        # Remove files and directories from replica that no longer exist in the source
        for root, dirs, files in os.walk(replica, topdown=False):
            relative_path = os.path.relpath(root, replica)
            source_root = os.path.join(source, relative_path)
            
            for file in files:
                replica_file = os.path.join(root, file)
                source_file = os.path.join(source_root, file)
                
                # Remove files that are not in source anymore
                if not os.path.exists(source_file):
                    os.remove(replica_file)
                    log_message = f"{datetime.now()} - Removed file: {replica_file}"
                    print(log_message)
                    log.write(log_message + "\n")
            
            # Remove directories that are not in source anymore
            for dir in dirs:
                replica_dir = os.path.join(root, dir)
                source_dir = os.path.join(source_root, dir)
                if not os.path.exists(source_dir):
                    shutil.rmtree(replica_dir)
                    log_message = f"{datetime.now()} - Removed directory: {replica_dir}"
                    print(log_message)
                    log.write(log_message + "\n")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Synchronize two folders to keep them identical.')
    parser.add_argument('source', type=str, help='Path to the source folder')
    parser.add_argument('replica', type=str, help='Path to the replica folder')
    parser.add_argument('interval', type=int, help='Synchronization interval in seconds')
    parser.add_argument('log_file', type=str, help='Path to the log file')

    # Parse the arguments
    args = parser.parse_args()

    # Continuous synchronization loop
    while True:
        try:
            sync_folders(args.source, args.replica, args.log_file)
        except Exception as e:
            print(f"Error during synchronization: {e}")
        finally:
            time.sleep(args.interval)

if __name__ == "__main__":
    main()
