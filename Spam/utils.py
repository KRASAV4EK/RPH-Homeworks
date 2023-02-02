# Make dict from !truth.txt or !prediction.txt
def read_classification_from_file(file):
    f = open(file, 'r', encoding='UTF-8')
    dictionary = {}

    # Make data structure from folder as dictionary
    for string in f:
        email = string.strip().split()
        if len(email) > 0:
            dictionary[email[0]] = email[1]

    f.close()
    return dictionary


# Create a file, using text from dict
def write_classification_to_file(file, dict):
    f = open(file, 'w+', encoding='UTF-8')
    for email in dict:
        f.write(email + ' ' + dict[email] + '\n')
    f.close()


if __name__ == '__main__':
    import os

    dir = os.path.dirname(os.path.realpath(__file__)) + '/1/!truth.txt'
    
    dict = read_classification_from_file(dir)

    print(dict)

    write_classification_to_file('test.txt', dict)
