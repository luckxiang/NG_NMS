import yaml
import pprint

f = open('configs/ngnms.conf')
dataMap = yaml.load(f)
f.close()

pprint.pprint(dataMap)

# # saving data
# f = open('data/newtree.yaml', "w")
# yaml.dump(dataMap, f)
# f.close() 