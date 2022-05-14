# Máquina de Turing Não Deterministica

**Aluno** : Jordan Silva Oliveira

### Introdução

Se trata de um dispositivo imaginário e concebido por Alan Mathinson Turing e publicada pela primeira vez em 1936, hoje aceita como a estutura básica para fundamentar a ciência da computação moderna e a computabilidade. Tal feito deu a Turing o título símbolico de "pai da computação".
A máquina de turing é capaz de ler, escrever e apagar símbolos binários em uma fita de comprimento limitado e dividida por quadros de igual tamanho. Uma cabeça de leitura/gravação que se moveria em qualquer direção ao longo da fita, um quadro por vez, e uma unidade d eocntrole poderia interpretar uma lista de instruções simples, movendo-se para a direita ou esquerda.

### Projeto e Implementação do Algoritmo

O algoritmo foi desenvolido usando como base algoritmos criados em atividades anteriores, utilizando uma estrutura de classe e métodos, assim como duas funções auxiliares para a testagem e construção da classe. Como parte dos requisitos desse trabalho a implementação de um sistema que quantifique o tempo gasto ao se processar cada uma das tPalavras de teste, assim a biblioteca *tempo* nativa do *python* foi importada e usada nas linhas de 95 e 97.
O código foi estruturado na seguinte ordem, a classe *MTND* é declarada, em seguida seus atributos são declarados, atributos esses que serão inseridos pelo usuário ao executar o algoritmo. Na sequência um método responsável por alimentar um *dicionário* nomeado como *transitions*, em seguida um outro método com nome *readTransitions* tem como função percorrer o *dicionario*, seguinte um outro método faz a escrita na fita, outro realiza a operação de movimento, ambos possuem identificadores autoexplicativos. Então realizamos a validação da transição por meio do método *validadeTransition* e finalizamos com dois métodos quem trabalham em conjunto, um lendo a uma pilha de transições e outro verificando a aceitação das tPalavras lidas.

### Metodologia

Buscando atender os requisitos exigidos para a correta realização deste trabalho, um experimento empírico foi conduzido como forma de coletar dados sobre a performance do algoritmo em relação ao tamanho das palavras testadas pelo mesmo, sendo assim o código do mesmo foi então adaptado para ler dados por meio de um arquivo nomeado *data.json*, desse modo os testes poderiam ser então realizados de forma mais fácil e economica em termos de tempo, então foram testadas as seguintes palavras:

- *
- a
- ab
- abb
- aabb
- aaabb
- aaabbb
- aaaabbbb
- ababababa
- abababababa
- aaaaaaabbbbbbbb
- aaaaaaaaaabbbbbbbbbb
- aaaaaaaaaaaaabbbbbbbbbbbbb
- aaaaaaaaaaaaaaabbbbbbbbbbbbbbb

Então o tempo percorrido para cada palavra foi então armazenado em um arquivo chamado *data.csv* e por meio da biblioteca Panda, gráficos foram gerados, tais gráficos podem ser encontrados no decorrer deste relatório. O código usado para gerar os gráficos foi encontrado encontrado já pronto em plataformas online e precisou apenas de mínimas modificações, estando este também presente no relatório.

### Resultados e Conclusões

Com a ajuda dos gráficos podemos aferir que à medida em que o tamanho da palavra cresce, o tempo gasto no seu processamento apresenta uma tendência exponencial, é necessário considerar que discrepâncias encontradas nas medidas podem ser jusificadas por tal processamento ocorrer em uma máquina não otimizada e que possui outras tarefas em paralelo, podendo entregar resultados diferentes para cada iteração, dito isto os dados de tempo de execução foram armazenados em um arquivo *.csv* que se encontra neste repositório.

```python
import pandas as pd

import matplotlib.pyplot as plt
from   sklearn.linear_model import LinearRegression
from   sklearn.metrics import r2_score

dataFile = pd.read_csv('data.csv', decimal=',', error_bad_lines=False)

plt.figure(figsize = (16,8))
plt.scatter(
    dataFile['tPalavra'], 
    dataFile['tempo'], 
    c='red')
plt.xlabel("Tamanho da Palavra")
plt.ylabel("Tempo de Execução (s)")

plt.show()

x = dataFile['tPalavra'].values.reshape(-1,1)
y = dataFile['tempo'].values.reshape(-1,1)
reg = LinearRegression()
reg.fit(x, y)

f_previsoes = reg.predict(x)

plt.figure(figsize = (16,8))
plt.scatter(
    dataFile['tPalavra'], 
    dataFile['tempo'], 
    c='red')

plt.plot(
    dataFile['tPalavra'],
    f_previsoes,
    c='blue',
    linewidth=3,
    linestyle=':'
)

plt.xlabel("Tamanho da Palavra")
plt.ylabel("Tempo de Execução (ms)")

plt.show()
```

```
/home/jordan/anaconda3/lib/python3.9/site-packages/IPython/core/interactiveshell.py:3444: FutureWarning: The error_bad_lines argument has been deprecated and will be removed in a future version.


  exec(code_obj, self.user_global_ns, self.user_ns)
```

![png](/Report/Report/output_1_1.png?msec=1652535069809)

![png](/Report/Report/output_1_2.png?msec=1652535069809)

```python
import time


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
            for stack in self.transitionStack:
                stop = self.validateTransition(
                    stack[0], stack[1], stack[2], newTransitionStack)
                if(self.isAccepted(stack[0], stop)):
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
        start_timer = time.perf_counter()
        MT.readTransitionStack(words, MT.initialState)
        print(" %s" % ((time.perf_counter() - start_timer)*1000.0))


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
```
