def draw_love_with_word(word):
    # Define the size of the heart
    size = 10

    # Create the top half of the heart
    for i in range(size // 2, 0, -1):
        spaces = " " * i
        hearts = "❤" * (size - i * 2)
        print(f"{spaces}{hearts}{spaces}")

    # Create the bottom half of the heart
    for i in range(size // 2):
        spaces = " " * i
        hearts = "❤" * (size - i * 2)
        print(f"{spaces}{hearts}{spaces}")

    # Print the word in the center
    word_spaces = " " * ((size - len(word)) // 2)
    print(f"{word_spaces}{word}{word_spaces}")

# Call the function to draw a heart with the word "teacher"
draw_love_with_word("teacher")
