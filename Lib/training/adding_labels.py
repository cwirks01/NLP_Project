import spacy

nlp = spacy.blank("en")

ner = nlp.create_pipe("ner")
ner.add_label("DRUGS")

nlp.add_pipe('ner', name="drug_recognition_ner")

nlp.to_disk("drug_ner")