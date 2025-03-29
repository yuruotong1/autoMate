"""
Workflow extraction module that processes mixed sequences of utterances and actions
to generate intent-based workflow segments
"""

class WorkflowExtractor:
    """
    Extracts workflows from mixed sequences of utterances and actions
    by segmenting based on utterance boundaries
    """
    
    def __init__(self):
        """Initialize workflow extractor"""
        pass
    
    def process_mixed_sequence(self, sequence):
        """
        Process a mixed sequence of utterances and actions
        
        Args:
            sequence: List of dictionaries containing utterances and actions
                Each item must have 'type' ('utterance' or 'action') and 'timestamp'
        
        Returns:
            List of (intent, actions) tuples representing workflow segments
        """
        if not sequence:
            return []
        
        # Sort by timestamp to ensure proper ordering
        sorted_sequence = sorted(sequence, key=lambda x: x['timestamp'])
        
        # First pass: Merge consecutive utterances with no actions in between
        merged_sequence = []
        i = 0
        while i < len(sorted_sequence):
            current_item = sorted_sequence[i].copy()  # Create a copy to avoid modifying original
            
            # If current item is an utterance, check if we can merge with next utterances
            if current_item['type'] == 'utterance':
                merged_text = current_item['text']
                next_i = i + 1
                
                # Look ahead for the next items
                has_actions_between = False
                last_utterance_idx = i
                
                while next_i < len(sorted_sequence):
                    next_item = sorted_sequence[next_i]
                    
                    # If we found an action, mark that there are actions between utterances
                    if next_item['type'] == 'action':
                        has_actions_between = True
                    
                    # If we found another utterance
                    elif next_item['type'] == 'utterance':
                        # If there were no actions between, merge this utterance
                        if not has_actions_between:
                            merged_text += " " + next_item['text']
                            last_utterance_idx = next_i
                        else:
                            # There were actions between, stop looking
                            break
                    
                    next_i += 1
                
                # Update the merged text in the current utterance if we found utterances to merge
                if last_utterance_idx > i:
                    current_item['text'] = merged_text
                    # Skip the merged utterances in the next iteration
                    i = last_utterance_idx
            
            merged_sequence.append(current_item)
            i += 1
        
        # Find all utterance indices in the merged sequence
        utterance_indices = [
            i for i, item in enumerate(merged_sequence) 
            if item['type'] == 'utterance'
        ]
        
        if not utterance_indices:
            # No utterances found, return empty result
            return []
        
        # Extract workflow segments based on utterance boundaries
        segments = []
        
        for i in range(len(utterance_indices)):
            # Current utterance index
            curr_idx = utterance_indices[i]
            
            # Extract the utterance
            utterance = merged_sequence[curr_idx]
            
            # Determine segment end (next utterance or end of sequence)
            next_idx = utterance_indices[i+1] if i+1 < len(utterance_indices) else len(merged_sequence)
            
            # Extract the actions between this utterance and the next
            actions = [
                merged_sequence[j] for j in range(curr_idx+1, next_idx)
                if merged_sequence[j]['type'] == 'action'
            ]
            
            # Add the segment to the result
            segments.append((utterance, actions))
        
        return segments
    
    def format_sequence_for_analysis(self, utterance, actions):
        """
        Format a (utterance, actions) pair for LLM analysis
        
        Args:
            utterance: The utterance dictionary
            actions: List of action dictionaries
        
        Returns:
            Dictionary with formatted utterance and actions
        """
        return {
            "intent": utterance.get('text', ''),
            "utterance": utterance,
            "actions": actions
        }
    
    def extract_workflows(self, mixed_sequence):
        """
        Extract workflows from a mixed sequence and format for analysis
        
        Args:
            mixed_sequence: List of dictionaries containing utterances and actions
        
        Returns:
            List of formatted workflow segments ready for LLM analysis
        """
        segments = self.process_mixed_sequence(mixed_sequence)
        return [
            self.format_sequence_for_analysis(utterance, actions)
            for utterance, actions in segments
        ] 