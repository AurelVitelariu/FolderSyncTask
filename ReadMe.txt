# FolderSync

## Overview

This is a Python program I developed as part of a coding task. The goal was to synchronize two folders: a source folder and a replica folder. The replica is always kept as an exact copy of the source. Any changes in the source—like new files, updates, or deletions—are reflected in the replica, but not the other way around.

## Approach

### Simplicity First

I wanted to keep things straightforward, so I relied on Python’s built-in libraries like `os`, `shutil`, and `hashlib` to get the job done without pulling in any third-party libraries. The idea was to make something that’s easy to understand and maintain.

### Synchronization Logic

1. **Directory Creation**: If a directory exists in the source but not in the replica, the program creates it in the replica.

2. **File Copying/Updating**: I used MD5 checksums to detect changes in files. If a file in the source is new or has changed, it gets copied to the replica.

3. **Removing Old Files**: Files and directories in the replica that no longer exist in the source are deleted to keep the replica clean and in sync.

### Periodic Sync

The program runs continuously at a set interval, which you can specify when you run it. This way, the replica stays up-to-date with any changes in the source folder.

### Logging

All actions, like creating, updating, or deleting files and directories, are logged to both the console and a log file. This helps in tracking what’s happening during each synchronization cycle.

