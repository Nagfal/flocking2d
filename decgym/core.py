import sys
sys.path.append('D:\PyProject')
import decgym

# Env-related abstractions

class DecEnv(object):
    """     
    The main decgym class. It encapsulates an environment with
    arbitrary behind-the-scenes dynamics. An environment can be
    partially or fully observed. Within decgym, DecEnvs will usually 
    be muti-agent and decentralized.

    The main API methods that users of this class need to know are:

        step
        reset
        render
        close
        seed
    
    And set the following attributes:

        action_space_red: a list of available actions of team red robots
        action_space_blue: a list of available actions of team blue robots
        observation_space_red: a list of possible observations may got by team red robots
        observation_space_blue: a list of possible observations may got by team blue robots
        reward_range_red_team: A tuple corresponding to the min and max possible rewards of team red
        reward_range_red_indi: A tuple corresponding to the min and max possible rewards of robot in team red, in dec-pomdp problem, this range should be [0,0]
        reward_range_blue_team: A tuple corresponding to the min and max possible rewards of team blue
        reward_range_blue_indi: A tuple corresponding to the min and max possible rewards of robot in team blue, in dec-pomdp problem, this range should be [0,0]

    Note: a default team reward range set to [-inf,+inf] 
    and a default individual reward range set to [0,0]already exists. Set it if you want a narrower range.
    The methods are accessed publicly as "step", "reset", etc.. 
    """

    # Set this in SOME subclasses
    metadata = {'render.modes': []}
    reward_range_red_team = (-float('inf'), float('inf'))
    reward_range_blue_team = (-float('inf'), float('inf'))
    reward_range_red_indi = (0,0)
    reward_range_blue_indi = (0,0)
    spec = None

    # Set these in ALL subclasses
    action_space = None
    observation_space = None

    def step(self, actions_red, actions_blue):
        """Run one timestep of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state.

        Accepts an action and returns a tuple (observation, reward, done, info).

        Args:
            action (object): an action provided by the environment

        Returns:
            observation (list): agents' observation of the current environment
                                observation[0][] for team red, observation[1][]for team blue, observation[][0] for whole team, and observation[][1:] for each individual
            reward (dict) : amount of reward returned after previous action, 
                           
            done (boolean): whether the episode has ended, in which case further step() calls will return undefined results
            info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning)
        """
        raise NotImplementedError
    
    def reset(self):
        """Resets the state of the environment and returns an initial observation.

        Returns: observation (object): the initial observation of the
            space.
        """
        raise NotImplementedError

    def render(self, mode = 'image', timestep=(0,0)):
        """ Render the environment.

        If mode is:
        -- image : render the current environment to a iamge and return nothing
        -- vedio : render a vedio start at timestep[1] end at timestep[1]

        Args:
            mode (str): the mode to render with
            timestep(tuple): the start timestep and end timestep of vedio """
        raise NotImplementedError
    
    def close(self):
        """Override _close in your subclass to perform any necessary cleanup.

        Environments will automatically close() themselves when
        garbage collected or when the program exits.
        """
        return
    
    def seed(self, seed=None):
        """Sets the seed for this env's random number generator(s).

        Note:
            Some environments use multiple pseudorandom number generators.
            We want to capture all such seeds used in order to ensure that
            there aren't accidental correlations between multiple generators.

        Returns:
            list<bigint>: Returns the list of seeds used in this env's random
              number generators. The first value in the list should be the
              "main" seed, or the value which a reproducer should pass to
              'seed'. Offen, the main seed equals the provided 'seed', but
              this won't be true if seed=None, for example.
        """
        return
    
