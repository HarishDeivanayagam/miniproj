from .inputHandler import create_test_data
from .config import siamese_config
from keras.preprocessing.text import Tokenizer
from operator import itemgetter	
from keras.models import load_model

def compare(s1, s2):

    tokenizer = Tokenizer()

    model = load_model(r"C:\Users\Harish\Desktop\miniprojv2\services\LSTM\model.h5")

    test_sentence_pairs = [(s1,s2),(s1,s2)]


    test_data_x1, test_data_x2, leaks_test = create_test_data(tokenizer,test_sentence_pairs,  siamese_config['MAX_SEQUENCE_LENGTH'])

    preds = list(model.predict([test_data_x1, test_data_x2, leaks_test], verbose=1).ravel())
    results = [(x, y, z) for (x, y), z in zip(test_sentence_pairs, preds)]
    results.sort(key=itemgetter(2), reverse=True)
    print(results[0][2])
    return results[0][2]
