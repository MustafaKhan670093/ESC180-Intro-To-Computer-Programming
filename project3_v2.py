import math

def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''
    
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)

def cosine_similarity(vec1, vec2):
    norm_vec1 = norm(vec1)
    norm_vec2 = norm(vec2)    

    product = 0
    '''
    Possible improvements:
    - list comprehension / zip?  - sum(x_i*y_i for x_i, y_i in zip(x, y))
    - loop through the shorter dict?
    '''
    for key in vec1:
        product += vec1[key] * vec2.get(key, 0)
    
    return product / (norm_vec1 * norm_vec2)

def build_semantic_descriptors(sentences, general_dict = {}):
    # sentence is a 1d list (["i", "am", "a", "spiteful", "man","man"])

    for sentence in sentences:
        # Generate dictionary
        sentence_dict = {}
        for word in sentence:
            sentence_dict[word] = 1

        # print(sentence_dict)
        sentence_word_dicts = {}
        for word in sentence_dict:
            if word not in sentence_word_dicts:
                temp_sentence_dict = sentence_dict.copy()
                del temp_sentence_dict[word]
                sentence_word_dicts[word] = temp_sentence_dict

                if word in general_dict:
                    for i in temp_sentence_dict:
                        if i in general_dict[word]:
                            general_dict[word][i] = general_dict[word][i] + temp_sentence_dict[i]
                        else:
                            general_dict[word][i] = temp_sentence_dict[i]
                else:
                    general_dict[word] = temp_sentence_dict

    #https://www.w3schools.com/python/python_ref_dictionary.asp


    return general_dict

# print(build_semantic_descriptors(sentences))

def build_semantic_descriptors_from_files(filenames):
    general_dict = {}

    for filename in filenames:
        with open(filename, "r", encoding="latin1") as f:
            data = f.read().lower()
            
            translation_table = {
                '\n': ' ',
                ',': ' ',
                '-': ' ',
                ':': ' ',
                ';': ' ',
                '--': ' ', # not necessary
                '!': '.',
                '?': '.',
                '  ': ' ', # check for double spaces
            }
            for i in translation_table:
                data = data.replace(i, translation_table[i])

            data_split = data.split(".")
            data_processed = []
            
            for line in data_split:
                data_processed.append(line.split())

            # data = [re.findall(r'\S+', i) for i in data.split(".")]

            # data = [i for i in [j for j in data] if i]
            general_dict = build_semantic_descriptors(data_processed, general_dict)

    return general_dict

# build_semantic_descriptors_from_files(["sample.txt"])

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    best_similarity = -2
    best_choice = None

    if word not in semantic_descriptors:

        return choices[0]

    for choice in choices:

        if choice in semantic_descriptors:
            similarity = similarity_fn(semantic_descriptors[word], semantic_descriptors[choice])
        else:
            similarity = -1

        if similarity > best_similarity:
            best_similarity = similarity
            best_choice = choice
    
    return best_choice

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    with open(filename, "r", encoding="latin1") as f:
        data = [i.split(" ") for i in f.read().split('\n')]

    counter = 0
    max_score = len(data)
    for line in data:
        problem = line[0]
        print("Problem: " + str(problem))
        answer = line[1]
        print("Answer: " + str(answer))
        choices = line[2:]

        guess = most_similar_word(problem, choices, semantic_descriptors, similarity_fn)

        if guess == answer:
            counter += 1
    
    return 100*counter/max_score

import time
start = time.time()

training_samples = ['sample.txt']

semantic_descriptors = build_semantic_descriptors_from_files(["sw.txt", "wp.txt"])
res = run_similarity_test('test.txt', semantic_descriptors, cosine_similarity)
print(f"{res}% of the guesses were correct")

end = time.time()
print(end - start)