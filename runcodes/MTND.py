
class MTND:
    def __init__(self):
        self.states = []
        self.entryAlphabet = []
        self.stackAlphabet = []
        self.transitions = dict()
        self.testWords = []
        self.finalStates = []
        self.transitionStack = []
        self.leftLimit = ''
        self.white = ''
        self.initialState = ''

    def createTransitions(self, trans):
        pair = trans[0]+trans[1]
        if(pair in self.transitions):
            self.transitions[pair] = self.transitions[pair] + \
                [[trans[2], trans[3], trans[4]]]
        else:
            newTransition = {
                trans[0]+trans[1]: [[trans[2], trans[3], trans[4]]]}
            self.transitions.update(newTransition)

    def readTransitions(self, num):
        for i in range(0, num):
            trans = input().split()
            self.createTransitions(trans)

    def write(self, tape, char, register):
        newTape = tape.copy()
        newTape[register] = char
        return newTape

    def move(self, tape, register, direction):
        if(direction == 'E'):
            if(register == 0):
                return register
            return register - 1
        elif(direction == 'D'):
            if(len(tape)-1 == register):
                tape.append(self.white)
            return register + 1
        elif(direction == 'I'):
            return register

    def validateTransition(self, currState, tape, register, transitionStack):
        stop = True
        readedChar = tape[register]
        if((currState+readedChar) in self.transitions):
            stop = False
            pairs = self.transitions.get(currState+readedChar)
            for pair in pairs:
                newRegister = self.move(tape, register, pair[2])
                transitionStack.append([pair[0], self.write(
                    tape, pair[1], register), newRegister])

        return stop

    def isAccepted(self, state, stop):
        if(stop and state in self.finalStates):
            return True
        else:
            return False

    def readTransitionStack(self, word, initialState):
        tape = list(word)
        tape.insert(0, self.leftLimit)
        tape.append(self.white)
        self.transitionStack = [[initialState, tape, 1]]
        accepted = False
        while (not (len(self.transitionStack) == 0)):
            newTransitionStack = []
            for pilha in self.transitionStack:
                stop = self.validateTransition(
                    pilha[0], pilha[1], pilha[2], newTransitionStack)
                if(self.isAccepted(pilha[0], stop)):
                    accepted = True
                    break

            if(accepted):
                break
            self.transitionStack = newTransitionStack

        if(accepted):
            print('S')
        else:
            print('N')


def testMT(MT):
    for words in MT.testWords:
        MT.readTransitionStack(words, MT.initialState)


def createMT():
    MT = MTND()
    MT.states = input()
    MT.entryAlphabet = input()
    MT.stackAlphabet = input()
    MT.leftLimit = input()
    MT.white = input()
    numOfTransitiosn = int(input())
    MT.readTransitions(numOfTransitiosn)
    MT.initialState = input()
    MT.finalStates = input().split()
    MT.testWords = input().split()

    return MT


MT = createMT()
testMT(MT)
