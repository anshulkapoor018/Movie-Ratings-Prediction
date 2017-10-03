import random
import Index

def cost(weight):
	sum=0
	for z in range(10):
		movie_file='training'+str(z)+'.csv'
		index_file='index'+str(z)+'.csv'
		test_file='testing'+str(z)+'.csv'
		index=Index.create_index(weight,movie_file,index_file)
		movie=Index.create_movie(test_file,index)
		for k in movie.keys():
			temp=estimate(movie[k][0:5],weight)
			if (temp!=0):
				sum+=(temp-movie[k][5] )*(temp-movie[k][5] )
	return sum

#Calculation of Rating using attributes of movies
def estimate(scores,weight):
	sum=0
	sum_weight=0
	for i in range(len(scores)):
		if (scores[i]!=0):
			sum+=scores[i]*weight[i]
			sum_weight+=weight[i]
	if sum_weight!=0:
		return sum/sum_weight
	else:
		return 0

def optimize(dom,movie_file='SampleDataset.csv',index_file='IndexedArtists.csv',test_file='test.csv',cost=cost,popsize=50,step=0.01,
                    mp=0.2,el=0.2,max=100,):
  # Mutation Operation
  def mutation(v):
    i=random.randint(0,len(dom)-1)
    if random.random()<0.5 and v[i]-step>dom[i][0]:
      return v[0:i]+[round(v[i]-step,2)]+v[i+1:]
    elif v[i]+step<dom[i][1]:
      return v[0:i]+[round(v[i]+step,2)]+v[i+1:]
    else:
      return v

  # Crossover Operation
  def crossover(r1,r2):
    i=random.randint(1,len(dom)-2)
    return r1[0:i]+r2[i:]

  pop=[]
  pop_set=set()
  for i in range(popsize):
    vec=[round( random.uniform(dom[i][0], dom[i][1]),2)
         for i in range(len(dom))]
    pop.append(vec)
    pop_set=pop_set.union([str(vec)])

  top=int(el*popsize)-1
  scores_index={}
  # Main loop
  for i in range(max):
    scores=[]
    for v in pop:
        temp=str(v)

        if scores_index.has_key(temp):
            score=scores_index[temp]
        else:
            score=cost(v)
            scores_index.update({temp:score})
        scores.append((score,v))
        scores.sort()
        print scores
    ordered=[v for (s,v) in scores]

    # Start with the pure winners
    pop=ordered[0:top]
    pop_set=set()
    for p in pop:
        pop_set=pop_set.union([str(p)])


    while len(pop)<popsize:
      if random.random()<mp:

        # Mutation
        c=random.randint(0,top)
        temp=mutation(ordered[c])
        if not( str(temp) in pop_set ):
            pop.append(temp)
            pop_set=pop_set.union([str(temp)])

      else:
        # Crossover
        c1=random.randint(0,top)
        c2=random.randint(0,top)
        temp=mutation(crossover(ordered[c1],ordered[c2]))
        if not( str(temp) in pop_set ):
            pop.append(temp)
            pop_set=pop_set.union([str(temp)])

  print scores[0][0],scores[0][1]
  return scores[0]