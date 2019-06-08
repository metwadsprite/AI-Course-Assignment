def hash(name):
    return 1 + (sum(ord(c) for c in name) % 4)


print(hash('VASILESCUVLAD'))