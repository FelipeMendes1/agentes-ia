import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

class RLAgent:
    def __init__(self):
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=4, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(2, activation='linear'))
        model.compile(loss='mse', optimizer='adam')
        return model

    def get_action(self, state):
        state = np.reshape(state, [1, 4])  # Ajuste o formato do estado
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])
    
    def train(self, state, action, reward, next_state, done):
        # Implementação do treinamento será necessária aqui
        pass
