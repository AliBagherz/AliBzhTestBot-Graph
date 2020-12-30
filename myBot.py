import requests
from time import sleep

import math
import numpy
import matplotlib.pyplot as plot

import os
import json
from flask import Flask
from flask import request
from flask import Response


url = "https://api.telegram.org/bot1477305025:AAHg-O4JTHEeFiNyRDGkbee_77SUuisQ3H0/"

app = Flask(__name__)


class StringTokenizer:
    @staticmethod
    def split(s, token=None):
        l = []
        lastINdex = 0
        i = 0
        noneToken = False
        if token == None:
            token = ' '
            noneToken = True
        while i < len(s):
            if s[i] == token[0]:
                a = 1
                ok = True
                while a < len(token):
                    if s[i+a] == token[a]:
                        a += 1
                    else:
                        ok = False
                        break
                if ok:
                    if noneToken and s[lastINdex:i] != '':
                        l.append(s[lastINdex:i])
                    elif noneToken == False:
                        l.append(s[lastINdex:i])
                    i += a
                    lastINdex = i
                else:
                    i += 1
            else:
                i += 1
            if i >= len(s):
                if noneToken and s[lastINdex:i] != '':
                    l.append(s[lastINdex:i])
                elif noneToken == False:
                    l.append(s[lastINdex:i])
        return l

    @staticmethod
    def join(l, token):
        s = ''
        for i in range(len(l)):
            s += l[i]
            if i != len(l)-1:
                s += token
        return s


class Number:
    @staticmethod
    def isNummericChar(c):
        return ((ord(c) == 46) or (48 <= ord(c) <= 57))

    @staticmethod
    def isNumber(s):
        if (len(s) > 1 and s[0] == '-') or (len(s) > 1 and s[0] == '+'):
            return True
        for i in s:
            if not((ord(i) == 46) or (48 <= ord(i) <= 57)):
                return False
        return True


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def xToList(points):
        xList = []
        for p in points:
            xList.append(p.x)
        return xList

    @staticmethod
    def yToList(points):
        yList = []
        for p in points:
            yList.append(p.y)
        return yList


class Stack:
    def __init__(self):
        self.list = []
        self.len = 0

    def push(self, val):
        self.list.append(val)
        self.len += 1

    def peek(self):
        return (self.list[-1])

    def pop(self):
        a = 0
        if (self.len != 0):
            a = self.peek()
            self.list.pop()
            self.len -= 1
        return a

    def isEmpty(self):
        return (self.len == 0)

    def print(self):
        list_str = ''
        for i in self.list:
            if len(str(i)) > 1:
                list_str += (str(round(float(i), 2)) + ' ')
            else:
                list_str += (str(i) + ' ')
        print('the last state of our stack:', list_str)


class Expression:
    def __init__(self, exp, option):
        self.stack = Stack()
        self.exp = exp
        self.option = option
        self.postFixList = []
        self.postFix = ''
        self.precedence = {'+': 1, '-': 1, '*': 2,
                           '/': 2, '^': 3, '!': 3}

    def isOperand(self, ch):
        return (ch.isalpha() or ch.isdigit())

    def notGreater(self, i):
        try:
            a = self.precedence[i]
            b = self.precedence[self.stack.peek()]
            return True if a <= b else False
        except KeyError:
            return False

    def infixToPostfix(self):
        fastView = False

        def print_check(c, exp):
            if self.option == 1:
                print()
                if (c != None):
                    print(
                        'reading {', c, '} from the inputed infix function: ', exp, sep='')
                else:
                    print(
                        'making stack empty after reading all of the chars in infix function :)')
                self.stack.print()
                print('the last state of out postFix function:',
                      *(self.postFixList))
                if not(fastView):
                    input('press Enter to continue : ')

        self.exp = self.exp.replace(' ', '')

        if self.exp[:2] == 'y=':
            self.exp = self.exp[2:]

        for i in range(len(self.exp) - 1):
            if (self.exp[i+1].lower() == 'x' and self.exp[i].isdigit()) or (self.exp[i+1] == '(' and self.exp[i].isdigit()):
                self.exp = self.exp[:i+1] + '*' + self.exp[i+1:]

        if self.option == 1:
            print('the inputed function in infix form:', self.exp)
            inp = input(
                'write f and Enter for fastView or just Enter to view the information slowly: ')
            if inp == 'f':
                fastView = True

        i = 0
        while i < len(self.exp):
            if self.isOperand(self.exp[i]):
                if self.exp[i].isdigit():
                    a = i+1
                    while a < len(self.exp):
                        if Number.isNummericChar(self.exp[a]):
                            a += 1
                        else:
                            break
                    self.postFixList.append(self.exp[i:a])
                    print_check(self.exp[i:a], self.exp)
                    i = a
                else:
                    self.postFixList.append(self.exp[i])
                    print_check(self.exp[i], self.exp)
                    i += 1
            elif self.exp[i] == '(':
                self.stack.push(self.exp[i])
                print_check(self.exp[i], self.exp)
                i += 1
            elif self.exp[i] == ')':
                while((not self.stack.isEmpty()) and
                      self.stack.peek() != '('):
                    a = self.stack.pop()
                    self.postFixList.append(a)
                    print_check(self.exp[i], self.exp)
                self.stack.pop()
                print_check(self.exp[i], self.exp)
                i += 1
            else:
                while(not self.stack.isEmpty() and self.notGreater(self.exp[i])):
                    self.postFixList.append(self.stack.pop())
                    print_check(self.exp[i], self.exp)
                self.stack.push(self.exp[i])
                print_check(self.exp[i], self.exp)
                i += 1

        while not self.stack.isEmpty():
            self.postFixList.append(self.stack.pop())
            print_check(None, None)

    def calculator(self, x):
        fastView = False
        tempStr = StringTokenizer.join(self.postFixList, '__')
        listExp = StringTokenizer.split(tempStr, '__')
        if self.option == 1:
            print()
            print('x =', round(x, 2))
            inp = input(
                'write f and Enter for fastView or just Enter to view the information slowly: ')
            if inp == 'f':
                fastView = True
        for i in range(len(listExp)):
            if listExp[i].lower() == 'x':
                listExp[i] = str(x)
        resultStack = Stack()

        def print_check_calculator(c):
            if self.option == 1:
                print()
                list_str = ''
                for i in listExp:
                    if len(i) > 1:
                        list_str += (str(round(float(i), 2)) + ' ')
                    else:
                        list_str += (i + ' ')
                if (len(c) > 1):
                    print('reading {', round(float(c), 2),
                          '} from our postFix expression: ', list_str)
                else:
                    print(
                        'reading {', c, '} from our postFix expression: ', list_str)
                if not(fastView):
                    input('press Enter to continue : ')

                resultStack.print()
        for i in range(len(listExp)):
            if Number.isNumber(listExp[i]):
                resultStack.push(listExp[i])
                print_check_calculator(listExp[i])
            else:
                if listExp[i] == '+':
                    if resultStack.len >= 2:
                        a = float(resultStack.pop())
                        b = float(resultStack.pop())
                        resultStack.push(a+b)
                        print_check_calculator(listExp[i])
                if listExp[i] == '-':
                    if resultStack.len >= 2:
                        a = float(resultStack.pop())
                        b = float(resultStack.pop())
                        resultStack.push(b-a)
                        print_check_calculator(listExp[i])
                    elif resultStack.len == 1:
                        a = float(resultStack.pop())
                        resultStack.push(-a)
                        print_check_calculator(listExp[i])
                if listExp[i] == '^':
                    a = float(resultStack.pop())
                    b = float(resultStack.pop())
                    resultStack.push(b**a)
                    print_check_calculator(listExp[i])
                if listExp[i] == '*':
                    a = float(resultStack.pop())
                    b = float(resultStack.pop())
                    resultStack.push(b*a)
                    print_check_calculator(listExp[i])
                if listExp[i] == '/':
                    a = float(resultStack.pop())
                    b = float(resultStack.pop())
                    resultStack.push(b/a)
                    print_check_calculator(listExp[i])
                if listExp[i] == '!':
                    a = int(float(resultStack.pop()))
                    resultStack.push(float(math.factorial(a)))
                    print_check_calculator(listExp[i])
        res = resultStack.pop()
        if self.option == 1:
            print()
            print('x =', round(x, 2), '-- y =', round(res, 2))
            input('press Enter to continue : ')
        return res


def isValidExpression(exp):
    if len(exp) > 30 or exp.count('x') > 7:
        return False
    list_mojaz = ['x', '^', ' ', '!', '+', '(', ')', '-', '/', '*', 'y', '=']
    for i in exp:
        if i not in list_mojaz and not i.isdigit():
            return False
    return True


def doPlot(exp, a, b, step, chat_id):
    option = 0
    ex = Expression(exp, option)
    ex.infixToPostfix()

    points = []
    i = a
    while i <= b:
        x = i
        y = ex.calculator(i)
        point = Point(x, y)
        points.append(point)
        i += step
    plot.clf()
    plot.plot(
        Point.xToList(points),  # liste x ha
        Point.yToList(points),  # liste y ha
        linestyle='solid',
        linewidth=2,
        markersize=8,
        marker='.',
        color='yellow',
        markerfacecolor='red'
    )
    plot.xlim(a, b)
    plot.title('AliBaBot')
    plot.xlabel('x Axix')
    plot.ylabel('y Axix')
    plot.savefig(chat_id + '.png', facecolor='w', edgecolor='w',
                 orientation='portrait', pad_inches=0.1,)


def get_updates_json(request, offset=None):

    response = requests.get(request + 'getUpdates',
                            data={'timeout': 100, 'offset': offset})

    return response.json()


def last_update(data):

    results = data['result']

    total_updates = len(results) - 1

    return results[total_updates]


def get_chat_id(update):

    chat_id = update['message']['chat']['id']

    return chat_id


def send_mess(chat, text):

    params = {'chat_id': chat, 'text': text}

    response = requests.post(url + 'sendMessage', data=params)

    return response


def send_photo(chat, photo):
    chat_id_dic = {'chat_id': chat}
    photo_dic = {'photo': photo}

    response = requests.post(
        url + 'sendPhoto', data=chat_id_dic, files=photo_dic)

    return response


def write_json(data, fileName='response.json'):
    with open(fileName, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def read_json(fileName='response.json'):
    with open(fileName, 'r') as f:
        dic = json.load(f)
    return dic


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id = str(msg['message']['chat']['id'])
        messageText = msg['message'].get('text', '')
        if messageText == '':
            pass
        elif messageText == '/func':
            send_mess(chat_id, '''
            give me the function in one of these formats
        y = 3x^2 + 17x - 2!
        3x^2 + (17x + 2) - 2!
        ''')
            olderCommands = read_json()
            olderCommands[chat_id] = []
            olderCommands[chat_id].append(messageText)
            write_json(olderCommands)
            # doPlot(messageText)
            # send_photo(chat_id, open('aks.png', 'rb'))
        else:
            olderCommands = read_json()
            print(olderCommands)
            print(chat_id)
            lst = olderCommands.get(chat_id)
            print(lst)
            print(isinstance(lst, list))
            if isinstance(lst, list):
                print(len(lst))
            if not isinstance(lst, list):
                send_mess(chat_id, '''
                    please choose your command at first
                    example: /func
                ''')
            elif len(lst) == 0:
                send_mess(chat_id, '''
                    please choose your command at first
                    example: /func
                ''')
            else:
                if len(lst) == 1:
                    try:
                        if not isValidExpression(messageText):
                            raise ValueError()
                        ex = Expression(messageText, 0)
                        ex.infixToPostfix()
                        olderCommands[chat_id].append(messageText)
                        write_json(olderCommands)
                        send_mess(chat_id, '''
                            please enter the starting point
                        ''')
                    except:
                        send_mess(chat_id, '''
                            not a valid function
                        ''')
                        olderCommands.pop(chat_id)
                        write_json(olderCommands)
                elif len(lst) == 2:
                    try:
                        a = float(messageText)
                        olderCommands[chat_id].append(messageText)
                        write_json(olderCommands)
                        send_mess(chat_id, '''
                            pleese choose the ending point
                        ''')
                    except:
                        send_mess(chat_id, '''
                            not a valid number
                        ''')
                        olderCommands.pop(chat_id)
                        write_json(olderCommands)
                elif len(lst) == 3:
                    try:
                        a = float(messageText)
                        olderCommands[chat_id].append(messageText)
                        write_json(olderCommands)
                        send_mess(chat_id, '''
                            pleese choose the step
                        ''')
                    except:
                        send_mess(chat_id, '''
                            not a valid number
                        ''')
                        olderCommands.pop(chat_id)
                        write_json(olderCommands)
                elif len(lst) == 4:
                    try:
                        step = float(messageText)
                        func = olderCommands[chat_id][1]
                        a = float(olderCommands[chat_id][2])
                        b = float(olderCommands[chat_id][3])
                        if (b-a)/step > 30 or step <= 0 or a >= b:
                            raise ValueError()
                        doPlot(func, a, b, step, chat_id)
                        send_photo(chat_id, open(chat_id + '.png', 'rb'))
                        olderCommands.pop(chat_id)
                        write_json(olderCommands)
                    except:
                        send_mess(chat_id, '''
                            not a valid step
                        ''')
                        olderCommands.pop(chat_id)
                        write_json(olderCommands)
        return Response('ok', status=200)
    else:
        return "<h1>salam karbar</h1>"


if __name__ == "__main__":
    olderCommands = {}
    write_json(olderCommands)
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    #app.run(debug=True, port=5000)
