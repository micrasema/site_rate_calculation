import sys
import re
import argparse

def retrieve_command(input):
	pass

# This is copied straight from phyml.py, need to modify so it works with site rate commands
def run_phyml(command):
    global _phyml_binary
    if _phyml_binary is None:
        _phyml_binary = find_program()

    #turn off any memory checking in PhyML - thanks Jess Thomas for pointing out this problem
    command = "%s --no_memory_check" % (command)

    # Add in the command file
    log.debug("Running 'phyml %s'", command)
    command = "\"%s\" %s" % (_phyml_binary, command)

    # Note: We use shlex.split as it does a proper job of handling command
    # lines that are complex
    p = subprocess.Popen(
        shlex.split(command),
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    # Capture the output, we might put it into the errors
    stdout, stderr = p.communicate()
    # p.terminate()

    if p.returncode != 0:
        log.error("Phyml did not execute successfully")
        log.error("Phyml output follows, in case it's helpful for finding the problem")
        log.error("%s", stdout)
        log.error("%s", stderr)
        raise PhymlError

def parse_rates(phyml_lk_file):
	'''
	Parses the mean relative rates from the PhyML
	*_phyml_lk.txt file. Returns a dictionary with site
	numbers as keys and mean relative rates as values
	'''
	# Open phyml_lk output file
	lnl_file = phyml_lk_file
	# Begin line counting
	line_number = 0
	# Assign variable to empty dictionary to store site rates
	site_dict = {}
	# Begins site numbers to add to dicitonary with rates
	site = 1
	# Loop through lines and store site rates in dictionary
	for line in lnl_file.readlines():
		line_number += 1
		# If the line contains data (greater than line 7, take the data)
		if line_number > 7:
			# Split data objects into a list and remove 
			# unnecessary whitespace
			rate_list = " ".join(line.split()).split(" ")
			# This could also be done with regular expressions:
			# rate_list = re.sub(' +', ' ', line).split(" ")
			# assign rate variable to last item in list
			rate = rate_list[-1]
			# Add rates to dictionary with site numbers
			site_dict[site] = float(rate)
			# Increase site number by one for next dictionary entry
			site += 1
	return site_dict

def categorize_rates(phyml_lk_file):
	'''
	Takes the PhyML *_phyml_lk.txt file as input and returns
	a dictionary with site numbers as keys and the rate category
	with the highest likelihood as values.
	'''
	# Assign file to a variable
	lnl_file = phyml_lk_file
	# Start the count of the line number
	count = 0
	# Begin site number count
	site = 1
	# Create dictionary to house site rate category info
	rate_cat_dict = {}
	# Loop through and pull the highest of the four categories
	for line in phyml_lk_file:
		count += 1
		if count > 7:
			# print line
			# Split the data and objects into a list and remove 
			# unnecessary whitespace
			rate_list = " ".join(line.split()).split(" ")
			# print rate_list
			# remove first two and last numbers from list
			rate_list.pop(-1)
			rate_list.pop(0)
			rate_list.pop(0)
			# print rate_list
			for i in range(len(rate_list)):
				rate_list[i]=float(rate_list[i])
			# print rate_list
			# Add site number and rate category to dictionary
			rate_cat = 1
			best_rate = 0
			for rate in rate_list:
				if rate > best_rate:
					best_rate = rate
					top = rate_cat
				rate_cat += 1
			rate_cat_dict[site] = top
			site += 1
	# print rate_cat_dict
	return rate_cat_dict

def rates_from_categories(phyml_lk_file):
	'''
	Takes as input the phyml lk file and returns
	a dictionary with sites as keys and a list of
	likelihoods under different rate categories as
	as the values
	'''
	# Assign file to a variable
	lnl_file = phyml_lk_file
	# Start the count of the line number
	count = 0
	# Begin site number count
	site = 1
	# Create dictionary to house site rate category info
	all_rates_dict = {}
	# Loop through and pull the highest of the four categories
	for line in phyml_lk_file:
		count += 1
		if count > 7:
			# print line
			# Split the data and objects into a list and remove 
			# unnecessary whitespace
			rate_list = " ".join(line.split()).split(" ")
			# print rate_list
			# remove first two and last numbers from list
			rate_list.pop(-1)
			rate_list.pop(0)
			rate_list.pop(0)
			# print rate_list
			for i in range(len(rate_list)):
				rate_list[i]=float(rate_list[i])
			# print rate_list
			# Add site number and rate list to dictionary
			all_rates_dict[site] = rate_list
			site += 1
	# print all_rates_dict
	return all_rates_dict


if __name__ == "__main__":
	in_file = sys.argv[1]
	phyml_lk_file = open(in_file)
	rate_cat_dict = categorize_rates(phyml_lk_file)
	count = 1
	for i in range(len(rate_cat_dict)):
		print str(count) + '\t' + str(rate_cat_dict[count])
		count += 1