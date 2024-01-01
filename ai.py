import g4f

g4f.debug.logging = True  # Enable logging
g4f.debug.check_version = False  # Disable automatic version checking
# print(g4f.Provider.Ails.params)  # Supported args
g4f.debug.timeout = 3

# Automatic selection of provider

# Streamed completion
response = g4f.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello"}],
)

print("GPT-3.5 Turbo:")
print(response)

# Normal response
response = g4f.ChatCompletion.create(
    model=g4f.models.gpt_4,
    messages=[{"role": "user", "content": "Hello"}],
)  # Alternative model setting

print("GPT-4:")
print(response)