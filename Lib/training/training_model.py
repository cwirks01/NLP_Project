# Import requirements
import random
import spacy

from spacy.util import minibatch, compounding
from pathlib import Path

def training_model(TRAIN_DATA, **args):
    # TRAINING THE MODEL
    with nlp.disable_pipes(*unaffected_pipes):

        # Training for 30 iterations
        for iteration in range(30):

            # shuufling examples  before every iteration
            random.shuffle(TRAIN_DATA)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                            texts,  # batch of texts
                            annotations,  # batch of annotations
                            drop=0.5,  # dropout - make it harder to memorise data
                            losses=losses,
                        )
                print("Losses", losses)

if __name__=='__main__':
    
    training_model()