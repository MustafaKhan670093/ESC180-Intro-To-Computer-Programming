
def get_phone_dict():
    s = open("phones.txt", encoding = "utf-8").read()
    lines = s.split("\n")
    ph_class_dict = {}
    for line in lines:
        if len(line) < 3:
            continue
        phone, ph_class = line.split("\t")
        ph_class_dict[phone] = ph_class
        
    return ph_class_dict
        

def strip_away_digits(s):
    s1 = ""
    for c in s:
        if not c.isdigit():
            s1 += c
    return s1
    
def get_phone_class(s, ph_class_dict):
    if ph_class_dict[strip_away_digits(s)] == "vowel":
        return "vowel"
    else:
        return "cons"

def get_phone_classes(phones, ph_class_dict):        
    res = []
    for ph in phones:
        res.append(get_phone_class(ph, ph_class_dict))
    return res
    
def count_syllables(vc):
     #("cons"+"".join(get_phone_classes(L, ph_class_dict))).count("consvowel")
    #flag = False
    cur_run_v = 0
    count = 0
    for a in vc:
        if a == "vowel":
            if cur_run_v == 0:
                count += 1
            #flag = True
            cur_run_v += 1
        else:
            #flag = False
            cur_run_v = 0
    return count
            

def get_syl_count(ph_class_dict):
    s = open("dict.txt", encoding = "utf-8").read()
    lines = s.split("\n")[126:]
    
    syl_count = {}
    
    for line in lines:
        if len(line) < 2:
            continue
            
        words = line.split()
        syl_count[words[0].lower()] = count_syllables(get_phone_classes(words[1:], ph_class_dict))

    return syl_count
    
def get_total_words(text):
    return len(text.split())    

def get_total_sentences(text):
    text = text.replace("!", ".")
    text = text.replace("?", ".")
    sentences = text.split('.')    
    return len(sentences)
    
def get_total_syllables(text, syl_count):
    words = text.split()
    total = 0
    for word in words:
        w = word.lower().strip("-,;")
        total += syl_count.get(w, 2)
    return total
        
def grade_level(filename, syl_count):
    text = open(filename, encoding="utf-8").read()
    total_words = get_total_words(text)
    total_sentences = get_total_sentences(text)
    total_syllables = get_total_syllables(text, syl_count)
    return .39*(total_words/total_sentences)+11.8*(total_syllables/total_words)-15.59
    
if __name__ == '__main__':
    import os
    os.chdir("/home/guerzhoy/Desktop/CSC180_2015/labs/lab08")
    
    ph_class_dict = get_phone_dict()
    syl_count = get_syl_count(ph_class_dict)
    print(grade_level("engsci.txt", syl_count))