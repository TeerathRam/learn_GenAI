import tiktoken

encoder = tiktoken.encoding_for_model("gpt-4o")

print("vocabe size", encoder.n_vocab)

text = "The cat sat on the mat"

token = encoder.encode(text)

print("Token", token)

my_token = [976, 9059, 10139, 402, 290, 2450]

print("Decode", encoder.decode(my_token))
