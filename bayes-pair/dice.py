prior_fair= {'4':.2,'6':.2,'8':.2,'12':.2,'20':.2}

prior_weight={'4':.08,'6':.12,'8':.16,'12':.24,'20':.40}

def dice(roll, die_sides):
    likelihood=0
    die_sides = float(die_sides)

    if roll <= die_sides:
        likelihood=1./die_sides
    return likelihood
