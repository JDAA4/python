import hashlib

def hash_id(identifier):
    return hashlib.sha256(identifier.encode()).hexdigest()

original_id = "Jose David Aguiar Avalos"
anonymous_id = hash_id(original_id)
print(anonymous_id)