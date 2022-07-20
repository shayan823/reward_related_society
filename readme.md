## Dataset used:
https://github.com/int-brain-lab/paper-behavior


## Method:
To study animal decision-making behavior, studies have used two alternative choice tasks (2AFC) in which mice learn via trial and error to choose the correct location of a stimulus displayed on the left or right of a computer screen. The mice are motivated via the delivery of reward when correct and streaks of reward are a succession of trials with either correct or wrong choices. We propose to investigate whether there is a correlation between past streaks of rewards or failures and changes in the current choice of the mice during training on a 2AFC task, in standardized experiments designed by the International Brain Laboratory.
The length of the streak, reward-related satiety, and choices in previous trials will be used as predictors of choice on subsequent trials in a GLM model. Apart from choice correctness, we will also quantify latency (i.e. time difference between stimulus display and wheel movement) and wheel velocity (wheel speed due to mouse action) as measures of task engagement. 
We hypothesize that the performance in trials following a streak will be above chance. In order to assess this hypothesis, we will first perform an exploratory Linear Regression. This technique allows for the prediction of the three outcomes of interest. More complex GLM could allow for a better explanation of the observed relationships. Ultimately, Markovian decision model or time series approaches could be used.
Studying the relationship between task engagement, reward, and learning rate could pave the way for insights on how we learn and perform decision making.
