import flask
from flask import request, jsonify
from transformers import GPT2Tokenizer, GPT2LMHeadModel

hf_model_path = 'IDEA-CCNL/Wenzhong-GPT2-110M'
tokenizer = GPT2Tokenizer.from_pretrained(hf_model_path)
model = GPT2LMHeadModel.from_pretrained(hf_model_path)
app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


# A route to return all of the available entries in our catalog.
@app.route('/call', methods=['GET'])
def api_call():
    query_parameters = request.args
    input = query_parameters.get('input')
    return jsonify(call(input))


def call(input):
    question = input
    inputs = tokenizer(question, return_tensors='pt')
    generation_output = model.generate(**inputs,
                                       return_dict_in_generate=True,
                                       output_scores=True,
                                       max_length=500,
                                       # max_new_tokens=80,
                                       do_sample=True,
                                       top_p=0.8,
                                       # num_beams=5,
                                       eos_token_id=50256,
                                       pad_token_id=0,
                                       num_return_sequences=1)
    output = ''
    for idx, sentence in enumerate(generation_output.sequences):
        output += 'next sentence %d:\n' % idx
        output += tokenizer.decode(sentence).split('<|endoftext|>')[0]
        output += '*' * 100
    return output


if __name__ == '__main__':
    app.run(host='0.0.0.0')
