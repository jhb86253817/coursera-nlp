import nltk
from nltk.corpus import brown

#to generate training data and testing data for bigram language model
#adding a * in the front of a sentence 

#get the traing data and testing data from brown corpus
sents = brown.sents(categories='news')
size = int(len(sents) * 0.9)
training_data, testing_data = sents[:size], sents[size:]

#writing them to files
train_file = open("training_data2", 'wb')
test_file = open("testing_data2", 'wb')

for sent in training_data:
    train_file.write("* ")
    for word in sent:
        train_file.write("%s " % word)
    train_file.write("\n")
train_file.close()

for sent in testing_data:
    test_file.write("* ")
    for word in sent:
        test_file.write("%s " % word)
    test_file.write("\n")
test_file.close()




