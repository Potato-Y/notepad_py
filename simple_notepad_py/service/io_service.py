class IOService():

    def open(path: str):
        file = open(path, 'r')

        data = file.read()
        print(data)

        file.close()

        return data

    def save(path: str, data: str):
        file = open(path, 'w')
        file.write(data)
        file.close()
