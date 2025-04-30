import random

def game():
    stop = False
    score = 0
    with open('celeb-ages.txt') as f:
        lines = f.readlines()
    print('Celebrity age guessing game!\nRULES\nGuess if celebrity\'s age is higher lower than the previous\nY - Younger\nO - Older')
    celeb = lines[random.randint(0,len(lines)-1)].strip("\n").split(",")
    print(celeb[0] + " is " + celeb[1] + " years old")
    previous = celeb[1]
    while stop == False:
        print("\nScore: "+str(score))
        question = lines[random.randint(0,len(lines)-1)].strip("\n").split(",")
        ans = input("Q: Is "+question[0]+" younger or older?\nA: ")
        if ans.lower() == 'y':
            if question[1]>previous:
                print("Incorrect! " + question[0] + " is " +question[1]+ " years old")
            else:
                print("Correct! " + question[0] + " is " +question[1]+ " years old")
                score += 1
            previous = question[1]
        elif ans.lower() == 'o':
            if question[1]>=previous:
                print("Correct! " + question[0] + " is " +question[1]+ " years old")
                score += 1
            else:
                print("Incorrect! " + question[0] + " is " +question[1]+ " years old")
            previous = question[1]
        elif ans == 'quit':
            stop = True

game()
