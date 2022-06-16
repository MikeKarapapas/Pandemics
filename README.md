# Pandemics

This project is inspired by the Covid-19 outbreak and it is designed to give you a sense of how pandemics work.
To start the project just double click on Pandemics.py file and a screen will pop-up.

# How does the project work?

It creates an non-visible environment like a canvas and places randomly the susceptile and infected people. Each person has a standard velocity that allows him to move
on the canvas and a house that he uses in case of a quarantine. While the pandemia is running you take desicions that will determine the future number of cases and
generally the evolution of the pandemia, for instance you can click on "Self protection measures" button to diminish the future number of cases, but we will explain later how buttons work and what each button does.

# Susceptible people

To beggin with, each susceptible person (person who is prone to catch the disease) has a chance of getting infected when he comes into contact with an infected person.
While the simulation is running the number of susceptible people keeps decreasing turning them into infected people!

# Infected people

Infected people are people that have the virus and they spread it when they come into contact with a susceptible person. The way they spread the disease is the following: They have a maxInfDis variable that creates a circle around them and if a susceptible person is in that circle he has a probability 20% of getting infected which might seem small but it is a very representative number as the dimensions of the canvas are small so the density of people in that canvas is big. Number of infected people keeps increasing unless you take action immediatelly!

# Immune people

Immune people have got infected in the past and can no longer get infected as their body have developed "antibodies".

# Dead people

A small number of people from the infected category fall into the dead people category as they couldn't "resist" against the virus...

# Begining of the pandemic

In the begining you will be asked to enter the initial number of susceptible people and the initial number of the infected people, be carefull not to enter a large number neither for the infected nor for the susceptible people, because the density of the people will be very big as I previously mentioned.

After that hit the "Go!" button and watch the evolution of the pandemic!

# Buttons

- Protection measures button : For every person it diminishes his velocity to decrease the number of interactions between humans and subsequently the probability of infection

- Self protection measures button : Each person is taking care of hisself (washing hands, not touching his face) and inferencly he diminishes the chances of getting infected by 70%!

- Quarantine button : Sets the velocity of each person to 0 decreasing the rate of infected people per day

- Quarantine for infected people button : Locks every infected person in his house

- Restricted Qurantine button : Locks all people in their house

# Conformed people rate

Not all people cooperate! There is a small number of people that don't follow the orders you give so even if you lock everyone in their house there is still a small number of people that don't obey, hence you might see the cases increasing for some days.

Note: Protection measures don't work the same every time, as in real life! There are times that work perfect and indeed stop the continuous increase number of infected people and other times it doesn't work the same.

Have fun!!!
