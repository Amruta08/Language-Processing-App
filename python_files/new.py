import language_tool_python
tool = language_tool_python.LanguageTool('en-US')
text = 'A sentence with a error in the Hitchhiker’s Guide tot he Galaxy'
matches = tool.check(text)
error_messages = []

for obj in matches:
    start = int(obj.offset)
    end = int(obj.offset + obj.errorLength)
    a = f'{obj.message} in "{text[start:end]}"'
    error_messages.append(a)

for msg in error_messages:
    print(msg)

# >>> tool.close() # Call `close()` to shut off the server when you're done.

new_text = tool.correct(text)
print(new_text)
'A sentence with an error in the Hitchhiker’s Guide to the Galaxy'
