def load_synonym_file(path):

    syn_list = []
    with open(path, 'r') as f:
        for line in f.readlines():
            syn_list.append(line)

    print("synonyms file loaded...")

    return syn_list