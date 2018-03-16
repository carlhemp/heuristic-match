import random

host_num = 0

class Family:
  def __init__(self, name, size, capacity=0):
    self.name = name
    self.size = size
    self.capacity = capacity

class Host:
  def __init__(self, host):
    self.host_name = host.name
    self.capacity = host.capacity
    self.number = host.size
    self.families = [host]
    

Schedule = []          #list of who goes to each place for each week.
                       #each item in list is a list of homes which is a list of
                       #who's at the home.  Ex: [[[,],[...]],[[,],[,]]]

#Most Desirable
def max_utility(i, wk_families):
  global Schedule
#  print Schedule
  utility = []
  for family in wk_families:                        #family = ['Name', size]
    #find max utility for each host in the week
    for host in Schedule[i]:                        #host = Host Class 
      util = family.size + 25/(host.number-host.families[0].size+1)
     
     #(host.capacity-host.families[0].size)/(host.number-host.families[0].size+.9)    #utility = size of family + host family
     
      if family.capacity > 0:
        util += 5
        
      for h_family in host.families:                    #for family in host
        if already_together(h_family,family):           #benefit of family and item not being together 
          util += 0                                     #no benefit if already together 
        else:
          util += 15 #+ h_family.size+family.size         #benefit greater than size of family
      #if util > family.size:
      utility.append([family,host,util])

  return sorted(utility, key=lambda family: family[2], reverse=True)

def already_together(family1, family2):   #two family objects and the schedule
  global Schedule
  for week in Schedule:
    for host in week:
      if (family1 in host.families) and (family2 in host.families):
        return True
  return False

def assign_host_families(week_num,num_host): 
  global Schedule
  global wk_families
  global host_num

  used_hosts = []
  week = []
  host_list = [family for family in wk_families if family.capacity > 0]
  len_host_list = len(host_list)    
  i=0

  if 1 and week_num == 0:
    while i < num_host:
      rand = random.randrange(0,len(wk_families))
      if rand not in used_hosts:
        if wk_families[rand].capacity > 0:
          used_hosts.append(rand)
          week.append(Host(wk_families.pop(rand)))
          i+= 1 
  elif 0:
    max_util = max_utility(week_num-1,host_list)
    for item in max_util:
      #first remove all but 8 hosts that have max utility
      if len_host_list - len(used_hosts) > num_host:   
        if item[0].name not in used_hosts:
          used_hosts.append(item[0].name)
          print item[0].name
          k = 0
          for host in host_list:          #remove host from consideration
            if host_list[k] == item[0].name:
              host_list[k].pop()
              break
            k += 1
      else:
        print used_hosts
        break
    
    #now assign hosts
    for host in host_list:
      if host.name not in used_hosts:
        week.append(add_host(host.name))

  elif 1:
    while i < num_host:
      k = 0
      for family in wk_families:
        if wk_families[k].name == host_list[host_num].name:
          week.append(Host(wk_families.pop(k)))
          break
        k += 1
      host_num += 1
      if host_num > len_host_list - 1:
        host_num -= len_host_list 

      i += 1

  return week

def add_host(name):
  global wk_families
  name_num = 0
  for family in wk_families:
    if wk_families[name_num].name == name:
      break
    name_num +=1
  return Host(wk_families.pop(name_num))


def add_to_host(i, pair):
  global Schedule
  global wk_families

  j = 0
  for item in wk_families:
    if item.name == pair[0].name:
      family = wk_families.pop(j)
      break
    j += 1

  for host in Schedule[i]:
    if host.host_name == pair[1].host_name:
      host.families.append(family)
      host.number += family.size
      break
  
  return


WEEKS=10
MAX_NUMBER_OF_HOSTS = 5

FAMILIES = [Family('Horsts ',12,25),Family('Bruce_Hempels',9,25),Family('Teubls ',6,25),Family('Schnackenbergs',6,25),Family('Williams',7),Family('Brian_Hempels',5),Family('Pattons',7,25),Family('Kresses',9),Family('Walters',6),Family('Stricklands',5,16),Family('Mayfields',2),Family('Carraturos',3,16),Family('Hards  ',2,16),Family('E_Schnacks',2),Family('J_Williams',2),Family('Luke   ',1),Family('Randy  ',1),Family('Casey  ',1)]

#print 'Families: ',FAMILIES,'\n'*2


i=0
while i <= WEEKS-1:
  wk_families = list(FAMILIES)
#  print FAMILIES
  # need to assign host families first
  Schedule.append(assign_host_families(i,MAX_NUMBER_OF_HOSTS))

#------------------------------------------------------------------
  print '\n'*2,'Host Families week ',i+1,':'
  for host in Schedule[i]:
    print host.host_name,'\t',host.number,'/',host.capacity
#------------------------------------------------------------------
  
  max_util_old = []
  # assign remaining families in wk_families based on max utility
  while len(wk_families) > 0:
    print '\nYay!: len(wk_families) = ', len(wk_families)

    # then calc utility
    max_util = max_utility(i, wk_families)  #sorted list of max utility
    if max_util_old == max_util:
      print '\n could not add family to a host. . .  breaking', '\n'*2
      break
    max_util_old = list(max_util)

#------------------------------------------------------------------
    for item in max_util:
      print item[0].name, '\t', item[1].host_name, '\t',item[2]
#------------------------------------------------------------------

    # max utility found, take max utility pair that meet requirements and combine into host family
    for pair in max_util:  
      #print pair[1].capacity
      if pair[0].size + pair[1].number <= pair[1].capacity:
        print 'yay', ' adding ', pair[0].name,'to host: ', pair[1].host_name
        add_to_host(i, pair)
        print 'addition successful'
        break
      else:
        print 'Noooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo', ' No possible!'



  i += 1

   
# print Schedule  
#------------------------------------------------------------------
i = 1
for week in Schedule:
  print '\nHost Families week ',i,':'
  for host in week:
    text = []
    print '\t',host.host_name,'\t',host.number,'/',host.capacity
    for family in host.families:
      text.append(family.name.strip())
    print '\t  ',', '.join(text)
      
  i+=1
#------------------------------------------------------------------


#check families, each family needs to meet each other family
missed = []
print "\nFamilies not able to eat together:"
for family in sorted(FAMILIES):
  for other_family in sorted(FAMILIES,reverse=True):
    if not already_together(family, other_family):
      print family.name, '\t', other_family.name
      missed.append([family, other_family])
    

#number of times as host family
hosts = []
for week in Schedule:
  for host in week:
    hosts.append(host.host_name)

hosts = sorted(hosts)
print "\nHosts:\t\t# of times"
count = 0 
prev_host = hosts[0]
for host in hosts:
  if prev_host != host:
    print prev_host,'\t',count
    count = 1 
  else:
    count += 1
  prev_host = host
print prev_host,'\t',count

