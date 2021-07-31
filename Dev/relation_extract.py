import spacy
from spacy.tokens import Doc, Span
from thinc.api import Model, chain, Linear, Logistic
from typing import List, Callable, cast
from thinc.types import Floats2d, Tuple, Ragged


@spacy.registry.architectures.register("rel_model.v1")
def create_relation_model(
        create_instance_tensor: Model[List[Doc], Floats2d],
        classification_layer: Model[Floats2d, Floats2d]
) -> Model[List[Doc], Floats2d]:
    model = chain(create_instance_tensor, classification_layer)
    model.attrs["get_instance"] = create_instance_tensor.attrs["get_instance"]
    return model


@spacy.registry.architectures.register("rel_classification_layer.v1")
def create_classification_layer(
        nO: int = None, nI: int = None
) -> Model[Floats2d, Floats2d]:
    model = chain(Linear(nO=nO, nI=nI), Logistic())
    return model


# The custom forward function


def instance_forward(
        model: Model[List[Doc], Floats2d],
        docs: List[Doc],
        is_train: bool,
) -> Tuple[Floats2d, Callable]:
    tok2vec = model.get_ref("tok2vec")
    pooling = model.get_ref("pooling")
    get_instances = model.attrs["get_instances"]
    all_instances = [get_instances(doc) for doc in docs]
    tokvecs, bp_tokvecs = tok2vec(docs, is_train)

    ents = []
    lengths = []

    for doc_nr, (instances, tokvec) in enumerate(zip(all_instances, tokvecs)):
        token_indices = []
        for instance in instances:
            for ent in ents:
                token_indices.extend([i for i in range(ent.start, ent.end)])
                lengths.append(ent.end - ent.start)
        ents.append(tokvec[token_indices])
    lengths = cast(Intsld, model.ops.asarray(lengths, dtype="int32"))
    entities = Ragged(model.ops.flatten(ents), lengths)
    pooled, bp_pooled = pooling(entities, is_train)
    relations = model.ops.reshape2f((pooled, -1, pooled.shape[1] * 2))

    def backprop(d_relations: Floats2d) -> List[Doc]:
        d_pooled = model.ops.reshape2f((d_relations, d_relations.shape[0] * 2, -1))
        d_ents = bp_pooled(d_pooled).data
        d_tokvecs = []
        ent_index = 0
        for doc_nr, instances in enumerate(all_instances):
            shape = tokvecs[doc_nr].shape
            d_tokvec = model.ops.alloc2f(*shape)
            count_occ = model.ops.alloc2f(*shape)
            for instance in instances:
                for ent in instance:
                    d_tokvec[ent.start:ent.end] += d_ents[ent_index]
                    count_occ[ent.start:ent.end] += 1
            d_tokvec /= count_occ + 0.00000000001
            d_tokvecs.append(d_tokvec)

        d_docs = bp_tokvecs(d_tokvecs)
        return d_docs

    return relations, backprop


def instance_init(model: Model, X: List[Doc] = None, Y: Floats2d = None) -> Model:
    tok2vec = model.get_ref("tok2vec")
    tok2vec.initialize(X)
    return model

def create_tensors(
        tok2vec: Model[List[Doc], List[Floats2d]],
        pooling: Model[Ragged, Floats2d],
        get_instances: Callable[[Doc], List[Tuple[Span, Span]]],
) -> Model[List[Doc], Floats2d]:
    return Model(
        "instance_tensors",
        instance_forward,
        init=instance_init,
        layers=[tok2vec, pooling],
        refs={"tok2vec": tok2vec, "pooling": pooling},
        attrs={"get_instances": get_instances},
    )
