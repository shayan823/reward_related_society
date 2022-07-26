import numpy as np
from itertools import groupby

import datajoint as dj

dj.config["database.host"] = "datajoint-public.internationalbrainlab.org"
dj.config["database.user"] = "ibl-public"
dj.config["database.password"] = "ibl-public" 
from nma_ibl import reference, subject, action, acquisition, data, behavior, behavior_analyses




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

def get_streak_length(lab, percentage):
  lab_mice_in_training = behavior_analyses.SessionTrainingStatus & 'training_status = "in_training" ' & (subject.SubjectLab & 'lab_name = "{}"'.format(lab)) 
  lab_mice = np.unique(lab_mice_in_training.fetch('subject_uuid'))

  id = lab_mice_in_training.fetch('subject_uuid')
  training_days = np.zeros_like(lab_mice)

  for idx, mouse in enumerate(lab_mice):
    training_days[idx] = len(np.where(id == mouse)[0])

  dictionary = fetch_mice_by_percentage(lab_mice,lab_mice_in_training,percentage)
  # print(dictionary)

  X_0=[]
  X_1=[]
  X_2=[]

  y = []
  for mouse in lab_mice:
    try:
      for i in range(len(dictionary[mouse])):
        session, contrast_left, contrast_right = ((behavior.TrialSet.Trial & {'subject_uuid' : mouse} & {'trial_stim_prob_left': 0.5}) & {'session_start_time' : dictionary[mouse][i]}).fetch('trial_feedback_type',
        'trial_stim_contrast_left',
        'trial_stim_contrast_right')
        
        x_0 = contrast_left + contrast_right
        x_pos = [length_last_streak(session,j,1) for j in range(len(session))]
        x_neg = [length_last_streak(session,j,-1) for j in range(len(session))]

        X_0 = np.append(X_0,x_0)
        X_1 = np.append(X_1,x_pos)
        X_2 = np.append(X_2,x_neg)

        y = np.append(y,session)
    except:
      pass
  X = np.vstack((X_0,X_1,X_2))
  X = X.astype("float")
  y = y.astype("float")

  return (X, y)


def please_work(lab,percentage,verbose = False):
  # works on previous version of get_streak_length
    """ Returns streak of rewards and/or punishments before all trials with 50/50 probability, for all mice in chosen lab, with chosen training percentage.

    Parameters
    ----------    
    lab    : input string
    percentage    : input int

    Output
    ------    
    Output :
    2D array with size (features x samples)
    1D array with size samples
    """


    lab_mice_in_training = behavior_analyses.SessionTrainingStatus & 'training_status = "in_training" ' & (subject.SubjectLab & 'lab_name = "{}"'.format(lab)) 
    
    lab_mice = np.unique(lab_mice_in_training.fetch('subject_uuid'))
    print(np.shape(lab_mice))
    id = lab_mice_in_training.fetch('subject_uuid')
    training_days = np.zeros_like(lab_mice)

    for idx, mouse in enumerate(lab_mice):
      training_days[idx] = len(np.where(id == mouse)[0])

    dictionary = fetch_mice_by_percentage(lab_mice,lab_mice_in_training,percentage)
    X_0 = []   # contrast
    X_1 = []   # feature 1, streaks of 2
    X_2 = []   # feature 2, streaks of 3
    X_3 = []   # feature 3, punishment streaks of 2
    X_4 = []   # feature 4, punishment streaks of 3
    X_5 = []   # water reward volume
    
    y = []
    for m, mouse in enumerate(lab_mice):
      if verbose:
          print('For mouse ', m)
      try:
        for i in range(len(dictionary[mouse])):
          if verbose:
            print('and session ',i)
          session, contrast_left, contrast_right, volume = ((behavior.TrialSet.Trial & {'subject_uuid' : mouse} & {'trial_stim_prob_left': 0.5}) & {'session_start_time' : dictionary[mouse][i]}).fetch('trial_feedback_type','trial_stim_contrast_left','trial_stim_contrast_right','trial_reward_volume')
            
          is_nan = np.argwhere(np.isnan(volume))[:,0]
          if len(is_nan) == len(session) : # all the session is to throw away

            # OPTION 1
            print('Sorry, cannot use this piece of data')

            if verbose:
              #print('Here are the reward volumes')
              #print(reward_volumes)
              #print('during session', i)      
              print('is the reward information for the session useless (all nan)? ' ,len(is_nan) == len(session))
              if len(is_nan) != len(session):
                    print('How many nan are there in this session? ',len(is_nan))                  
              print()
            # we are actually not adding the data to the output!
            continue 
                # OPTION 2
                # reward_volumes = np.nan_to_num(reward_volumes, nan= 123456789)

          elif len(is_nan) != len(session) and len(is_nan) != 0:
            raise Exception("Sorry, I dont know how to deal with missing water reward information in few trials only")
          else:
            if verbose:
              print('water reward info present !')
              
          x_0 = contrast_left + contrast_right
          x_1 = search_sequence(session,2,1) 
          x_2 = search_sequence(session,3,1)
          x_3 = search_sequence(session,2,-1) 
          x_4 = search_sequence(session,3,-1)
          x_5 = volume

          X_0 = np.append(X_0,x_0)
          X_1 = np.append(X_1,x_1)
          X_2 = np.append(X_2,x_2)
          X_3 = np.append(X_3,x_3)
          X_4 = np.append(X_4,x_4)
          X_5 = np.append(X_5,x_5)

          y = np.append(y,session)
      except:
        pass
    

    X = np.vstack((X_0,X_1,X_2,X_3,X_4,X_5))
    X = X.astype("float")
    y = y.astype("float")

    return (X, y)