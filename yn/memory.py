from dataclasses import dataclass
import pickle
from random import random


@dataclass()
class Word:
    memory: vars;
    name: str;
    weight: float = 1.0;

    def copy(self):
        return Word(self.memory, self.name, self.weight);


@dataclass()
class WordLink:
    origin: vars
    other: vars

    def set(self, this):
        self.origin = this;
        return self;

    def copy(self):
        return WordLink(self.origin, self.other);


class WordList:
    def __init__(self):
        self.words = [];
        # self.wordLink = WordLink().set(self);

    def append(self, word):
        if isinstance(word, WordList):
            for i in word.words:
                self.append(i);
        elif isinstance(word, Word):
            self.delDupe(word.name);
            self.words.append(word);
        else:
            raise Exception("Cannot Append Non WordType Object!");

    def vAdd(self, value):
        for i in self.words:
            i.weight += value;

    def find(self, wordName):
        word = None;
        for i in self.words:
            if i.name == wordName:
                word = i;
        return word;

    def delDupe(self, name):
        for i in self.words:
            if i.name == name:
                self.words.remove(i);

    def toName(self):
        names = [];
        for i in self.words:
            names.append(i.name);
        return names;

    def toWeight(self):
        weights = [];
        for i in self.words:
            weights.append(i.weight);
        return weights;

    def inherit(self, other, names=None):
        if names:
            words = [];
            for i in names:
                words.append(other.find(i));
            self.words = words;
        else:
            self.words = other.words;


class Memory:
    def __init__(self):
        self.words = WordList();

    def parse(self, inpit):
        raw = inpit.lower().strip("?").split(" ");
        words = self.generate(raw);
        out = self.randomise(words);
        if out == 1:
            return "Yes";
        else:
            return "No";

    def train(self, inpit):
        raw = inpit.lower().strip("?").split(" ");
        real = int(inpit.strip(" ").split(";")[1])
        words = self.generate(raw);
        out = self.randomise(words);
        if out != real:
            if out > real:
                words.vAdd(-0.1);
            elif out < real:
                words.vAdd(0.1);

    def generate(self, raw):
        listOfNames = self.words.toName();

        currentWords = WordList();
        for i in raw:
            if i not in listOfNames:
                currentWords.append(Word(self, i));
            else:
                currentWords.append(self.words.find(i))

        self.words.append(currentWords);
        return currentWords;

    def randomise(self, words):
        weights = words.toWeight();
        print(weights)
        avg = self.avg(weights);
        trueRan = random();
        comp = trueRan * avg;
        comp = round(comp);
        return comp;

    def avg(self, num):
        out = 0;
        for i in num:
            out += i;
        out /= len(num);
        return out

    def store(self):
        with open("memory.cfg", "wb+") as file:
            pickle.dump(self, file);

    def load(self):
        try:
            with open("memory.cfg", "rb") as file:
                return pickle.load(file);
        except:
            return self
