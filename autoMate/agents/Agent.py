from utils.logging_utils import logger
class Agent:
    def __init__(self, name, prompt=None, knowledge=None):
        self.prompt = prompt
        self.name = name
        self.memory = [] # directly used with LLM
        self.knowledge = knowledge if knowledge else {} # any other information, maybe RAG?
        
        logger.info(f"{self.name} is alive! ")

    def listen(self, input_data):
        '''
        Receives data from user or agent
        '''
        input_data = self._process_data(input_data)
        self.memory.append(input_data)

    
    def _process_data(self, input_data):
        '''
        Further processes the data as needed
        currently just let the agents do it themselves
        '''
        logger.info(f"{self.name} heard: {input_data}")
        return input_data

    def speak(self, target_agent, message):
        '''
        Talk to one agent
        '''
        target_agent.listen(message)

    def broadcast(self, target_agents:list, message):
        '''
        Talk to multiple agents
        '''
        for target_agent in target_agents:
            target_agent.listen(message)

    def think(self):
        # TODO: RL/CoT goes here
        pass


