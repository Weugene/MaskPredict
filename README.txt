Project documentation
1. problem statement
2. model
3. architecture for the resulting service
4. how to use the Telegram service
5. how to use the HTML service


# 0. Intallation and Run.
first of all, you need to clone this repository and then download the model from the [link](
https://drive.google.com/drive/folders/1j-WzXAzUQ9jHB4cI8eFyTV8PAyituDCN?usp=sharing) a `service/mymodel/file pytorch_model.bin` and put it inside service/mymodel/
'''
docker-compose build && docker-compose up
'''

# 1. This ML-service uses a pretrained BERT model (BertForMaskedLM), which predicts a masked word.
(BERT: Bidirectional Encoder Representations from Transformers. It’s a language representation model created by Google researchers)

Problem statement: to find out what word can be hidden behind the word "MASK" (a special token).


# 2. Model: BertForMaskedLM.

We’ll be using HuggingFace’s transformers and PyTorch, alongside the bert-base-uncased model.

Steps:
1) Tokenization — we tokenize our input text using BertTokenizer.
2) Create labels — we clone our input_ids tensor into a new labels tensor. 
3) Masking — we need to mask a random selection of tokens in our input_ids tensor. To create our 15% probability of masking any one token, we can use torch.rand alongside a condition of each value < 0.15.
4) Training 2 epochs.
5) Calculate Loss — final step: the model loss.

Dataset:
Because we’re just randomly masking a selection of tokens — we can use almost any text. We don’t need labeled or special data. Here, we’ll use "The Adventures of Huckleberry Finn" by Mark Twain.

Input and output description: input - text (type: str); the output would be several words with weights (how likely a particular word can be used in that sentence).

Training loss: 0.0075


# 3. Architecture for the resulting service: A python telegram bot framework based on Flask (a light-weight Python web framework that gets use of Werkzeug toolkit and Jinja2 template engine).
This bot acts as a relay between server and Telegram.
Docker: synchronous projects (Flask)
Client: Telegram Bot or HTML


# 4. Chat Bot name: @MovieCommentClassifier_bot (please, don't look at the name:)
To run the bot: 
1) clone the repository 
2) open folder LSML_BERT_ML_service 
3) run this command: docker-compose build && docker-compose up  
4) find the bot  
5) type command /start 
6) type sentence (for example, "My [MASK] is so cute.")


# 5. It was written a simple HTML front end. In the input form user should enter a masked text.
After running the docker you can check HTML frontend part using this link: http://localhost:4000/
The service which is responsible for the html frontend is called client-html_frontend.
