import concurrent.futures

from collections import defaultdict
from pathlib import Path
import time

def search_in_file(file_path, keywords):
    result =[]
    try:
        with open(file_path, "r") as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    result.append((keyword, file_path))
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
    return result

def main_concurrent(file_paths, keywords):
    start_time = time.time()
    results = defaultdict(list)

    with concurrent.futures.ProcessPoolExecutor(max_workers= 8) as executor:
        futures = {executor.submit(search_in_file, file_path, keywords): file_path for file_path in file_paths}
        for future in concurrent.futures.as_completed(futures):
            file_path=futures[future]
            try:
                result = future.result()
                for keyword, file_path in result:
                    results[keyword].append(file_path)
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")

    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    return results
   
if __name__ =="__main__":
    file_paths = list(Path("C:/Users/tutov/Documents/GitHub/goit-cs-hw-04").glob("*.py"))
    keywords = ["modify_", "multiprocessing"]
    results= main_concurrent(file_paths, keywords)
    print(results)
        

