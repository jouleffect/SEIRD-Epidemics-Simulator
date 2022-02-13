from tkinter import *
import model
import simulator
import matplotlib as plt
from pylab import show

plot_freq = 29

def start_sim():

	global img3

	console.insert(INSERT,"Done!\n> ")

	# Creo gli oggetti di classe simulator e network
	sim = simulator.Simulator(num_nodi.get(),p_link.get(),leng.get(),exp0.get(),t_exp.get(),t_inf.get(),alfa.get(),beta.get(),gamma.get())
	net = model.Network(sim)

	for i in range(sim.num_iter):
		if i%10==0:
			print("Iterazione {}/{} completata\n".format(i,sim.num_iter))
		
		# Aggiorno gli stati epidemici
		net.update_states(i,sim)
		
		# Aggiorno i nodi e i link del network
		net.update_nodes(i,sim)

		# Incremento lo step temporale del network
		net.t_state = net.t_state + sim.dt_state

		# Calcolo i nuovi casi di contatto tra i nodi suscettibili e i vicini con stato epidemico esposto o infetto
		new_cases = net.get_new_cases(i,sim)

		# Calcolo le transizioni dei vari stati epidemici
		sim.s_to_e(net,new_cases)
		sim.e_to_i(net)
		sim.i_to_r(net)
		sim.i_to_ig(net,i)
		sim.ig_to_d(net,i)

		# Creo il grafico degli stati epidemici nel tempo
		if i>=plot_freq and i%plot_freq==0:
			p = net.plot(i,sim)
			
	img3 = PhotoImage(file='plots/states.png')
	plot.itemconfigure(img2, image = img3)



#------------------------------------------------------------------------------------------------
# Scheletro dell'interfaccia

root = Tk()
root.title("SEIR Simulator") 
root.config(bg="skyblue")

left_frame = Frame(root, width=400, height=400, bg='skyblue')
left_frame.grid(row=0, column=0, padx=5, pady=5)
right_frame = Frame(root, width=800, height=600, bg='skyblue')
right_frame.grid(row=0, column=1, padx=5, pady=5)

title = Label(right_frame, text="SEIR Simulator", bg='skyblue')
title.config(font=('Helvetica bold',20))
title.grid(row=0, column=0, padx=5, pady=5)

console = Text(left_frame, width = 25, height = 10, bg='black', fg='white')          
console.grid(row=4, column=0, padx=5, pady=5)
console.insert(INSERT,"##### Console debug #####\n> ")

tool_bar1 = Frame(left_frame, width=400, height=400)
tool_bar1.grid(row=1, column=0, padx=5, pady=5)

tool_bar2 = Frame(left_frame, width=600, height=100)
tool_bar2.grid(row=3, column=0, padx=5, pady=5)

plot = Canvas(right_frame, width=600, height=600, bg='white', borderwidth=2,relief=RIDGE)
img = PhotoImage(file="plots/empty.png")
img2 = plot.create_image(5,5, anchor=NW, image=img)
plot.grid(row=1, column=0, padx=10, pady=10)


#-------------------------------------------------------------------------------------------------
# Variabili da input

num_nodi = IntVar()
num_nodi.set(100)
p_link = DoubleVar()
p_link.set(0.2)
leng = IntVar()
leng.set(30)
exp0 = IntVar()
exp0.set(2)
t_exp = IntVar()
t_exp.set(2)
t_inf = IntVar()
t_inf.set(10)
alfa = DoubleVar()
alfa.set(0.02)
beta = DoubleVar()
beta.set(0.04)
gamma = DoubleVar()
gamma.set(0.03)

#-------------------------------------------------------------------------------------------------
# Oggetti dell'interfaccia

Label(left_frame, text="Network Parameters",bg='skyblue').grid(row=0, column=0, padx=5, pady=1)
Label(tool_bar1, text="Number of nodes").grid(row=1, column=0, padx=5, pady=3, ipadx=10)
Spinbox(tool_bar1, textvariable = num_nodi, from_= 0, to=10000).grid(row=1, column=1, padx=5, pady=5)
Label(tool_bar1, text="Link probability").grid(row=2, column=0, padx=5, pady=3, ipadx=10)
Spinbox(tool_bar1, textvariable = p_link, from_= 0.0, increment=0.01, to=1.0, format="%.2f").grid(row=2, column=1, padx=5, pady=5)
Label(left_frame, text="Simulator Parameters",bg='skyblue').grid(row=2, column=0, padx=5, pady=1)
Label(tool_bar2, text="Number of iterations").grid(row=2, column=0, padx=5, pady=3, ipadx=10)
Spinbox(tool_bar2, textvariable = leng, from_= 0, to=10000).grid(row=2, column=1, padx=5, pady=5)
Label(tool_bar2, text="Initial exposed").grid(row=3, column=0, padx=5, pady=3, ipadx=10)
Spinbox(tool_bar2, textvariable = exp0, from_= 0, to=10000).grid(row=3, column=1, padx=5, pady=5)
Label(tool_bar2, text="Incubation period (days)").grid(row=4, column=0, padx=5, pady=3, ipadx=10)
Spinbox(tool_bar2, textvariable = t_exp, from_= 0, to=10000).grid(row=4, column=1, padx=5, pady=5)
Label(tool_bar2, text="Disease period (days)").grid(row=5, column=0, padx=5, pady=3, ipadx=10)
Spinbox(tool_bar2, textvariable = t_inf, from_= 0, to=10000).grid(row=5, column=1, padx=5, pady=5)
Label(tool_bar2, text="Exposing rate").grid(row=6, column=0, padx=5, pady=3, ipadx=10)
Spinbox(tool_bar2, textvariable = alfa, from_= 0.0, increment=0.01, to=1.0, format="%.2f").grid(row=6, column=1, padx=5, pady=5)
Label(tool_bar2, text="Severe infected rate").grid(row=7, column=0, padx=5, pady=3, ipadx=10)
Spinbox(tool_bar2, textvariable = beta, from_= 0.0, increment=0.01, to=1.0, format="%.2f").grid(row=7, column=1, padx=5, pady=5)
Label(tool_bar2, text="Dead rate").grid(row=8, column=0, padx=5, pady=3, ipadx=10)
Spinbox(tool_bar2, textvariable = gamma, from_= 0.0, increment=0.01, to=1.0, format="%.2f").grid(row=8, column=1, padx=5, pady=5)
Button(tool_bar2, text='Start Simulation', command = start_sim).grid(row=9, column=1, padx=5, pady=1)

#------------------------------------------------------------------------------------------

root.mainloop()