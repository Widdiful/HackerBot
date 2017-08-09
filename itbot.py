import random, inflect, re

# initialise literal magic
p = inflect.engine()

def makeWord():
    # creates randomly generated jargon
    with open("prefix.txt") as f:
        prefix = [x.strip('\r\n') for x in f.readlines()]
    with open("suffix.txt") as f:
        suffix = [x.strip('\r\n') for x in f.readlines()]
    with open("letters.txt") as f:
        letters = [x.strip('\r\n') for x in f.readlines()]

    if random.randint(0,2) == 0:
        # acronym jargon
        result = ""
        for x in range(0, random.randint(3,4)):
            result += random.choice(letters)
        
        # random lowercase vowels for extra computer
        for x in range(1, len(result) - 1):
            if random.randint(0,1) == 0:
                if result[x] in "AEIOU":
                    result = result[:x] + result[x].lower() + result[x+1:]
                    break
        
        # add jargon suffix
        if random.randint(0,1) == 0:
            result += " " + random.choice(suffix).title()
    else:
        # proper noun jargon
        if random.randint(0,2) == 0:
            result = random.choice(prefix) + " " + random.choice(suffix).title()
        else:
            result = random.choice(prefix) + random.choice(suffix).title()
    result = result.replace("  "," ").replace("i ", "i").replace("- ", "-").replace("Mal ", "Mal")
    return result
    
def doVerbs(str):
    # replaces verb/swear tags with randomly selected verbs, conjugated correctly
    with open("verbs.txt") as f:
        verbs = [x.strip('\r\n') for x in f.readlines()]
    verbs.pop(0)
    with open("swears.txt") as f:
        swears = [x.strip('\r\n') for x in f.readlines()]
    verbs.pop(0)
    punct = [".", ",", "!"]
    p = inflect.engine()
    
    # regex shit i dont fucking know
    rep = {"VERBd": random.choice(verbs).split("|")[0], "VERBed": random.choice(verbs).split("|")[1], "VERBs": random.choice(verbs).split("|")[2], "VERBobj": random.choice(verbs).split("|")[3], "VERBing": random.choice(verbs).split("|")[4], "VERBn": random.choice(verbs).split("|")[5], "SWEARd": random.choice(swears).split("|")[0], "SWEARed": random.choice(swears).split("|")[1], "SWEARs": random.choice(swears).split("|")[2], "SWEARing": random.choice(swears).split("|")[3]}
    result = str.replace("a VERBn", p.a(random.choice(verbs).split("|")[5]))
    
    pattern = re.compile("|".join(rep.keys()))
    result = pattern.sub(lambda m: rep[re.escape(m.group(0))], result)
    result = result.replace(".", random.choice(punct))
    return result
    
while True:
    with open("sentences.txt") as f:
        sentences = [x.strip('\r\n') for x in f.readlines()]
    phrase = ""
    hasNoun = False
    sentencesNo = random.randint(1, 3)
    
    # generates random number of clauses/sentences
    for i in range(0, sentencesNo):
        curSentence = random.choice(sentences)
        
        # ensures that at least the first sentence has a noun to avoid boring results
        while not "NOUN" in curSentence and hasNoun == False and i == sentencesNo - 1:
            curSentence = random.choice(sentences)
        sentences.remove(curSentence)
        if "NOUN" in curSentence:
            hasNoun = True
        
        # replace tags and generates punctuation
        for word in curSentence.split():
            curSentence = curSentence.replace("NOUNa", p.a(makeWord()), 1)
            curSentence = curSentence.replace("NOUNd", makeWord(), 1)
        curSentence = doVerbs(curSentence)
        if phrase.endswith(", "):
            phrase += curSentence + " "
        else:
            phrase += curSentence[0].upper() + curSentence[1:] + " "
    phrase = (phrase + "#").replace(", #", ".").replace("#", "")
    print phrase