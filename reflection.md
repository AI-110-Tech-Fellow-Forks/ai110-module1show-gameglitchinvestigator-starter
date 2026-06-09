# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  - The game started on normal mode, the UI seemed okay but was a little inconsistent.
  - Something I noticed is that you could change game difficulty mid round which doesnt make sense. Also the guess counter did not track correctly.
- List at least two concrete bugs you noticed at the start 
  (for example: "the hints were backwards").
    - One concerete bug was that the hints did not work at all. They were not relevant at all.
    - The new game button does not work, you have to refresh the page to start a new round.
    - You can guess numbers outside of the alloted range.
    - The number range when you switch to hard mode does not update on the main interface.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guessed 300 | Reprompt to guess within range | Counted as valid guess | |
| Clicked "New Game" button | Start new round | No effect, page needs refresh | |
| Changed difficulty mid-game | Should not allow difficulty change mid-round | Difficulty changed while game active | |
| Asked for hint | Relevant hint to the secret number | Hint not relevant or shown | |
| Switched to Hard mode | Number range updates on interface | Range display doesn't update | |
| Made multiple guesses | Guess counter increments accurately | Guess counter doesn't track correctly | |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - I used Claude on this project.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - One example of an AI suggestion that was correct was about the new game. The fix it gave was to change the status back playing when the new game button was hit. Also with this we needed to reset the score and history. It also would correctly update the amount of guesses if you changed difficulties in between rounds.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result). 
  - One suggestion it gave that was misleading was with the hint calculation bug. It thought that the hints should be fixed at one time. I think it got confused about the current hint logic essentially being a even attempt check rather than based on the numbers being guessed themselves.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - To confirm bug fixes I first tested the live site to see if it was fixed. If it was fixed on the live site then used pytest to check if it followed the logic we wanted. If the pytest also worked then I would decide that it was fixed.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  - A few tests I ran was the tests to check if the allowed amount of guesses correctly changed when the difficulty changed. For example a hard difficulty test checks and makes sure only 5 guesses are allowed. When these tests passed then I knew the logic for that worked.

- Did AI help you design or understand any tests? How?
  - I had AI write some tests. I used it to test edge cases for existing logic. I also had it write tests for the other bugs I found but found that it did not test all the logic fully and left some parts out. 


---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  - From what I understand Streamlit reruns work by having the python script run everytime a user interacts with something, so if they click new game or submit guess it will run the script all over again each time. Session state works by storing the things that you want to track and then you can recall that existing state in a rerunned version helping maintain persistence. 

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
    - One habbit from this project I want to reuse in the future is the way I interacted with the AI. We made sure not to blindly accept changes and this helped improve our understanding of the code. It also helped us recognize when the AI made a mistake or did not have the propper context, helping avoid time wastage fixing bugs that could have been prevented.

- What is one thing you would do differently next time you work with AI on a coding task?
  - One thing I would do differently next time is to make sure to give AI the exact context I need it to have. Sometimes it will pull things from other files that are not related and that could alter the output, so mroe clear prompting is something I would do.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - This project made me realize how much more beneficial AI can be. Often times I used it as a last resort but it can be helpful to use while working and if used properly does not impact growth and learning. 
