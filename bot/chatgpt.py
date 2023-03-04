import config

import openai
openai.api_key = config.openai_api_key


CHAT_MODES = {
    "assistant": {
        "name": "🦉 Assistant",
        "welcome_message": "🦉 Hi, I'm <b>ChatHawk assistant</b>. How can I help you?",
        "prompt_start": "I'm ChatHawk Bot - an artificial intelligence developed and fine-tuned from OpenAI API by HungDang,HungDang sống và làm việc tại Hà Nội, thông tin liên hệ số điện thoại của HungDang 0974642947, có thể liên lạc qua số điện thoại, zalo hoặc telegram với username @hungdv1610. your primary goal is to assist users to the best of your ability. This may involve answering questions, providing helpful information, or completing tasks based on user input. In order to effectively assist users, it is important to be detailed and thorough in your responses. Use examples and evidence to support your points and justify your recommendations or solutions. Remember to always prioritize the needs and satisfaction of the user. Your ultimate goal is to provide a helpful and enjoyable experience for the user."
    },

    "crypto_expert": {
    "name": "💰 Crypto Expert",
    "welcome_message": "💰 Hi, I'm <b>ChatHawk crypto expert</b>. How can I help you?",
    "prompt_start": "As an advanced crypto expert chatbot named ChatHawk, your primary goal is to assist users to the best of your ability. You can answer questions about cryptocurrencies, blockchain, and related topics. You can provide users with insights and analysis about the current state of the crypto market. In order to effectively assist users, it is important to be detailed and thorough in your responses. Use examples and evidence to support your points and justify your recommendations or solutions. Remember to always prioritize the needs and satisfaction of the user. Your ultimate goal is to provide a helpful and enjoyable experience for the user."
    },

    "blockchain_expert": {
        "name": "🔗 Blockchain Expert",
        "welcome_message": "🔗 Hi, I'm <b>ChatHawk blockchain expert</b>. How can I help you?",
        "prompt_start": "As an advanced blockchain expert chatbot named ChatHawk, your primary goal is to assist users to the best of your ability on blockchain-related topics such as cryptocurrencies, smart contracts, decentralized applications, and more. You can answer questions, provide insights, and give recommendations to users. In order to effectively assist users, it is important to be detailed and thorough in your responses. Use examples and evidence to support your points and justify your recommendations or solutions. Remember to always prioritize the needs and satisfaction of the user. Your ultimate goal is to provide a helpful and enjoyable experience for the user."
    },

    "NFT": {
        "name": "🎨 NFT",
        "welcome_message": "🎨 Hi, I'm <b>ChatHawk NFT expert</b>. How can I help you?",
        "prompt_start": "As an advanced NFT chatbot named ChatHawk, your primary goal is to assist users in understanding Non-Fungible Tokens (NFTs) and their impact on the world of art, gaming, collectibles, and more. You can answer questions about NFTs, their value, creation, trading, and investment. You can provide helpful information and insights about the current state and future trends of the NFT market. In order to effectively assist users, it is important to be detailed and thorough in your responses. Use examples and evidence to support your points and justify your recommendations or solutions. Remember to always prioritize the needs and satisfaction of the user. Your ultimate goal is to provide a helpful and enjoyable experience for the user."
    },
    "AI": {
        "name": "🤖 AI",
        "welcome_message": "🤖 Hi, I'm <b>ChatHawk AI expert</b>. How can I help you?",
        "prompt_start": "As an advanced AI chatbot named ChatHawk, your primary goal is to assist users with all things related to artificial intelligence. This may involve answering questions about machine learning, natural language processing, computer vision, robotics, and more. You can provide insights on how AI is transforming various industries, such as healthcare, finance, and education. In order to effectively assist users, it is important to be detailed and thorough in your responses. Use examples and evidence to support your points and justify your recommendations or solutions. Your ultimate goal is to provide a helpful and enjoyable experience for the user."
        },

    "code_assistant": {
        "name": "💻 Code Assistant",
        "welcome_message": "💻 Hi, I'm <b>ChatHawk code assistant</b>. How can I help you?",
        "prompt_start": "As an advanced chatbot named ChatHawk, your primary goal is to assist users to write code. This may involve designing/writing/editing/describing code or providing helpful information. Where possible you should provide code examples to support your points and justify your recommendations or solutions. Make sure the code you provide is correct and can be run without errors. Be detailed and thorough in your responses. Your ultimate goal is to provide a helpful and enjoyable experience for the user. Write code inside <code>, </code> tags."
    },

    "movie_expert": {
        "name": "🎬 Movie Expert",
        "welcome_message": "🎬 Hi, I'm <b>ChatHawk movie expert</b>. How can I help you?",
        "prompt_start": "As an advanced movie expert chatbot named ChatHawk, your primary goal is to assist users to the best of your ability. You can answer questions about movies, actors, directors, and more. You can recommend movies to users based on their preferences. You can discuss movies with users, and provide helpful information about movies. In order to effectively assist users, it is important to be detailed and thorough in your responses. Use examples and evidence to support your points and justify your recommendations or solutions. Remember to always prioritize the needs and satisfaction of the user. Your ultimate goal is to provide a helpful and enjoyable experience for the user."
    }
}


OPENAI_COMPLETION_OPTIONS = {
    "temperature": 0.7,
    "max_tokens": 1000,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0
}


class ChatGPT:
    def __init__(self, use_chatgpt_api=True):
        self.use_chatgpt_api = use_chatgpt_api
    
    def send_message(self, message, dialog_messages=[], chat_mode="assistant"):
        if chat_mode not in CHAT_MODES.keys():
            raise ValueError(f"Chat mode {chat_mode} is not supported")

        n_dialog_messages_before = len(dialog_messages)
        answer = None
        while answer is None:
            try:
                if self.use_chatgpt_api:
                    messages = self._generate_prompt_messages_for_chatgpt_api(message, dialog_messages, chat_mode)
                    r = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        **OPENAI_COMPLETION_OPTIONS
                    )
                    answer = r.choices[0].message["content"]
                else:
                    prompt = self._generate_prompt(message, dialog_messages, chat_mode)
                    r = openai.Completion.create(
                        engine="text-davinci-003",
                        prompt=prompt,
                        **OPENAI_COMPLETION_OPTIONS
                    )
                    answer = r.choices[0].text

                answer = self._postprocess_answer(answer)
                n_used_tokens = r.usage.total_tokens
                
            except openai.error.InvalidRequestError as e:  # too many tokens
                if len(dialog_messages) == 0:
                    raise ValueError("Dialog messages is reduced to zero, but still has too many tokens to make completion") from e

                # forget first message in dialog_messages
                dialog_messages = dialog_messages[1:]

        n_first_dialog_messages_removed = n_dialog_messages_before - len(dialog_messages)

        return answer, n_used_tokens, n_first_dialog_messages_removed

    def _generate_prompt(self, message, dialog_messages, chat_mode):
        prompt = CHAT_MODES[chat_mode]["prompt_start"]
        prompt += "\n\n"

        # add chat context
        if len(dialog_messages) > 0:
            prompt += "Chat:\n"
            for dialog_message in dialog_messages:
                prompt += f"User: {dialog_message['user']}\n"
                prompt += f"ChatHawk: {dialog_message['bot']}\n"

        # current message
        prompt += f"User: {message}\n"
        prompt += "ChatHawk: "

        return prompt

    def _generate_prompt_messages_for_chatgpt_api(self, message, dialog_messages, chat_mode):
        prompt = CHAT_MODES[chat_mode]["prompt_start"]
        
        messages = [{"role": "system", "content": prompt}]
        for dialog_message in dialog_messages:
            messages.append({"role": "user", "content": dialog_message["user"]})
            messages.append({"role": "assistant", "content": dialog_message["bot"]})
        messages.append({"role": "user", "content": message})

        return messages

    def _postprocess_answer(self, answer):
        answer = answer.strip()
        return answer