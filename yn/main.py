from memory import Memory


def train(rounds):
    trainer = Memory().load();
    data = open("training.dat").read().split("\n");

    for i in range(rounds):
        for a in data:
            trainer.train(a);
            trainer.store();


def run():
    while True:
        mem = Memory().load();
        inpit = input("yna>");
        print(mem.parse(inpit));
        mem.store();


if __name__ == "__main__":
    train(100);
