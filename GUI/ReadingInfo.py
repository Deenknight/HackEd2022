
class ReadingInfo:

    def save(self, title="pee", page="2", chapter="2"):
        file = open('info.txt', 'r')
        fileRead = file.read()
        int = fileRead.find(title)
        if int == -1:
            file = open('info.txt', 'a')
            file.write(f"\n{title}-{page}-{chapter}")

        file.close()

    def load(self, title="piss"):
        file = open('info.txt', 'r')
        read_file = file.read()
        list = read_file.split('\n')
        for line in list:
            if title in line:
                string = line

        self.title = string.split('-')[0]
        self.page = string.split('-')[1]
        self.chapter = string.split('-')[2]

        file.close()


if __name__ == "__main__":
    test = ReadingInfo()
    test.save()
    test.load()
