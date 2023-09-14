class IOService():

    def open(path: str):
        file = open(path, 'r')

        data = file.read()
        print(data)

        file.close()

        return data
