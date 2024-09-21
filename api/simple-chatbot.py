# from transformers import pipeline, Conversation

# def chat_with_ai():
#     chatbot = pipeline("conversational", model="microsoft/DialoGPT-medium")
#     conversation = Conversation()
#     print("Chatbot: Hello! Type 'bye' to exit.")
    
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() == "bye":
#             print("Chatbot: Goodbye!")
#             break
#         conversation.add_user_input(user_input)
#         response = chatbot(conversation)
#         print(f"Chatbot: {response.generated_responses[-1]}")

# if __name__ == "__main__":
#     chat_with_ai()

from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "distilgpt2"  # or another smaller model
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

input_text = "How is it"
inputs = tokenizer.encode(input_text, return_tensors='pt')
outputs = model.generate(inputs, max_length=50, num_return_sequences=1)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)

