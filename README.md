# PythonAimTrainer

Simple Python Aim Trainer made with pygame to improve gamer's aim.

## Requirements

Download the lateset version of pygame and python3.

I used the latest at the time:
Pygame Version 2.5.0
Python Version 3.11.4

Then launch and click away!

When the game ends click or press any key to end the game and exit.

## Additional

As I have been focusing on other modules and hobbies, I recreated this aim trainer by following Tech With Tim's tutorial on YouTube in order to refresh my knowledge on Python and remember the correct Syntax usage.

One little interesting I learned, which was unexpected, was the Splat/Unpack Operator used to unpack the mouse position as seen below, rather than indexing mouse_pos[0], etc.

```python
if click and target.collide(*mouse_pos):
```