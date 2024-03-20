import concurrent.futures
from collections import defaultdict
from pathlib import Path
import time
from multiprocessing import Queue, Process

def search_in_file(file_path, keywords, results_queue):
    result = []
    try:
        with open(file_path, "r") as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    result.append((keyword, file_path))
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
    results_queue.put(result)

def process_files(file_paths, keywords, results_queue):
    for file_path in file_paths:
        search_in_file(file_path, keywords, results_queue)

def main_multiprocessing(file_paths, keywords, num_processes=8):
    start_time = time.time()
    results = defaultdict(list)

    # Розділити список файлів на підсписки для процесів
    file_chunks = [file_paths[i::num_processes] for i in range(num_processes)]

    # Створити чергу для обміну даними між процесами
    results_queue = Queue()

    # Запустити кожен процес для обробки своєї частини файлів
    processes = []
    for file_chunk in file_chunks:
        process = Process(target=process_files, args=(file_chunk, keywords, results_queue))
        process.start()
        processes.append(process)

    # Зібрати результати з черги
    for _ in range(len(file_paths)):
        result = results_queue.get()
        for keyword, file_path in result:
            results[keyword].append(file_path)

    # Завершити всі процеси
    for process in processes:
        process.join()

    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    return results

if __name__ == "__main__":
    file_paths = list(Path("C:/Users/tutov/Documents/GitHub/goit-cs-hw-04").glob("*.txt"))
    keywords = ["Harry", "dump", "apple"] 
    results = main_multiprocessing(file_paths, keywords)
    print(results)
