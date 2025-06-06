# run interactively or in a script
from client import send_note
send_note("alice", "http://localhost:9001", "http://localhost:9002/actor/bob", "Hello Bob!")
send_note("bob", "http://localhost:9002", "http://localhost:9001/actor/alice", "Hi Alice!")
