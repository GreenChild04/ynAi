from memory import Memory
from tqdm import tqdm;


def train(rounds):
    trainer = Memory().load();
    bar = tqdm(total=rounds, position=0);
    bar.set_description("Training ai with data...");
    data = open("training.dat").read().split("\n");

    for i in range(rounds):
        bar.update()
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
    run()
