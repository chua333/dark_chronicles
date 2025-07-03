################################################################## meta llama
# import transformers
# import torch

# from credentials import huggingface_read
# from huggingface_hub import login

# login(token=huggingface_read)


# # "meta-llama/Llama-3.2-1B-Instruct"
# # "meta-llama/Meta-Llama-3.1-8B-Instruct"
# model_id = "google/gemma-2b"

# pipeline = transformers.pipeline(
#     "text-generation",
#     model=model_id,
#     model_kwargs={"torch_dtype": torch.bfloat16},
#     device_map="auto",
# )

# messages = [
#     {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
#     {"role": "user", "content": "Who are you?"},
# ]

# outputs = pipeline(
#     messages,
#     max_new_tokens=256,
# )
# print(outputs[0]["generated_text"][-1])

#################################################################### google gemma
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b")
model = AutoModelForCausalLM.from_pretrained("google/gemma-2b", device_map="auto")

input_text = "Context: Company ABC has the product of smartphones and tablets released in 2023, Question: Can you tell me about company ABC's product?"
input_ids = tokenizer(input_text, return_tensors="pt").to("cuda")

outputs = model.generate(
    **input_ids,
    max_new_tokens=100,
    do_sample=True,          # Enable sampling (instead of greedy)
    temperature=0.7,         # Controls creativity (lower = more focused)
    top_p=0.9,               # Nucleus sampling
    repetition_penalty=1.1,  # Prevents excessive repetition
)
print(tokenizer.decode(outputs[0]))
