from dataclasses import dataclass
import pickle
from random import random


class Word:
    def __init__(self, memory, name, links=None):
        self.links = [];
        if links:
            self.links = links
        self.memory = memory;
        self.name = name;

    def append(self, link):
        if isinstance(link, Word):
            for i in link.links:
                self.append(i);
        elif isinstance(link, WordLink):
            self.delDupe(link.id);
            self.links.append(link);
        else:
            raise Exception("Cannot Append This Object to Word")

    def vAdd(self, value, words):
        for i in self.links:
            if i.other in words:
                i.weight += value;
                if i.weight > 1.9:
                    i.weight = 1.9;
                elif i.weight < 0.1:
                    i.weight = 0.1;

    def delDupe(self, id):
        for i in self.links:
            if i.id == id:
                self.links.remove(i);

    def toId(self):
        names = [];
        for i in self.links:
            names.append(i.id);
        return names;

    def toName(self):
        names = [];
        for i in self.links:
            names.append(i.other.name);
        return names;

    def new(self, other):
        weights = [];
        for i in self.links:
            weights.append(i.weight);
        weight = self.memory.avg(weights);
        self.links.append(WordLink(self, other, weight));
        return self

    def toWeight(self, words):
        weights = [];
        word = [];
        for a in words:
            word.append(a.name);
        for i in words:
            if i.name not in self.toName():
                self.new(i);
        for i in self.links:
            if i.other.name in word and i.other.name != self.name:
                # print(i);
                weights.append(i.weight);
        return weights;

    def find(self, name):
        link = None
        for i in self.links:
            if i.id == name:
                link = i;
        return link

    def copy(self):
        return Word(self.memory, self.name, self.links);


@dataclass()
class WordLink:
    origin: vars
    other: vars
    weight: float = 1.0

    def __post_init__(self):
        self.id = f"[{self.origin.name}]:[{self.other.name}]";

    def set(self, this):
        self.origin = this;
        return self;

    def copy(self):
        return WordLink(self.origin, self.other);

    def __repr__(self):
        return f"\t({self.id}:[{self.weight}])";


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

    def find(self, wordName):
        word = None;
        for i in self.words:
            if i.name == wordName:
                word = i;
        return word;

    def vAdd(self, value):
        for i in self.words:
            i.vAdd(value, self.words);

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
            for a in i.toWeight(self.words):
                weights.append(a);
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
        raw = inpit.lower().strip("?").split(";")[0].split(" ");
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
        avg = self.avg(weights);
        trueRan = random();
        if trueRan < 0.1:
            trueRan = 0.1;
        comp = trueRan * avg;
        print(f"\taverage[{avg}] random[{trueRan}] final[{comp}]")
        comp = round(comp);
        return comp;

    def avg(self, num):
        out = 0;
        for i in num:
            out += i;
        try:
            out /= len(num);
        except:
            out = 1.0
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
