import re, time

# this script prints overtop the previous text (over multiple lines)


class BlockPrinter:
    def __init__(self):
        self.num_lines = 0
        self.max_line_width = 0

    def clear(self):
        for _ in range(self.num_lines):
            print('\x1b[A' + '\r' + ' '*self.max_line_width + '\r', end='')

    def print(self, text, end='\n'):

        # Clear previous text by overwriting non-spaces with spaces
        self.clear()

        # Print new text
        text += end
        print(text, end='')
        self.num_lines = text.count('\n')
        self.max_line_width = max(map(
            lambda line : len(line), text.split('\n')
        ))

# # TEST

# bp = BlockPrinter()

# bp.print('Foobar\nBazbar')
# time.sleep(3)

# bp.print('Foo\nBar')
# time.sleep(3)

# bp.print('Ayyyyyy')

