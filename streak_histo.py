import matplotlib.pyplot as plt
import numpy as np
import pickle
import pandas as pd
import datetime
import datajoint as dj

dj.config["database.host"] = "datajoint-public.internationalbrainlab.org"
dj.config["database.user"] = "ibl-public"
dj.config["database.password"] = "ibl-public" 

from nma_ibl import reference, subject, action, acquisition, data, behavior, behavior_analyses

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

def main():
    # select trained subjects
    trained_subjects = subject.Subject * behavior_analyses.SessionTrainingStatus & 'training_status="in_training"'
    interesting_trials = behavior.TrialSet.Trial.proj('trial_stim_prob_left','trial_feedback_type')  & 'trial_stim_prob_left = 0.5'
    data = trained_subjects * interesting_trials

    all_streaks = {}
    all_subjects = np.unique(data.fetch('subject_uuid'));
    for i, mouse in enumerate(all_subjects):
        print(i,'/',len(all_subjects))
        all_streaks[str(mouse)] = {}
        mouse_portion = data & {'subject_uuid': mouse}
        
        all_sessions_mouse = np.unique(mouse_portion.fetch('session_start_time'))
        
        for session in all_sessions_mouse:
            all_streaks[str(mouse)][session] = {}
            session_table = mouse_portion & {'subject_session_start_date': session}
            answers = session_table.fetch('trial_feedback_type')
            
            rewards, failures = find_streaks(answers)
            all_streaks[str(mouse)][session]['rewards'] = rewards
            all_streaks[str(mouse)][session]['failures'] = failures

    with open('all_streaks.pickle', 'wb') as handle:
        pickle.dump(all_streaks, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return


if __name__=="__main__":
    main()