"""
Initializing "models" module
"""
from models.engine.storage import Storage

storage = Storage()
storage.reload() # Reload objects from the database