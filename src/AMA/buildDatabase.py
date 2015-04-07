def buildDatabase(D1, D2, D3):
	# Di's are dictionaries of dictionaries in the form:
	# D1 : relation_name -----> subject --> [(verb, object)] list
	# D2 : relation_name (verb) -----> subject --> [adv] list
	# D3 : relation_name (verb) -----> subject --> [adj] list
	
	# returns a dictionary of the form: subject ----> (list of) properties, where 
	# a subject's property in the result dictionary contains the relation's name
	# and a list of verb-object/adv/adj relations

	D = {}
	for relation_name, inner_dict1 in D1.iteritems():
		for subject, verb_object_properties in inner_dict1.iteritems():
			if not subject in D:
				D[subject] = []
			
			D[subject] += [(relation_name, verb_object_properties)]

	for verb_name, inner_dict2 in D2.iteritems():
		for subject, adv_properties in inner_dict2.iteritems():
			if not subject in D:
				D[subject] = []
			D[subject] += [(verb_name, adv_properties)]

	for verb_name, inner_dict3 in D3.iteritems():
		for subject, adj_properties in inner_dict3.iteritems():
			if not subject in D:
				D[subject] = []
			D[subject] += [(verb_name, adj_properties)]

	return D

# D1 = {"IN": {"Beth":[("live", "Pittsburgh"), ("born", "Nanjing")], "Joe":[("swim","pool"), ("study", "Gates")],
# 			 "Nathan":[("smoke","basement"), ("eat", "kitchen")]},
# 	  "ON": {"Beth":[("jump","table")], "Nathan":[("cry", "shoulder")]}}

# D2 = {"DANCE": {"Beth":["beautifully", "elegantly"], "Joe":["passionately","romantically"]},
# 	  "EAT": {"Nathan":["fast"], "Joe":["slowly"]}}

# D3 = {"BE": {"Beth":["medium-height", "lean","sporty"], "Nathan":["beardy", "lazy"], "Joe":["skinny"], "Jack":["dizzy", "blond"]},
# 	  "BECOME": {"Jack":["an actor", "the student president"], "Nathan":["musician", "fat"]}}

# print buildDatabase(D1, D2, D3)
