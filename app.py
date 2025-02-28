import cmd
import json

class GymApp(cmd.Cmd):
    intro = 'Welcome to the Gym App. Type help or ? to list commands.\n'
    prompt = '(gym) '
    file = None

    def __init__(self):
        super().__init__()
        self.data = []
        self.load_data()

    def load_data(self):
        try:
            with open('data.json', 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = []

    def save_data(self):
        with open('data.json', 'w') as f:
            json.dump(self.data, f, indent=4)

    def do_add(self, arg):
        'Add a new entry: add <name> <description>'
        args = arg.split()
        if len(args) != 2:
            print('Usage: add <name> <description>')
            return
        name, description = args
        self.data.append({'name': name, 'description': description})
        self.save_data()
        print(f'Added: {name}')

    def do_list(self, arg):
        'List all entries'
        if not self.data:
            print('No entries found.')
            return
        for i, entry in enumerate(self.data):
            print(f'{i+1}. {entry["name"]}: {entry["description"]}')

    def do_edit(self, arg):
        'Edit an entry: edit <index> <name> <description>'
        args = arg.split()
        if len(args) != 3:
            print('Usage: edit <index> <name> <description>')
            return
        try:
            index = int(args[0]) - 1
            name, description = args[1], args[2]
            if 0 <= index < len(self.data):
                self.data[index]['name'] = name
                self.data[index]['description'] = description
                self.save_data()
                print(f'Edited entry {index+1}')
            else:
                print('Invalid index.')
        except ValueError:
            print('Invalid index.')

    def do_delete(self, arg):
        'Delete an entry: delete <index>'
        try:
            index = int(arg) - 1
            if 0 <= index < len(self.data):
                del self.data[index]
                self.save_data()
                print(f'Deleted entry {index+1}')
            else:
                print('Invalid index.')
        except ValueError:
            print('Invalid index.')

    def do_exit(self, arg):
        'Exit the application.'
        self.save_data()
        print('Thank you for using the Gym App!')
        return True

    def do_EOF(self, line):
        return self.do_exit(line)

if __name__ == '__main__':
    GymApp().cmdloop()
