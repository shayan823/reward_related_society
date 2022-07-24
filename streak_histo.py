import matplotlib.pyplot as plt
import numpy as np
import pickle
import datetime
import pandas as pd
from itertools import groupby

import datajoint as dj

dj.config["database.host"] = "datajoint-public.internationalbrainlab.org"
dj.config["database.user"] = "ibl-public"
dj.config["database.password"] = "ibl-public" 

from nma_ibl import reference, subject, action, acquisition, data, behavior, behavior_analyses


def find_streaks_n_contrast(one_session_answers,one_session_contrasts):
  # input: two array same size
  # answers is array of -1 1 for failure, reward for each trail
  # contrast is the matching contrast


  coupled_data = zip(one_session_answers,one_session_contrasts)
  # get a list of lists. every sublist contains tuples feedback-contrast with identical and contiguous feedback
  grouped = [list(group) for key,group in groupby(coupled_data, lambda x: x[0]) ] 
  # grouped answers and contrasts in streaks
  grouped_streaks, grouped_contrasts = zip(*[([inner_el[0] for inner_el in el], [inner_el[1] for inner_el in el]) for el in grouped])

  streak_rewards = [len(el) for el in grouped_streaks if len(el)>1 and el[0]>0]
  streak_failures = [len(el) for el in grouped_streaks if len(el)>1 and el[0]<0]

  contrast_rewards = [np.mean(grouped_contrasts[i]) for i, el in enumerate(grouped_streaks) if len(el)>1 and el[0]>0]
  contrast_failures = [np.mean(grouped_contrasts[i]) for i, el in enumerate(grouped_streaks) if len(el)>1 and el[0]<0]


  return streak_rewards, streak_failures, contrast_rewards, contrast_failures

def find_streaks(one_session_answers):
    next_trial_change = np.where(np.diff(np.sign(one_session_answers)))[0] # stores when next sign is different from the current - is a zero crossing problems
    ## always add last index
    next_trial_change = np.append(next_trial_change,len(one_session_answers)-1)
    if one_session_answers[0] != one_session_answers[1]:
        next_trial_change = np.append( np.asarray([0]), next_trial_change)

    portion_sign = np.sign(one_session_answers[next_trial_change]) #always alternate 
    repetitions = np.diff(next_trial_change)
    streak_index = np.where(repetitions>=2)[0] # returns tuple?
    streak_index+=1
    signed_streaks = portion_sign[streak_index] * repetitions[repetitions >= 2]
    streak_rewards = signed_streaks[signed_streaks > 0]
    streak_failure = signed_streaks[signed_streaks < 0] 

    return streak_rewards, streak_failure

def plot_answers(data,subject_id,session_date):
    portion = data & {'subject_uuid': subject_id} & {'session_start_time': session_date}
    answers = portion.fetch('trial_feedback_type')
    plt.figure(figsize=(12,8))
    plt.scatter(np.arange(len(answers)),answers)
    plt.plot(np.arange(len(answers)),answers)
    plt.show()

    return

def sessions2percentage_learning(mouse_portion):
    
    total_trials = len(np.unique(mouse_portion.fetch('session_start_time')))
    train_percentage = np.arange(1,total_trials+1) / total_trials
    bins = np.linspace(0, 100, 10)
    digitized = np.digitize(train_percentage*100, bins)*10
    # train_percentage_bin = ((train_percentage // 0.1) + 1)*10 assisgnes 0.8 to 90 %
    return digitized # should be assigend to all trials, not session  

def main():
    trained_subjects = subject.Subject * behavior_analyses.SessionTrainingStatus & 'training_status="in_training"'
    interesting_trials = behavior.TrialSet.Trial.proj('trial_stim_prob_left','trial_feedback_type','trial_stim_contrast_left','trial_stim_contrast_right')  & 'trial_stim_prob_left = 0.5'
    data = trained_subjects * interesting_trials

    all_streaks = {}
    all_subjects = np.unique(data.fetch('subject_uuid'));
    for i, mouse in enumerate(all_subjects):
        print(i+1,'/',len(all_subjects))
        all_streaks[str(mouse)] = {}
        mouse_portion = data & {'subject_uuid': mouse}
        
        percentage_learning = sessions2percentage_learning(mouse_portion)
        
        all_sessions_mouse = np.unique(mouse_portion.fetch('session_start_time'))
        
        for j,session in enumerate(all_sessions_mouse):
            all_streaks[str(mouse)][session] = {}
            
            session_table = mouse_portion & {'session_start_time': session} # very stupid before was subject_session_start_date
        
            
            answers = session_table.fetch('trial_feedback_type')
            
            contrasts = session_table.fetch('trial_stim_contrast_left') + session_table.fetch('trial_stim_contrast_right') 
            rewards, failures, contrast_rewards, contrast_failures = find_streaks_n_contrast(answers,contrasts)
            

            all_streaks[str(mouse)][session]['rewards'] = rewards
            all_streaks[str(mouse)][session]['failures'] = failures
            all_streaks[str(mouse)][session]['contrast_rewards'] = contrast_rewards
            all_streaks[str(mouse)][session]['contrast_failures'] = contrast_failures
            all_streaks[str(mouse)][session]['learning_percentage'] = percentage_learning[j]

    with open('extended_all_streaks.pickle', 'wb') as handle:
            pickle.dump(all_streaks, handle, protocol=pickle.HIGHEST_PROTOCOL)


    return


if __name__=="__main__":
    main()