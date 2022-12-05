from transformers import (
    T5ForConditionalGeneration,
    T5Tokenizer
)
import torch

# read fine-tuned tokenizer from model folder
tokenizer = T5Tokenizer.from_pretrained("model")
model = T5ForConditionalGeneration.from_pretrained(
    'model')  # read fine-tuned model from model folder
model.eval()


# function for getting a prediction from our fine-tuned T5 model, given some input text
def getResponse(text, model=model):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    preprocess_text = text.strip().replace("\n", "")
    tokenized_text = tokenizer.encode(
        preprocess_text, return_tensors="pt").to(device)
    model = model.to(device)

    outs = model.generate(    # generate tokenized response
        tokenized_text,
        max_length=100,
        num_beams=2,
        early_stopping=True
    )
    # decode tokenized response to regular text
    resp = [tokenizer.decode(ids) for ids in outs]
    return resp


text = ''

while text != 'q':        # Keep presenting prompt until q is pressed
    text = input('Ask any question. q to quit.\n')
    response = getResponse(text)
    # print response to terminal after stripping <pad> and </s> from the response
    print(response[0].strip('<pad></s'))
