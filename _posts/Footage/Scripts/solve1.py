def split_chunks(data, delimiter="ffd8ff"):
    chunks = []
    start = 0 # Start the split at the beginning of the data
    while True:
        index = data.find(delimiter, start) # Find the next occurrence of the delimiter
        if index == -1:
            break
        
        chunk = data[index:index + len(delimiter)] # Add the chunk starting from the delimiter
        next_index = data.find(delimiter, index + len(delimiter)) # Keep adding until the next delimiter
        if next_index == -1:
            chunks.append(data[index:])
            break
        else:
            chunks.append(data[index:next_index])

        start = next_index + len(delimiter) # the next delimiter
    
    return chunks

def hex_to_bytes(hex_string):
    return bytes.fromhex(hex_string) # Convert hex to bytes

def save_chunk_as_file(chunk, chunk_number):
    byte_data = hex_to_bytes(chunk)  # Convert the hex chunk to bytes
    
    with open(f"chunk_{chunk_number}.jpg", "wb") as f:
        f.write(byte_data)
    print(f"Saved chunk_{chunk_number}.jpg")

# usage
data = open("footage.txt").read()
chunks = split_chunks(data)

# save each chunk in a file
for i, chunk in enumerate(chunks):
    save_chunk_as_file(chunk, i + 1)
