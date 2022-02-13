# Simulatore 

import numpy as np
import model
import random
from igraph import *

class Simulator():
	"""docstring for Simulator"""
	def __init__(self, num_nodi=10000, p_link=0.5, leng=10000, exp0=20, t_exp=3, t_inf=10, alfa=0.5, beta=0.7, gamma=0.1):

		self.num_nodi = num_nodi # Numero di nodi del network
		self.p_link = p_link	 # Probabilità di connessione

		self.exp0 = exp0 # Numero iniziale di individui esposti alla malattia
		
		self.leng = leng # lunghezza della simulazione
		self.dt_state = 1		# incremento del tempo degli stati (1 giorno)
		self.num_iter = int(self.leng/self.dt_state) # Numero di iterazioni

		self.t_exp = t_exp 	# Tempo di passaggio da Exposed a Infected (tempo di incubazione del virus)
		self.t_inf = t_inf  # Durata dell'infezione fino alla guarigione
		
		self.alfa = alfa	# Tasso di esposizione al virus
		self.beta = beta	# tasso di infezione grave
		self.gamma = gamma	# tasso di mortalità nello stato di infezione grave

	def s_to_e(self, network, contacts): # Transizione da stato Suscettibile a Esposto
		
		# Pongo a 1 gli stati epidemici e a 0 gli stati temporali corrispondenti
		network.e_state[contacts] = 1
		network.t_state[contacts] = 0

	def e_to_i(self, network):	# Transizione da stato Esposto a Infetto
		
		# Calcolo gli infetti prendendo gli esposti che hanno superato il tempo di esposizione
		# Settando a 2 gli stati epidemici e a 0 i corrispondenti stati temporali
		inf = np.where(((network.e_state==1) & (network.t_state >= self.t_exp)),1,0)
		network.e_state = np.where(inf==1,2,network.e_state)
		network.t_state = np.where(inf==1,0,network.t_state)


	def i_to_r(self, network): # Transizione da stato Infetto a Recovered
		
		# Calcolo i recovered prendendo gli infetti che hanno superato il tempo di infezione		
		# Settando a 4 gli stati epidemici
		infected = np.where(((network.e_state==2)&(network.t_state>=self.t_inf)),1,0)
		network.e_state = np.where(infected == 1, 4, network.e_state)


	def i_to_ig(self, network, i): # Transizione da stato Infetto a Gravemente Infetto
		
		# Calcolo i gravemente infetti, prendendo gli infetti che soddisfano la probabilità beta
		inf = np.where((network.e_state==2))
		ind_inf = inf[0]

		Rand = np.random.random((len(ind_inf), 1))

		# Setto gli stati epidemici a 3
		network.e_state[ind_inf[np.where(Rand<(self.beta*self.dt_state))[0]]] = 3


	def ig_to_d(self, network, i): # Transizione da stato Gravemente Infetto a Morto
		
		# Calcolo i morti prendendo gli stati infetti che, superato il tempo di infezione, soddisfano la probabilità gamma
		Rand = np.random.random((self.num_nodi,1)) # generazione numero random

		# Casi di guarigione
		end_inf = np.where((network.t_state >= self.t_inf) & (network.e_state == 3) & (Rand>self.gamma)) 
		network.e_state[end_inf] = 4
		
		# Casi di morte
		dead_inf = np.where((network.t_state >= self.t_inf) & (network.e_state == 3) & (Rand<self.gamma))
		network.e_state[dead_inf] = 5

