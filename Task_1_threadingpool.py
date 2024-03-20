import concurrent.futures
from collections import defaultdict
from pathlib import Path
import time

def search_in_file(file_path, keywords):
    result = []
    try:
        with open(file_path, "r") as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    result.append((keyword, file_path))
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
    return result

def main_concurrent(file_paths, keywords, num_threads=8):
    start_time = time.time()
    results = defaultdict(list)

    # Розділити список файлів на підсписки для потоків
    file_chunks = [file_paths[i::num_threads] for i in range(num_threads)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for file_chunk in file_chunks:
            futures.append(executor.submit(process_files, file_chunk, keywords))
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            for keyword, file_path in result:
                results[keyword].append(file_path)

    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    return results

def process_files(file_paths, keywords):
    result = []
    for file_path in file_paths:
        result.extend(search_in_file(file_path, keywords))
    return result
   
if __name__ == "__main__":
    file_paths = list(Path("C:/Users/tutov/Documents/GitHub/goit-cs-hw-04").glob("*.txt"))
    keywords = ["Harry", "dump", "apple"]  # Замініть ці ключові слова на потрібні
    results = main_concurrent(file_paths, keywords)
    print(results)