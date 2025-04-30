;assembly code for celebrity age guessing game
;opens a text file and reads in different celebrities and their ages
;the game prints the celebrity's age to the screen
;compares user input against correct answer

%macro print 2
; print name, 17
mov eax,4
mov ebx,1
mov ecx, %1
mov edx,%2
int 80h
%endmacro

section .data
;Welcome message for game
welcome db "Celebrity age guessing game! Guess if celebrity's age is higher lower than the previous", 10
welcomelen equ $-welcome

rules db "RULES: Y - Younger, O - Older",10
ruleslen equ $-rules

correct db "Correct! They are ", 10
correctlen equ $-correct

incorrect db "Incorrect! They are ", 10
incorrectlen equ $-incorrect

start db "Vin Diesel is 53 years old", 10
startlen equ $-start

question db "Is the following celebrity older or younger than the previous? ", 10
questionlen equ $-question 

cr db 10

global listAnswers
listAnswers:
  dq 'Y'
  dq 'Y'
  dq 'O'
  dq 'Y'
  dq 'O'
  dq 'O'
  dq 'Y'
  dq 'O'
  dq 'Y'
  dq 'O'
  
global listAges
listAges:
  dq '51'
  dq '40'
  dq '43'
  dq '39'
  dq '50'
  dq '65'
  dq '48'
  dq '57'
  dq '32'
  dq '54'
 
global listNames 
listNames:
  dq 'Matthew Perry   ',10
  dq 'Kim Kardashian  ',10
  dq 'Milo Ventimiglia',10
  dq 'Serena Williams ',10
  dq 'Nick Offerman   ',10
  dq 'Kris Jenner     ',10
  dq 'Eminem          ',10
  dq 'Brad Pitt       ',10
  dq 'Vanessa Hudgens ',10
  dq 'Halle Berry     ',10

answer:
  dq 0
  
age:
  dq 0
  
name:
  dq 0

global score
score:
  dq 0
  dq 1
  dq 2
  dq 3
  dq 4
  dq 5
  dq 6
  dq 7
  dq 8
  dq 9
  dq 10
  
c_score:
  dq 0
    
segment .bss
guess resb 1 ;store users guess

section .text
  global _start
  
_start:
call displayWelcome
call newLine
mov rax, 10 ;number of celebrities
mov rbx, 0  ;store the answer
mov rcx, listAnswers    ;RCX will point to the current element array to be guessed
mov rdx, listNames      ;
mov rsi, listAges       ;
;mov rdi, score

;main function that calls other functions
top: 
  mov rbx, [rcx] ;put the current answer being guessed in rbx
  mov [answer],rbx ;move rbx into variable answer that stores the current guess
  mov rbx,[rsi]
  mov [age],rbx
  ;mov rbx, [rdx]
  mov [name],rdx
  push rax ;push rax on stack
  push rcx ;push rcx on stack
  push rsi
  push rdx
  ;push rdi
  call displayQuestion ;display the question
  call newLine
  call reading ;call reading to get the users guess
  call display ; print the letter they should have guessed
  call newLine ; new line like endl in C++
  ;pop rdi
  pop rdx
  pop rsi
  pop rcx ; get back from stack
  pop rax ; get back from stack
  
  add rsi,8      ;
  add rdx,24     ;
  add  rcx,8     ;move pointer to next element as 8 bits for each move on by 8
  
  dec  rax        ;decrement counter so going down 
  jnz  top        ;if counter not 0, then loop again
  call done ; end program
  
;Display function
display:
  mov edx, 2   ;message length
  mov ecx, age    ; message to write the letter to be predicted
  mov ebx, 1     
  mov eax, 4
  int 0x80
    ret
    
;function to read the user guess and do comparison with thte answer
reading:
  mov eax, 3 ;read from keyboard
  mov ebx, 2
  mov ecx, guess ;move guess into ecx
  mov edx, 1
  int 80h ;call interrupt
  mov rax, [guess] ;move guess by user into rax
  cmp rax, [answer] ;compare correct answer with whats in rax
  je same ;if guess was correct jump to same function
  call Notsame ;if the guess is incorrect then go to Notsame function
  ret
  
;function to show message that answer was not correct answer
Notsame:
  print incorrect,incorrectlen
  mov eax, 3 ; read prevoius enter key press
  mov ebx, 2;
  mov ecx, guess ;deal with previous enter key press so it does not mess up loop
  mov edx, 1 ;as single letter using 1 byte
  int 80h      ;call interrupt
  print [c_score], 1
    ret

;function to show message answer was correct
same:
  print correct, correctlen
  mov eax, 3
  mov ebx, 2
  mov ecx, guess ;deal with previous enter key press so it does not mess up loop
  mov edx, 1 ;as single letter using 1 byte
  int 80h      ;call interrupt
  
  ;add rdi,8
  ;mov [c_score], rdi
  ;print c_score, 1
    ret
    
;function to create new line
newLine:
  mov eax, 4 ; syswrite
  mov ebx, 1 ; stdout
  mov ecx, cr ; put new line value in ecx register
  mov edx, 1 ; length of new line value
  int 80h
  ret
  
;function to display welcometo game message
displayWelcome:
  print welcome, welcomelen       ;call kernel
  print rules, ruleslen
  print start, startlen
  ret
  
;function to display quiz question
displayQuestion:
  print question, questionlen
  print [name], 17
  ret
  
;function to end the program
done:
  mov eax, 1
  int 0x80
