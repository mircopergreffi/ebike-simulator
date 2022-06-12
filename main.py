
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
		t = [0]
		v = [0]
		while t[-1] <= defaults["exit_time"]:
			# Calculate engine force
			if v[-1] == 0:
				F = F_max
			else:
				F = min(simulation["max_power"] / v[-1], F_max)
			# Subtract air resistance
			F = F - k * v[-1] ** 2
			# Subtract rolling resistance
			F = F - mgf
			# Calculate speed variation
			dv = F / simulation["mass"] * defaults["time_step"]
			# Calculate time and speed
			t.append(t[-1] + defaults["time_step"])
			v.append(v[-1] + dv)
		
		# Convert to km/h
		v = [x*3.6 for x in v]

		simulation["t"] = t
		simulation["v"] = v
	
	# Print top speed
	for simulation in simulations:
		print("{} top speed: {:.0f} km/h".format(simulation["name"], max(simulation["v"])))

	# Graphs simulation results
	for simulation in simulations:
		plt.plot(simulation["t"], simulation["v"], label=simulation["name"])

	plt.xlabel('Time (s)')
	plt.ylabel('Speed (km/h)')
	plt.title('Bike Acceleration')
	plt.legend()
	plt.savefig("images/simulation.png")
	plt.show()


if __name__ == "__main__":
	main()