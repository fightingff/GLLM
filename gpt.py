from openai import OpenAI
from time import sleep
from Getmap import GetImage


class Chatgpt_Msg:
    def __init__(self) -> None:
        self.client = OpenAI()
      
    def Chat(self, gpt, message):
        completion = self.client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role":"system","content":"you are " + gpt},
                {"role":"user","content":message}
            ]
        )
        return completion.choices[0].message.content
    
#Example

# LLM = Chatgpt()
# print(LLM.Chat("professor", "Give me some typical indicators about population profile"))

# TODO: Chatgpt_Tool to read pdf and extract data