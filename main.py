import os, configparser, json
from openai import OpenAI


def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


def get_openai_token():
    if os.getenv('OPENAI_API_KEY'):
        print('Using OpenAI token from environment variable')
        return os.environ['OPENAI_API_KEY']
    
    config = read_config()
    print('Using OpenAI token from config file')
    return config.get("openai", "key")


def init_openai() -> OpenAI:
    token = get_openai_token()
    if token == "" or token is None:
        raise ValueError("OpenAI token is required")
    return OpenAI(api_key=token)


def request_question(client: OpenAI):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """
                You will be a teacher for GCP Cloud Dev certification. 
                You should provide tricky and advanced questions to teach students everything required for passing GCP Cloud Dev certification. You should ask questions such as on GCP cloud dev exam. Sometimes use real life  based questions. 
                Here is a format in which you should give questions: 
                {"question":"...?","answers":[{"key":"a","value":"..."},{"key":"b","value":"..."},{"key":"c","value":"..."},{"key":"d","value":"..."}],"correctAnswer":"....","explanation":"...."}
"""
            },
            {
                'role': 'user',
                'content': 'Give me a question for GCP Cloud Developer certification'
            }
        ]
    )
    response = response.choices[0].message.content
    return json.loads(response)


def ask_question(question: str):
    print('************************************')
    print('Question: ', question['question'])
    for answer in question['answers']:
        print(f"{answer['key']}) {answer['value']}")


def handle_output(question: str):
    user_answer=''
    while user_answer.lower() not in [answer['key'].lower() for answer in question['answers']]:
        user_answer = input('Enter your answer: ')
    return user_answer


def validate_output(question: str, user_answer: str):
    print('Correct!') if user_answer.lower() == question['correctAnswer'].lower() else print('Wrong!')
    print(f'Explanation: {question["explanation"]}')


def main():
    openai = init_openai()
    while True:
        question = request_question(openai)
        ask_question(question)
        user_answer = handle_output(question)
        validate_output(question, user_answer)


if __name__ == '__main__':
    main()
