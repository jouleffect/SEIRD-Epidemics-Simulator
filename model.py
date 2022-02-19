# Network

import numpy as np 
import pandas as pd 
import simulator
import random
from igraph import *
import matplotlib.pyplot as plt


class Network():
	"""docstring for Network"""
	def __init__(self, simulator):
		
		# Genero un grafo random
		self.g = Graph.Erdos_Renyi(simulator.num_nodi,simulator.p_link)

		# Inizializzazione dei vettori degli step temporali e degli stati epidemici
		self.t_state = np.zeros((simulator.num_nodi,1))
		self.e_state = np.zeros((simulator.num_nodi,1),dtype=np.int8)	

		# assegnazione iniziale random dei nodi esposti
		np.put(self.e_state,np.random.choice(range(simulator.num_nodi*1), simulator.exp0, replace=False),1)	
				
		self.states = {}	# Lista degli stati
		self.data = pd.DataFrame(columns=["index","days","exposed","infected","severe infected","recovered","dead","susceptible","total"]) # Tabella stati


	def update_states(self,i,simulator): # Aggiornamento degli stati
		"""Lista degli stati:
			- Susceptible = 0
			- Exposed = 1
			- Infected = 2
			- Severe Infected = 3
			- Recovered = 4
			- Dead = 5
		"""

		# Copia degli stati epidemici dagli array degli stati epidemici al dizionario	
		self.states = { 'exposed':np.where(np.copy(self.e_state)==1,self.e_state,0),
						'infected':np.where(np.copy(self.e_state)==2,self.e_state,0), 
						'recovered':np.where(np.copy(self.e_state)==4,self.e_state,0), 
						'severe_infected':np.where(np.copy(self.e_state)==3,self.e_state,0), 
						'dead':np.where(np.copy(self.e_state)==5,self.e_state,0), 
						'susceptible':(simulator.num_nodi - np.count_nonzero(np.copy(self.e_state))), 
						'total_cases':np.count_nonzero(np.copy(self.e_state)) }

		# Inserimento della somma di ogni stato epidemico nel dataframe 
		self.data.loc[i,:] = [i, i*simulator.dt_state,np.count_nonzero(self.states['exposed']), np.count_nonzero(self.states['infected']),
		np.count_nonzero(self.states['severe_infected']), np.count_nonzero(self.states['recovered']),
		np.count_nonzero(self.states['dead']), self.states['susceptible'], self.states['total_cases']]

		#print(self.data)

	def plot(self,i,simulator): # Creazione Grafici
		
		plt.clf()

		ax = plt.gca()
		self.data.plot(x = 'days', y = 'susceptible', kind = 'line', color = 'cyan', ax = ax)
		self.data.plot(x = 'days', y = 'exposed', kind = 'line', color = 'yellow', ax = ax)
		self.data.plot(x = 'days', y = 'infected', kind = 'line', color = 'blue', ax = ax)
		self.data.plot(x = 'days', y = 'severe infected', kind = 'line', color = 'magenta', ax = ax)
		self.data.plot(x = 'days', y = 'recovered', kind = 'line', color = 'green', ax = ax)
		self.data.plot(x = 'days', y = 'dead', kind = 'line', color = 'brown', ax = ax)


		plt.title('link_p: {}; exp0: {}; t_inc: {}; t_inf: {}\n alpha: {}; beta: {}; gamma: {}'.format(simulator.p_link, simulator.exp0,simulator.t_exp,simulator.t_inf,simulator.alfa,simulator.beta,simulator.gamma))
		plt.xlabel('Time (days)')
		plt.ylabel('Number of nodes')
		plt.savefig('./plots/states.png')

	def update_nodes(self,i,simulator): # Aggiornamento dei nodi del network (rimozione dei nodi morti e isolamento dei nodi gravemente infetti)
		pass


	def get_new_cases(self,i,simulator): # Nuovi casi (aggiornamento dei nodi che propagano l'epidemia)

		# Trova i vicini degli esposti, infetti e gravemente infetti
		# Calcola la probabilità che i vicini siano contaggiati con tasso alfa

		# Nodi esposti
		n_exp = np.array(np.nonzero(self.states['exposed'])[0])
		# Nodi infetti
		n_inf = np.array(np.nonzero(self.states['infected'])[0])
		# Nodi gravemente infetti
		n_g_inf = np.array(np.nonzero(self.states['severe_infected'])[0])
		# Nodi guariti
		n_rec = np.array(np.nonzero(self.states['recovered'])[0])
		# Nodi morti
		n_dead = np.array(np.nonzero(self.states['dead'])[0])

		new_cases = []
		
		# Ciclo i Nodi esposti, infetti e gravemente infetti e trovo i loro vicini suscettibili che vengono contaggiati con tasso alfa
		contaggiosi = np.concatenate((n_exp,n_inf,n_g_inf), axis=None)

		for x in contaggiosi:
			for n in self.g.neighbors(x):
				Rand = np.random.random()
				# Condizione per entrare nei nuovi casi di esposto (Rientra nella prob, non è nella categoria contaggiati, ne in quella guariti ne in quella morti, nemmeno doppione)
				if (Rand<simulator.alfa) and (n not in contaggiosi) and (n not in n_rec) and (n not in n_dead) and (n not in new_cases):
					new_cases.append(n)

		#print(new_cases)
		return new_cases
