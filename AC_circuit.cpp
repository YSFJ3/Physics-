#include "Circuit.h"

// Functions
char lower_to_upper(char component_type) 
{
	char component_type_capital;
	component_type_capital = toupper(component_type);
	return component_type_capital;
}

double numeric_input_check(double input_to_check) 
{
	while (1)
	{
		if (std::cin.fail())
		{
			std::cin.clear();
			std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
			std::cout << "You have entered wrong input" << std::endl;
			std::cout << "Please enter a number" << std::endl;
			std::cin >> input_to_check;
		}
		if (!std::cin.fail())
			
			break;
	}
	return input_to_check;
}

void menu()
{
	bool new_circuit_choice = true;
	int menu_selection;
	std::complex<double> impedance_whole_circuit;
	std::vector<component*> components;
	std::vector<component*> series_components;
	std::vector<component*> parralel_components;
	std::vector<circuit*> new_circuit;
	int circuit_count{ 0 };
	std::cout.precision(3);
	while (new_circuit_choice != false) {
		std::cout << "What is the frequency of the circuit in Hz? ";
		double frequency_value{};
		std::cin >> frequency_value;
		frequency_value = numeric_input_check(frequency_value);
		new_circuit.push_back(new circuit(frequency_value));
		bool circuit_run = true;
		while (circuit_run != false) {
			// Create menu 
			std::cout << " 1 - Add component to the circuit components catalogue.\n";
			std::cout << " 2 - Display the circuit components catalogue.\n";
			std::cout << " 3 - Add component in series.\n";
			std::cout << " 4 - Add component in parralel.\n";
			std::cout << " 5 - Display current circuit information.\n";
			std::cout << " 6 - Display individual components information.\n";
			std::cout << " 7 - Add a new circuit.\n";
			std::cout << " 8 - Display all created circuits information.\n";
			std::cout << " 9 - Combine all made circuits in series and display the total circuit information.\n";
			std::cout << " 10 - Exit.\n";
			std::cout << " Enter your choice and press return: ";
			std::cin >> menu_selection;
			menu_selection = numeric_input_check(menu_selection);
			std::cout << "\n";

			switch (menu_selection)
			{
			case 1:
				// Create components catalogue
				std::cout << "Add a component to the circuit components catalogue \n";
				std::cout << "Is your component real[R] or ideal[I] \n";
				char real_or_ideal;
				std::cin >> real_or_ideal;
				real_or_ideal = lower_to_upper(real_or_ideal);
				std::cout << "Do you want to add a Resistor[R], Inductor[I] or a Capacitor[C]? \n";
				char component_type;
				std::cin >> component_type;
				component_type = lower_to_upper(component_type);
				// Make a resistor
				if (component_type == 'R') {
					std::cout << "What is the resistance of the resistor in ohms? ";
					double resistance_value{};
					std::cin >> resistance_value;
					resistance_value = numeric_input_check(resistance_value);
					if (real_or_ideal == 'R') {
						std::cout << "What is the parasatic inductance of the resistor in H? ";
						double parasatic_inductance_value{};
						std::cin >> parasatic_inductance_value;
						parasatic_inductance_value = numeric_input_check(parasatic_inductance_value);
						std::cout << "What is the parasatic capacitance of the resistor in F? ";
						double parasatic_capacitance_value{};
						std::cin >> parasatic_capacitance_value;
						parasatic_capacitance_value = numeric_input_check(parasatic_capacitance_value);
						components.push_back(new real_resistor{ frequency_value, resistance_value, parasatic_inductance_value, parasatic_capacitance_value });
					}
					else {
						components.push_back(new resistor{ resistance_value });
					}
				}
				// Make an inductor
				else if (component_type == 'I') {
					std::cout << "What is the inductance of the inductor in H? ";
					double inductance_value{};
					std::cin >> inductance_value;
					inductance_value = numeric_input_check(inductance_value);
					if (real_or_ideal == 'R') {
						std::cout << "What is the parasatic resistance of the inductor in ohms? ";
						double parasatic_resistance_value{};
						std::cin >> parasatic_resistance_value;
						parasatic_resistance_value = numeric_input_check(parasatic_resistance_value);
						std::cout << "What is the parasatic capacitance of the inductor in F? ";
						double parasatic_capacitance_value{};
						std::cin >> parasatic_capacitance_value;
						parasatic_capacitance_value = numeric_input_check(parasatic_capacitance_value);
						components.push_back(new real_inductor{ inductance_value, frequency_value, parasatic_capacitance_value, parasatic_resistance_value });
					}
					else {
						components.push_back(new inductor{ inductance_value, frequency_value });
					}

				}
				// Make a capacitor
				else {
					std::cout << "What is the capacitance of the capacitor in F? ";
					double capacitance_value{};
					std::cin >> capacitance_value;
					capacitance_value = numeric_input_check(capacitance_value);
					if (real_or_ideal == 'R') {
						std::cout << "What is the parasatic resistance of the capacitor in ohms? ";
						double parasatic_resistance_value{};
						std::cin >> parasatic_resistance_value;
						parasatic_resistance_value = numeric_input_check(parasatic_resistance_value);
						std::cout << "What is the parasatic inductance of the capacitor in in H? ";
						double parasatic_inductance_value{};
						std::cin >> parasatic_inductance_value;
						parasatic_inductance_value = numeric_input_check(parasatic_inductance_value);
						components.push_back(new real_capacitor{ capacitance_value, frequency_value, parasatic_inductance_value, parasatic_resistance_value });
					}
					else {
						components.push_back(new capacitor{ capacitance_value, frequency_value });
					}
				}

				break;
			case 2:
				// Print out all components that have been added
				std::cout << '\n' << "***COMPONENTS CATALOGUE*** \n";
				if (components.size() == 0) {
					std::cout << "You need to add components \n";
					break;
				}
				else {
					for (int i = 0; i < components.size(); i++) {
						int real_index = i + 1;
						components[i]->catalogue_print(real_index);
					}
					break;
				}
			case 3:
				// Add components in series
				std::cout << '\n' << "Add a component/ components from the catalogue in series \n";
				if (components.size() == 0) {
					std::cout << "You need to add components \n" << '\n';
					break;
				}
				else {
					// Assign each component a number the user can type in
					for (int i = 0; i < components.size(); i++) {
						int real_index = i + 1;
						components[i]->catalogue_print(real_index);
					}
					bool series_add = true;
					while (series_add != false) {
						int component_index;
						std::cout << "Press a number to add that component to series\n";
						std::cin >> component_index;

						series_components.push_back(components[component_index - 1]);
						char series_condition;
						std::cout << "Do you want to add another component in series [Y/N]?\n";
						std::cin >> series_condition;
						series_condition = lower_to_upper(series_condition);
						if (series_condition == 'N') {
							series_add = false;
						}
						else {
						}
					}
					// Calculate series impedance for the circuit
					new_circuit[circuit_count]->series_component(series_components);
					break;
				}
			case 4:
				// Add components in parralel
				if (components.size() == 0) {
					std::cout << "You need to add components \n" << '\n';
					break;
				}
				else {
					// Can only add components in series before adding in parralel
					if (series_components.size() == 0) {
						std::cout << "You need to add components in series first. \n" << '\n';
						break;
					}
					else {
						// Assign each component a number the user can type in
						std::cout << '\n' << "Add a component/ components from the catalogue in parralel\n";
						std::cout << "***COMPONENTS CATALOGUE*** \n";
						for (int i = 0; i < components.size(); i++) {
							int real_index = i + 1;
							components[i]->catalogue_print(real_index);
						}
						bool parralel_add = true;
						while (parralel_add != false) {
							int component_index;
							std::cout << "Press a number to add that component in parralel\n";
							std::cin >> component_index;
							parralel_components.push_back(components[component_index - 1]);
							char parralel_condition;
							std::cout << "Do you want to add another component in parralel [Y/N]?\n";
							std::cin >> parralel_condition;
							parralel_condition = lower_to_upper(parralel_condition);
							if (parralel_condition == 'N') {
								parralel_add = false;
							}
							else {
							}
						}
						// Calculate parralel impedance for the circuit
						new_circuit[circuit_count]->parralel_component(parralel_components);
						break;
					}

				}
			case 5:
				// Print circuit information
				std::cout << "CIRCUIT INFORMATION\n";
				new_circuit[0]->print();
				break;
			case 6:
				// Print indiividual components information
				if (components.size() == 0) {
					std::cout << "You need to add components \n";
					break;
				}
				else {
					std::cout << "INDIVIDUAL COMPONENTS INFORMATION.\n";
					for (int i = 0; i < components.size(); i++) {
						components[i]->print();
					}
					break;
				}

			case 7:
				// Ask the user if they want to add another circuit 
				circuit_run = false;
				char circuit_condition;
				std::cout << "Do you want to add another circuit [Y/N]?\n";
				std::cin >> circuit_condition;
				circuit_condition = lower_to_upper(circuit_condition);
				if (circuit_condition == 'N') {
					new_circuit_choice = false;
				}
				else {
					// Add to the number of circuits being tracked by the circuit count variable
					circuit_count = circuit_count + 1;
					// Clear series and parralel components vectors so they can be used by the new circuit
					series_components.clear();
					parralel_components.clear();
				}
				break;
			case 8:
				// Print the information for all the circuits that have been created
				std::cout << "All created circuits information.\n";
				for (int i = 0; i < new_circuit.size(); i++) {
					std::cout << "Circuit-" << i + 1 << std::endl;
					new_circuit[i]->print();
				}
				break;
			case 9:
				// Combine all circuits in series and print out there information
				std::cout << "Circuit information after combining all created circuits in series.\n";

				for (int i = 0; i < new_circuit.size(); i++) {
					impedance_whole_circuit += new_circuit[i]->get_impedance();
				}
				std::cout << "The combination of circuits has an IMPEDANCE: " << impedance_whole_circuit << std::endl;
				std::cout << "IMPEDANCE MAGNITUDE: " << abs(impedance_whole_circuit) << std::endl;
				std::cout << "IMPEDANCE PHASE: " << arg(impedance_whole_circuit) << std::endl;
				break;
			case 10:
				// Exit program
				std::cout << "End of Program.\n";
				circuit_run = false;
				new_circuit_choice = false;
				break;
			default:
				// Check for invalid user menu input
				std::cout << "Not a Valid Choice. \n";
				std::cout << "Choose again.\n";
				break;
			}


		}
	}
	// clear components vector
	std::cout << "Components has size " << components.size() << std::endl;
	for (auto components_it = components.begin();
		components_it < components.end();
		++components_it) delete* components_it;
	components.clear();
	std::cout << "components now has size " << components.size() << std::endl;
}

int main() 
{
	menu();
	return 0;
}
		


