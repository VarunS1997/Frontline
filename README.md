## Inspiration
Every minute, over 500 websites are made, 120 thousand images are uploaded, and 204 million emails are sent... **every minute** over 612 GB of data is uploaded to "mainstream" sites alone -- data that needs to be read, processed, and stored. And that number is only rising; and it's already quite the jump from 10 years ago -- when modern Facebook alone was larger than the entire Internet

Clearly, our world is growing digitally. We are getting more data, more programmers, and more work to do. But, with the [possible end to Moore's Law](https://www.technologyreview.com/s/601441/moores-law-is-dead-now-what/), how are we planning to keep up? We barely have enough programmers as is!

__The computer revolution is over, now, it's time for the information revolution -- and our app is going to lead the charge.__

## What it does
Information processing and "Big Data" programs are slow; they regularly deal with innumerable amounts of bytes and data, but it certainly shows. Yet, as the world digitizes, humanity's demands for speed do, too. In this field, our best weapon as programmers is multi-threading -- the process of employing more than one thread for calculations and data processing. Often, we think of it as the "holy grail" -- surely, two threads work twice as fast as one and four work twice as fast as two!

The problem is multi-threaded programs get complex, fast. Their source code alone is often twice as complex and demands other overhead, such as dynamic resource management -- not to mention they are much more difficult to program and debug.

__Essentially, there always has been a disconnect between rapid deployment and rapid execution -- big programs run fast, but only slow programs are small.__

Frontline is here to bridge that gap. Our program analyzes small simple programs and automatically generates larges, more efficient programs that follow the same instructions. We employ multi-threading wherever we can, while keeping the simplicity every programmer loves, and still leaving you with the option of taking your program back in your hands.

__Who cares?__
YOU DO. Frontline means data companies can store small, but inefficient programs in their databases, while keeping maximum performance a run time away. This means more space to the consumer, more speed to the internet, and less headache for every engineer involved -- all while making the world a better place.

## How we built it
To put it simply, teamwork, adaptability, and determination.

Frontline is a program that creates multi-threaded programs; a programmer would shudder at being tasked that -- we certainly did. When we built it, it came with headaches, cryptic error messages, and things out of a programmer's nightmares.

But we persevered. We stuck together through the sleepless nights and seemingly endless lines-for-food. And while we had our own jobs, we looked out for each other. And when we hit hurdles -- and we hit a lot -- we threw out the old plans, and made new ones. No plan is a good plan if it never changes. But most importantly, when even the backup plans failed, and we wanted to quit drinking coffee and just go to sleep, we all fought on. We are a team, and we wouldn't let ourselves forget that -- because if we did, Frontline would just be a series of declarations and missed opportunities.

## Challenges we ran into
Auto-parallelization is a difficult problem. No one hesitated to tell us that.

But when we started, we had no idea what we were getting ourselves into. This program has been the stuff of nightmares. Aside from the small problems, there were some tough hurdles to overcome:

First and foremost, a familiar problem to all of us, the cryptic error messages. Considering our program executes programs and analyzes them, it creates nested scopes. These "subscopes" are treated as their own pseudofiles, complete with their own definitions and code; yet, they disappear at termination -- however, abrupt. Often the error messages were "None" or something like "Error: on line :". We nearly ripped out our hair at these words. Eventually, we got clever. We learned to write the executions to their own files and running them for analysis. Then the messages became less cryptic and we progressed -- even if it was a bit cumbersome every run.

Next was the analysis itself. When we analyzed programs, we had to identify what variables could be moved around, what loops could be parallelized, and what variables would exist at the time of execution, without executing it. Originally, we tried to employ regular expressions -- to little success. We found there were too many possible cases to account for everything, and we shifted focus slightly to be a bit more flexible and less reliant on the regex. Still, regex is an integral part of our program.

Finally, the higher order programming. In our classes, we had to learn to output code -- complete with indentation and proper scopes. This meant carefully writing each character, keeping in mind what the output would look like. It was a difficult and slow process, but we come out stronger.

All in all, the project was difficult. But, we learned a lot -- and admittedly , had a lot of fun. We knew it wasn't easy, and that's fine. Sometimes, easy is boring.

## Accomplishments that we're proud of
Frontline works!

You're welcome to see the outputs yourself in our TestCode subdirectory, or just keep reading here (especially the part about program 4).

We created some simple programs and let Frontline optimize them; and it did a brilliant job:
On a sample of **1000** tests...

__Program 1: A Proof of Concept__<br>
Program 1 analyzed a very basic for loop, purposefully written to be slow (about 1 second per iteration, with 4 iterations per test), and as expected, Frontline cut those numbers by nearly 75%.

Runtimes...<br>
Without Frontline deployment: 4.000 seconds<br>
With Frontline deployment: 1.274 seconds<br>
Improvement of 68.2%

__Program 2: Useless Recalculations__<br>
Program 2 showcases the power of our optimizer on a small scale by detecting a deterministic, constant calculation in a "for" loop and elevating its scope to prevent recalculation.

Runtimes...<br>
Without Frontline deployment: 0.003 seconds<br>
With Frontline deployment: .000055 seconds<br>
Improvement of 97.8%

__Program 3: A Word Counter__<br>
Program 3 counts the number of occurrences of every word in a chapter. A simple proof of concept for other similar data mining such as web crawling.

Runtimes...<br>
Without Frontline deployment: 3.008 seconds<br>
With Frontline deployment: 2.002 seconds<br>
Improvement of 33.7%<br>

__Program 4: Parallelized Factorials + Recalculations__<br>
Program 4 is a culmination of our work on Frontline. It employs both the optimizer and the parallelizer to give the best possible improvements; essentially, this program is a sample of a real world calculation.

Runtimes... (of 20 trials)<br>
Without Frontline deployment: 10.022 seconds<br>
With Frontline deployment: 3.241 seconds<br>
Improvement of 67.7%

__Running more tests! Come back later!__

## What we learned
Automatically enabling multiprocessing is a complicated endeavor. Despite our initial concerns over choosing Python as our programming language over, say, C++, we have realized Python may have been the best choice for programming languages that we could have possibly made. The interpreted nature of the language has proven to be invaluable in our processing. Furthermore, while the indentation-based annotation was a nuisance as first, it ultimately proved worthwhile.

Furthermore, we learned the idea behind creating an IDE. Essentially, our GUI accompaniment, while not the focus of the program, demonstrated a proof of concept that we can create a functional text editor that directly integrates with the core elements of our project, providing a framework for the eventual IDE that Frontline will inevitably need.

Needless to say, our skills in Higher Order Programming have taken bounds and leaps during this project. These skills have and will be the basis for Frontline for development cycles to come.

## What's next for Frontline
We've got a lot planned. Technical details aside, this project can bring about a whole new way to program for Big Data -- distributed computing, rapid deployment cycles, and much more. Give it a chance, be the first to step into the future with Frontline.
