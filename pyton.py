import re

def tokenize(expression):
    if expression == "": return []
    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]

class Interpreter:
    def __init__(self):
        self.vars = {}
        self.func = {}

    def funkcja(self,ciag):
        pointer=self.func[ciag[0]].index("=>")
        z=self.func[ciag[0]][0:pointer]
        w=ciag[1:]
        d=self.func[ciag[0]][pointer+1:]
        for x in z:
            while x in d: d[d.index(x)]=str(w[z.index(x)])
        return self.input("".join(d))

    def licz(self,ciag):
        znak=["fn","(",")",self.func,"%","*","/","+","-","="]
        for c in range(len(znak)):
            while znak[c] in ciag or c==3:
                if c!=3:
                    first=ciag.index(znak[c])
                    last=len(ciag)-ciag[::-1].index(znak[c])-1
                if c==0:
                    if ciag[0]=="(": raise Exception ("Tu nie wiem czemu")
                    pointer=ciag[last:].index("=>")
                    body=ciag[pointer+1:]
                    for x in body[::-1]:
                        if not x.isalpha(): body.remove(x)
                    var=ciag[last+2:pointer]
                    ile=len(var)
                    if ciag[last+1] in self.vars: raise Exception ("Funkcja nie porzyjmie nazwy zmiennej")
                    if (ile==0 and len(body)!=0) : raise Exception ("Brak zmiennych w funkcji")
                    for x in var:
                        if var.count(x)>1: raise Exception ("Duble zmiennych w funkcji")
                        if body.count(x)==0: raise Exception ("Brak zmiennych po prawej stronie")
                    if set("".join(body))!=set("".join(var)): raise Exception ("Nadmiarowe zmienne po prawej")
                    self.func[ciag[last+1]]=ciag[last+2:]
                    del ciag[last:]
                elif c>=1 and c<3:
                    x,a=0,0
                    while "("  in ciag:
                        if ciag[x]=="(":a=x
                        elif ciag[x]==")":
                            ciag[a]=self.licz(ciag[a+1:x])
                            del ciag[a+1:x+1]
                            x=-1
                        x+=1
                elif c==3:
                    for x in ciag[::-1]:
                        if x in self.func:
                            last=len(ciag)-ciag[::-1].index(x)-1
                            var=self.func[x]
                            ile=self.func[x].index("=>")
                            wyn=self.funkcja(ciag[last:last+ile+1])
                            ciag[last]=str(wyn)
                            del ciag[last+1:last+ile+1]
                    break
                elif c>3 and c<9:
                    if c in (4,5,6):
                        for d in ("%","/","*"):
                            try:first=(ciag.index(d) if ciag.index(d)<first else first)
                            except: None
                    try:
                        x=int(self.vars[ciag[first-1]] if ciag[first-1].isalpha() else int(ciag[first-1]))
                        y=int(self.vars[ciag[first+1]] if ciag[first+1].isalpha() else int(ciag[first+1]))
                    except: raise Exception("Brak parametrów w działaniu lub brak zmiennej")
                    if ciag[first]=="+": wyn=x+y
                    elif ciag[first]=="-": wyn=x-y
                    elif ciag[first]=="*": wyn=x*y
                    elif ciag[first]=="/": wyn=x/y
                    elif ciag[first]=="%": wyn=x%y
                    ciag[first-1]=str(int(wyn))
                    del ciag[first:first+2]
                elif c==9:
                    try: y=int(self.vars[ciag[last+1]] if ciag[last+1].isalpha() else int(ciag[last+1]))
                    except: raise Exception("brak drugiej zmiennej przy porównaniu")
                    if ciag[last-1].isalpha(): self.vars[ciag[last-1]]=y
                    else: raise Exception("Przyrównanie nie do zmiennej")
                    ciag[last-1]=str(y)
                    del ciag[last:last+2]

        #one or two parameters
        if len(ciag)==2: raise Exception("Tylko dwa parametry")
        elif len(ciag)==1 and (ciag[0].isalpha()==False or ciag[0] in self.vars or ciag[0]==""):
            return(ciag[0] if ciag[0].isalpha()==False else self.vars[ciag[0]])
        elif len(ciag)==0: return("")
        else: raise Exception("Jeden zły parametr")
        return(ciag)

    def input(self, expression):
        exp = tokenize(expression)
        exp=self.licz(exp)
        if exp=="": return ("")
        return int(exp)