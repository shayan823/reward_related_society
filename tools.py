import numpy as np
from itertools import groupby

def length_last_streak(all_trials,current_trial,streak_type=1):
    """ Gives length of streak of streak_type preceding the current_trial
    Args:
        all_trials (numpy array): an array with all feddback for the session (+1/-1)
        current_trial (int): the index of the current trial
        streak_type (int, optional): type of streak to search for. Defaults to 1, aka reward, else -1 for failure

    Returns:
        len_last_streak:  length of streak of streak_type preceding the current_trial. None if not current type or streak length <2
    """
    #len_last_streak = None as a feature you shouldnt have none
    len_last_streak = 0
    if current_trial > 0:
        grouped_before_index = [list(g) for k,g in groupby(all_trials[:current_trial])] #index is excluded
        if grouped_before_index[-1][0] == streak_type:
        
            if len(grouped_before_index[-1]) > 1:
                len_last_streak = len(grouped_before_index[-1])
    
    return len_last_streak

def fetch_mice_by_percentage(lab_mice, lab_mice_in_training, percentage):
  dictionary = {}

  for mouse in lab_mice:
    one_guy = lab_mice_in_training & {'subject_uuid' : mouse}
    total_trials = len(one_guy.fetch('training_status'))
    train_percentage = np.arange(1,total_trials+1) / total_trials

    bins = np.linspace(0, 100, 10)
    train_percentage_bin = np.digitize(train_percentage*100, bins)*10
    where = np.where(train_percentage_bin == percentage)[0]
    if len(where) !=0:
      dictionary[mouse] = one_guy.fetch('session_start_time')[where]
  return dictionary

def search_sequence(arr,streak_length, feedback):
    """ Find sequence in an array using NumPy only.

    Parameters
    ----------    
    arr    : input 1D array
    streak_length    : input int

    Output
    ------    
    Output : 1D Array with 1s on indices where input array matches the sequence and 0s otherwise.
    """
    # Create the sequence to look for
    seq = np.ones(streak_length)*feedback

    # Store sizes of input array and sequence
    streak = np.zeros(arr.size)
    Na, Nseq = arr.size, seq.size

    # Range of sequence
    r_seq = np.arange(Nseq)

    # Create a 2D array of sliding indices across the entire length of input array.
    # Match up with the input sequence & get the matching starting indices.
    M = (arr[np.arange(Na-Nseq)[:,None] + r_seq] == seq).all(1)

    # Get True values of M and write streak array
    where = np.where(M == True)[0] 
    streak[where] = 1

    return streak

def get_streak_data(lab,percentage,features):
  """ Returns streak of rewards and/or punishments before all trials with 50/50 probability, for all mice in chosen lab, with chosen training percentage.

  Parameters
  ----------    
  lab    : input string
  percentage    : input int
  features: input list of signed ints (positive for reward streak length, negative for punish streak length)

  Output
  ------    
  Output :
  2D array with size (features x samples)
  1D array with size samples
  """


  lab_mice_in_training = ((behavior_analyses.SessionTrainingStatus & {'training_status' : 'in_training'}) * subject.SubjectLab & {'lab_name' : lab}) & behavior.TrialSet.Trial
  lab_mice = np.unique(lab_mice_in_training.fetch('subject_uuid'))

  id = lab_mice_in_training.fetch('subject_uuid')
  training_days = np.zeros_like(lab_mice)

  for idx, mouse in enumerate(lab_mice):
    training_days[idx] = len(np.where(id == mouse)[0])

  dictionary = fetch_mice_by_percentage(lab_mice,lab_mice_in_training,percentage)


  X = np.empty((len(features)+1,1))
  
  y = []
  for mouse in lab_mice:
    try:
      for i in range(len(dictionary[mouse])):
        session, contrast_left, contrast_right = ((behavior.TrialSet.Trial & {'subject_uuid' : mouse} & {'trial_stim_prob_left': 0.5}) & {'session_start_time' : dictionary[mouse][i]}).fetch('trial_feedback_type','trial_stim_contrast_left','trial_stim_contrast_right')
        x_0 = contrast_left + contrast_right
        x = x_0

        for feature in features:
          x = np.vstack( (x,search_sequence(session,abs(feature), np.sign(feature) )))
        
        X = np.concatenate((X,x),axis=1)


        y = np.append(y,session)
    except:
      pass
    
  return(X[:,1:],y.astype('int'))