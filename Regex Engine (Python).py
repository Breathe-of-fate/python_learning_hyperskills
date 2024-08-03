def matching(regex, text):
    if not regex:
        return True
    if not text:
        return regex == "$"
    
    if regex[0] == "\\":
        if regex[1:2] == text[0]:
            return matching(regex[2:], text[1:])
        return False

    if regex[0] not in [text[0], "."]:
        if regex[1:2] in ["?", "*"]:
            return matching(regex[2:], text)
        return False

    if regex[1:2] == "?":
        return matching(regex[2:], text[1:])
    if regex[1:2] == "*":
        return matching(regex, text[1:]) or matching(regex[2:], text)
    if regex[1:2] == "+":
        return matching(regex, text[1:]) or matching(regex[2:], text[1:])

    return matching(regex[1:], text[1:])


def start_begins(pattern, string):
    if not pattern:
        return True
    if pattern[0] == "^":
        return matching(pattern[1:], string)
    if matching(pattern, string):
        return True
    if not string:
        return pattern == "$"

    return start_begins(pattern, string[1:])

regex, text = input().split("|")
print(start_begins(regex, text))