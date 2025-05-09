import { writable } from 'svelte/store';
import { v4 as uuidv4 } from 'uuid';

// Initial state
const initialState = {
  sequences: [],
  currentSequence: null,
  selectedRows: [],
  isLoading: false,
  error: null
};

// Sample data for demonstration
const sampleData = {
  id: uuidv4(),
  title: 'Sample Cognition Sequence',
  description: 'A demonstration of a synthetic cognition sequence',
  context: 'You are an AI assistant helping a user plan a vacation to Japan.',
  rows: [
    {
      id: uuidv4(),
      parent_id: null,
      goal: 'Help the user plan a 10-day trip to Japan in spring.',
      beliefs: [
        'The user wants to visit Japan in spring.',
        'The user has approximately 10 days for the trip.',
        'Cherry blossom season is a popular time to visit Japan.',
        'The user has not specified a budget constraint.'
      ],
      operation: {
        type: 'Reflect',
        description: 'Consider key factors for planning a Japan trip'
      },
      output: 'To plan an effective 10-day Japan trip in spring, I should consider: 1) Optimal cities/regions to visit in that timeframe, 2) Transportation options between locations, 3) Cherry blossom forecast for timing recommendations, 4) Must-see attractions that align with spring season, 5) Accommodation suggestions in each location.'
    },
    {
      id: uuidv4(),
      parent_id: null,
      goal: 'Help the user plan a 10-day trip to Japan in spring.',
      beliefs: [
        'The user wants to visit Japan in spring.',
        'Cherry blossom season typically runs from late March to early April.',
        'A 10-day trip allows for visiting 2-3 major regions in Japan.',
        'Tokyo, Kyoto, and Osaka are popular destinations for first-time visitors.'
      ],
      operation: {
        type: 'Plan',
        description: 'Create an itinerary outline'
      },
      output: 'Recommended 10-day Japan itinerary:\nDays 1-3: Tokyo (Explore neighborhoods, visit Shinjuku Gyoen for cherry blossoms)\nDays 4-7: Kyoto (Historic temples, Philosopher\'s Path for cherry blossoms)\nDays 8-9: Osaka (Food experiences, day trip to Nara)\nDay 10: Return to Tokyo for departure\n\nThis balanced itinerary allows for experiencing both modern and traditional Japan while maximizing cherry blossom viewing opportunities.'
    }
  ]
};

// Create the store
const createCognitionStore = () => {
  const { subscribe, set, update } = writable(initialState);
  
  return {
    subscribe,
    
    // Initialize with sample data
    initializeWithSampleData: () => {
      update(state => ({
        ...state,
        sequences: [sampleData],
        currentSequence: sampleData
      }));
    },
    
    // Load sequences
    loadSequences: async () => {
      update(state => ({ ...state, isLoading: true }));
      
      try {
        // This would be an API call in a real implementation
        const mockSequences = [sampleData];
        
        update(state => ({
          ...state,
          sequences: mockSequences,
          currentSequence: mockSequences[0],
          isLoading: false
        }));
      } catch (error) {
        update(state => ({
          ...state,
          error: 'Failed to load sequences',
          isLoading: false
        }));
      }
    },
    
    // Set current sequence
    setCurrentSequence: (sequenceId) => {
      update(state => {
        const sequence = state.sequences.find(s => s.id === sequenceId);
        return { ...state, currentSequence: sequence };
      });
    },
    
    // Add a new row
    addRow: (rowData) => {
      update(state => {
        if (!state.currentSequence) return state;
        
        const newRow = {
          id: uuidv4(),
          parent_id: null,
          ...rowData
        };
        
        const updatedSequence = {
          ...state.currentSequence,
          rows: [...state.currentSequence.rows, newRow]
        };
        
        return {
          ...state,
          currentSequence: updatedSequence,
          sequences: state.sequences.map(seq => 
            seq.id === updatedSequence.id ? updatedSequence : seq
          )
        };
      });
    },
    
    // Update a row
    updateRow: (rowId, rowData) => {
      update(state => {
        if (!state.currentSequence) return state;
        
        const updatedRows = state.currentSequence.rows.map(row => 
          row.id === rowId ? { ...row, ...rowData } : row
        );
        
        const updatedSequence = {
          ...state.currentSequence,
          rows: updatedRows
        };
        
        return {
          ...state,
          currentSequence: updatedSequence,
          sequences: state.sequences.map(seq => 
            seq.id === updatedSequence.id ? updatedSequence : seq
          )
        };
      });
    },
    
    // Delete a row
    deleteRow: (rowId) => {
      update(state => {
        if (!state.currentSequence) return state;
        
        const updatedRows = state.currentSequence.rows.filter(row => row.id !== rowId);
        
        const updatedSequence = {
          ...state.currentSequence,
          rows: updatedRows
        };
        
        return {
          ...state,
          currentSequence: updatedSequence,
          sequences: state.sequences.map(seq => 
            seq.id === updatedSequence.id ? updatedSequence : seq
          ),
          selectedRows: state.selectedRows.filter(id => id !== rowId)
        };
      });
    },
    
    // Select/deselect a row
    toggleRowSelection: (rowId) => {
      update(state => {
        const isSelected = state.selectedRows.includes(rowId);
        const updatedSelection = isSelected
          ? state.selectedRows.filter(id => id !== rowId)
          : [...state.selectedRows, rowId];
        
        return {
          ...state,
          selectedRows: updatedSelection
        };
      });
    },
    
    // Clear row selection
    clearSelection: () => {
      update(state => ({
        ...state,
        selectedRows: []
      }));
    },
    
    // Reset store
    reset: () => {
      set(initialState);
    }
  };
};

// Export the store
export const cognitionStore = createCognitionStore();