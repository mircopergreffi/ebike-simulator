
import yaml
import matplotlib.pyplot as plt

def main():
	
	with open('config.yaml', 'r') as f:
		config = yaml.safe_load(f)
	
	defaults = config["defaults"]
	simulations = config["simulations"]

	for simulation in simulations:
		# Default values
		for key, value in defaults.items():
			if key not in simulation:
				simulation[key] = value
		
		simulation["mass"] = simulation["mass_vehicle"] + simulation["mass_passenger"]

		# Calculate coefficients
		k = simulation["air_density"] * simulation["drag_coefficient"] * simulation["frontal_area"] / 2
		mgf = simulation["mass"] * defaults["gravity"] * simulation["rolling_resistance"]
		F_max = simulation["max_torque"] / simulation["wheel_radius"]

		# Simulate
		t = [0] # time
		v = [0] # velocity
		P = [0] # friction power
		C = [0] # Wh/km
		while t[-1] <= defaults["exit_time"]:
			# Calculate engine force
			if v[-1] == 0:
				F = F_max
			else:
				F = min(simulation["max_power"] / v[-1], F_max)
			# Air resistance and rolling resistance
			friction = k * v[-1] ** 2 + mgf
			# Substract friction force
			F = F - friction
			# Calculate speed variation
			dv = F / simulation["mass"] * defaults["time_step"]
			# Calculate time and speed
			t.append(t[-1] + defaults["time_step"])
			v.append(v[-1] + dv)
			P.append(friction * v[-1])
			C.append(friction / 3.6)
		
		# Convert to km/h
		v = [x*3.6 for x in v]

		simulation["t"] = t
		simulation["v"] = v
		simulation["P"] = P
		simulation["C"] = C
	
	# Print top speed
	for simulation in simulations:
		print("{} top speed: {:.0f} km/h".format(simulation["name"], max(simulation["v"])))

	# Graphs acceleration simulation results
	for simulation in simulations:
		plt.plot(simulation["t"], simulation["v"], label=simulation["name"])

	plt.xlabel('Time (s)')
	plt.ylabel('Speed (km/h)')
	plt.title('Bike Acceleration')
	plt.legend()
	plt.savefig("images/simulation.png")
	plt.show()

	# Graph power consumption
	for simulation in simulations:
		plt.plot(simulation["v"], simulation["C"], label=simulation["name"])
	
	plt.xlabel('Speed (km/h)')
	plt.ylabel('Consumption (Wh/km)')
	plt.title('Power Consumption')
	plt.legend()
	plt.savefig("images/consumption.png")
	plt.show()

if __name__ == "__main__":
	main()