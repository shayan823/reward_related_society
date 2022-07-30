# Reward and punishment-related changes in behavior during a decision-making task in mice

“Reward-related Society” Group :
Federico Szmidt, Maria Luiza de Vasconcelos, Nada Moustafa, Shayan Shafquat,
Simona Leserri

## Theoretical Background
Earlier studies on animals, such as fighting lobsters (Kravitz, 2000) and crickets (Rillich & Stevenson, 2011), show that they base their decisions on multiple factors, including the recent consequence of their actions. Interestingly, they are more likely to repeat their action after a streak of successes than following a streak of failures (Carlson & Shu, 2007). We set out to find whether making successful or failed choices in tandem also affects subsequent decisions in mice.
Decision-making has been studied through models including reinforcement Learning (RL) (Niv, 2009), which often measures the effects of context, rewards and punishments, and trial-history on decision-making behavior dynamics (Ashwood et al., 2022). The most common tasks used in decision-making studies consist of two or more options to be chosen, with or without rewards and punishments, and the subjects are either fixed or free.
The animal’s motivational state could also affect its choices, as tested, for example, by Berditchevskaia et al. (2016) in a GO/NO-GO visual discrimination task. Their animals showed changes in motivation with associated variations in response rate and correctness between the initial state of water-deprivation and late water satiation (Berditchevskaia, Cazé, & Schultz, 2016). This gives reason to investigate motivation in other decision-making tasks.
The International Brain Lab implemented a two-alternative forced-choice (2AFC) task in which mice detected the appearance of visual stimuli with changeable contrasts in their right or left visual field, and are required to move the detected stimulus to the center of the visual field using either clockwise or counterclockwise turns of a  steering wheel. Correct decisions are rewarded with variable volumes of sweetened water, while incorrect ones are followed by a noise burst and a longer inter-trial interval (Aguillon-Rodriguez et al., 2021). 

## Goals
We investigate whether or not the current decision and/or animal engagement are affected by preceding streaks of rewards or failures during training on the basic version of the modified 2AFC task designed by the International Brain Laboratory. 

## Methods
Publically available IBL datasets (data.internationalbrainlab.org) are used for modeling, analysis and visualization in Python. The basic 2AFC task data is targeted by our analysis. This task is purely perceptual, comprising an equal (50:50) probability of the stimulus to appear on the right or left of the visual field. We define a streak as a succession of trials with either correct (streak of rewards) or wrong (streak of failures) choices.
We hypothesize that the performance in trials following a streak will be above chance. To test this hypothesis, we will use a logistic regression model to predict the correctness of the current decision based on the length of preceding streaks, the contrast of the current stimulus, and the mouse satiety, measured as the total amount of water ingested by the animal in previous trials. Furthermore, a linear regression will be used to predict a proxy of task engagement, namely  the mouse’s reaction time, taking into account the same parameters. 

## Results
A preliminary data exploration showed that the streak distribution differs from a Poisson distribution with the same mean, suggesting that the streaks are not random but rather influenced by other factors, such as the task’s difficulty, learning, and motivation. An initial logistic regression resulted in an accuracy above 0.7 for untrained mice, and the weights for the streaks remained similar to the ones of the contrast.

## Next Week Goals
To test our hypothesis, we will:	

Keep exploring the distribution of both reward and failure streaks, for different learning levels and stimulus contrasts.
Build a logistic regression model of different lengths of streaks of rewards and punishments, and compare the weights for each case.
Include the accumulated water reward in the model as a proxy for motivation, and compare the accuracy for all cases. 
Run a linear regression to predict response time, factoring in all of the parameters (i.e. streaks, contrast and accumulated reward).

## References
Aguillon-Rodriguez, V., Angelaki, D., Bayer, H., Bonacchi, N., Carandini, M., Cazettes, F., … Zador, A. M. (2021). Standardized and reproducible measurement of decision-making in mice. ELife, 10, 1–28. https://doi.org/10.7554/eLife.63711
Ashwood, Z. C., Roy, N. A., Stone, I. R., Urai, A. E., Churchland, A. K., Pouget, A., & Pillow, J. W. (2022). Mice alternate between discrete strategies during perceptual decision-making. Nature Neuroscience 2022 25:2, 25(2), 201–212. https://doi.org/10.1038/s41593-021-01007-z
Berditchevskaia, A., Cazé, R. D., & Schultz, S. R. (2016). Performance in a GO/NOGO perceptual task reflects a balance between impulsive and instrumental components of behaviour. Scientific Reports, 6. https://doi.org/10.1038/SREP27389
Carlson, K. A., & Shu, S. B. (2007). The rule of three: How the third event signals the emergence of a streak. Organizational Behavior and Human Decision Processes, 104(1), 113–121. https://doi.org/10.1016/J.OBHDP.2007.03.004
Kravitz, E. A. (2000). Serotonin and aggression: insights gained from a lobster model system and speculations on the role of amine neurons in a complex behavior. Journal of Comparative Physiology A 2000 186:3, 186(3), 221–238. https://doi.org/10.1007/S003590050423
Niv, Y. (2009). Reinforcement learning in the brain. Journal of Mathematical Psychology, 53(3), 139–154. https://doi.org/10.1016/J.JMP.2008.12.005
Rillich, J., & Stevenson, P. A. (2011). Winning Fights Induces Hyperaggression via the Action of the Biogenic Amine Octopamine in Crickets. PLOS ONE, 6(12), e28891. https://doi.org/10.1371/JOURNAL.PONE.0028891


## Dataset used:
https://github.com/int-brain-lab/paper-behavior

### Guide to IBL code library
https://int-brain-lab.github.io/iblenv/
