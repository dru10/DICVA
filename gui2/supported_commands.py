import pickle
import globals

supported_commands = [
    {
        'name': 'hello',
        'description': 'Greets the user',
        'type': 'conversation',
        'handler': f"Hello there {globals.username}, happy to hear from you!"
    },
    {
        'name': 'stop',
        'description': 'Stops the program from listening',
        'type': 'conversation',
        'handler': f"Goodbye"
    },
]

outfile = 'mydata.data'
fw = open(outfile, 'wb')
pickle.dump(supported_commands, fw)
fw.close()

fd = open(outfile, 'rb')
stored_commands = pickle.load(fd)
print(stored_commands)
