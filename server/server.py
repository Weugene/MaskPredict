from flask import Flask, request
import json

import torch
from transformers import BertTokenizer, BertModel, BertForMaskedLM
import logging
logging.basicConfig(level=logging.INFO)# OPTIONAL
app = Flask(__name__)




def predict_masked_sent(text, top_k=5):
    # Tokenize input
    text = "[CLS] %s [SEP]"%text
    tokenized_text = tokenizer.tokenize(text)
    masked_index = tokenized_text.index("[MASK]")
    indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
    tokens_tensor = torch.tensor([indexed_tokens])
    # tokens_tensor = tokens_tensor.to('cuda')    # if you have gpu

    # Predict all tokens
    with torch.no_grad():
        outputs = model(tokens_tensor)
        predictions = outputs[0]

    probs = torch.nn.functional.softmax(predictions[0, masked_index], dim=-1)
    top_k_weights, top_k_indices = torch.topk(probs, top_k, sorted=True)
    res = []
    for i, pred_idx in enumerate(top_k_indices):
        predicted_token = tokenizer.convert_ids_to_tokens([pred_idx])[0]
        token_weight = top_k_weights[i]
        print("[MASK]: '%s'"%predicted_token, " | weights:", float(token_weight))
        res.append({"MASK": predicted_token, "weights:": float(token_weight)})
    return res

#print(predict_masked_sent("My [MASK] is so cute.", top_k=5))

def load_model():
    tokenizer = BertTokenizer.from_pretrained('mytokenizer/')
    model = BertForMaskedLM.from_pretrained('mymodel/')
    #tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    #model = BertForMaskedLM.from_pretrained('bert-base-uncased')
    model.eval()
    # model.to('cuda')  # if you have gpu
    return tokenizer, model


def calc(text):
    result = predict_masked_sent(text, top_k=5)
    return result

@app.route('/getmask', methods=["GET", "POST"])
def clf_handler():
    if request.method == 'POST':  # handle only POST requests
        data = request.get_json(force=True)  # read the payload
        result = calc(data)  # calculate the target function
        response = {
            "result": result
        }
        return json.dumps(response)
    else:
        return "You should use only POST query"

if __name__ == '__main__':
    tokenizer, model = load_model()
    app.run("0.0.0.0", 1234)
