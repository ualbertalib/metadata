class DateFinder:
    def __init__(self, tokens):
        self.word = tokens
        self.out = []
        self.output = [""]
        
    def getyear(self):
        # find all years with a 4 digit format (between 1900 and 2018)
        self.year = [i for i, w in enumerate(self.word) if re.search('^\d{4}$', w)]
        #print (self.year)
        for n,year in enumerate(self.year):
            self.out.append({'year': '', "grams": {"1-gram": "", "-1-gram": "", "2-gram": "", "-2-gram": "", "3-gram": "", "-3-gram": "", "4-gram": "", "-4-gram": "", "5-gram": "", "-5-gram": ""}})
            if int(self.word[year]) > 1900 and int(self.word[year]) < 2018:
                #index = self.word.index(year)
                self.out[n]["year"] = self.word[year]
                for j in range(1, 6):
                    # preceding grams
                    if j + year < len(self.word): 
                        self.out[n]["grams"][str(j) + "-gram"] = self.word[year + j] 
                    #succeeding grams 
                    if year - j > 0:
                        self.out[n]["grams"]["-" + str(j) + "-gram"] = self.word[year - j]
                self.output = self.out 
        if self.output[0] != '':
            return self.output
        else: 
            return None
    
    def getymonth(self):
        # find all dates with yyyy-./:mm format
        self.ymonth = [w for w in self.word if re.search('^\d{4}?[-/.//://\/]\d{2}$', w)]
        for i in self.ymonth:
            for j in ["-", ":", "/", "."]:
                if j in i:
                    self.year = ""
                    self.month = ""
                    self.year = i.split(str(j))[0]
                    self.month = i.split(str(j))[1]
                if self.year in range (1900, 2019) and self.month in range (1, 13):
                    self.output[0] = self.month + "/" + self.year
        if self.output[0] != '':
            return self.output
        else:
            return None
    
    def getyday(self):
        self.yday = [w for w in self.word if re.search('^\d{4}?[-/.//://\/]\d{2}?[/.//:/-/\/]\d{2}$', w)]
        for i in self.yday:
            for j in ["-", ":", "/", "."]:
                if j in i:
                    self.year = ""
                    self.month = ""
                    self.day = ""
                    self.year = i.split(str(j))[0]
                    self.month = i.split(str(j))[1]
                    self.day = i.split(str(j))[2]
                if self.year in range (1900, 2019) and self.month in range (1, 13) and slef.day in range (1, 32):
                    self.output[0] = self.day + "/" + self.month + "/" + self.year
        if self.output[0] != '':
            return self.output
        else:
            return None  
